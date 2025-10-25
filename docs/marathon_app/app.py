import streamlit as st
import pandas as pd
from pycaret.regression import load_model, predict_model
from openai import OpenAI
from dotenv import load_dotenv
from dotenv import dotenv_values
import os
import json
from langfuse import Langfuse
from langfuse.decorators import observe
from langfuse.openai import OpenAI as LangfuseOpenAI

load_dotenv()
env = dotenv_values(".env")
#client = OpenAI(api_key=env["OPENAI_API_KEY"])
client = LangfuseOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@observe()
def extract_runner_info(message: str) -> dict:
    system_prompt = """Jesteś asystentem wyodrębniającym dane o biegaczach z tekstu.
Twoje zadanie to znaleźć i zwrócić następujące informacje w formacie JSON:
- "Kategoria wiekowa": wiek jako liczba całkowita
- "Płeć": "K" dla kobiety, "M" dla mężczyzny
- "5 km Czas": czas przebiegnięcia 5 km w minutach jako liczba zmiennoprzecinkowa

Jeśli informacja nie jest dostępna w tekście, użyj null.

Zwróć TYLKO poprawny JSON bez dodatkowego tekstu, w formacie:
{
    "Kategoria wiekowa": [liczba],
    "Płeć": ["K" lub "M"],
    "5 km Czas": [liczba]
}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        
        formatted_result = {
            "Kategoria wiekowa": [result.get("Kategoria wiekowa")],
            "Płeć": [result.get("Płeć")],
            "5 km Czas": [result.get("5 km Czas")]
        }
        
        return formatted_result
        
    except Exception as e:
        print(f"Błąd podczas wyodrębniania danych: {e}")
        return {
            "Kategoria wiekowa": [None],
            "Płeć": [None],
            "5 km Czas": [None]
        }


st.title("Kalkulator czasu maratonu")
st.subheader("Wprowadź swoje dane:")

if "message" not in st.session_state:
        st.session_state.message = ""

col1, col2 = st.columns(2)

with col1:
    wiek = st.number_input(
        "Wiek",
        min_value=15,
        max_value=80,
        value=30,
        step=1,
        help="Podaj swój wiek"
    )
    
    plec = st.selectbox(
        "Płeć",
        options=["M", "K"],
        help="Wybierz płeć"
    )

with col2:
    czas_5km = st.number_input(
        "Czas na 5 km (minuty)",
        min_value=10.0,
        max_value=60.0,
        value=25.0,
        step=0.5,
        format="%.1f",
        help="Podaj swój najlepszy czas na 5 km w minutach"
    )

st.subheader("Albo")    
st.session_state.message = st.text_area(label="Powiedz mi coś o sobie:")

if st.button("Oblicz przewidywany czas maratonu", type="primary", use_container_width=True):
    model = load_model('marathon_regression_pipeline')
    if st.session_state.message == "":
        dane_input = pd.DataFrame({
            'Kategoria wiekowa': [wiek],
            'Płeć': [plec],
            '5 km Czas': [czas_5km]
        })
    else:
        dane_input = pd.DataFrame(extract_runner_info(st.session_state.message))

    predykcja = predict_model(model, data=dane_input)
    przewidziany_czas = predykcja['prediction_label'].values[0]

    st.markdown("### Przewidywany czas ukończenia maratonu:")
    
    godziny = int(przewidziany_czas // 60)
    minuty = int(przewidziany_czas % 60)
    
    d1, d2 = st.columns(2)
    with d1:
        st.metric(
            label="Czas (godziny)",
            value=f"{godziny}h {minuty}min"
        )
    with d2:
        st.text("Twoje dane")
        st.dataframe(dane_input)

    
