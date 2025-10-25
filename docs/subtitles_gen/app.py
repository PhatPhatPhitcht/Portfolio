from dotenv import dotenv_values
#from openai import OpenAI
#from IPython.display import Audio # Stare importy
import streamlit as st
from pydub import AudioSegment
from langfuse.decorators import observe
from langfuse.openai import OpenAI as LangfuseOpenAI
import os
from langfuse import Langfuse
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse()
#langfuse.auth_check() # Alternatywa / bez obserwatora

env = dotenv_values(".env")
#openai_client = OpenAI(api_key=env["OPENAI_API_KEY"]) # Bez Langfuse
llm_client = LangfuseOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@observe()
def generate_subtitles(audio_path):
    with open(audio_path, "rb") as f:
        transcript = llm_client.audio.transcriptions.create(
            file=f,
            model="whisper-1",
            response_format="srt",
        )
    return transcript

@observe()
def transcribe_audio_to_text(audio_path):
    with open(audio_path, "rb") as f:
        transcript = llm_client.audio.transcriptions.create(
            file=f,
            model="whisper-1",
            response_format="verbose_json",
        )

    return transcript.text

@observe()
def translate_srt(srt_text: str) -> str:
    prompt = f"""
    Przetłumacz poniższy plik SRT na język angielski.
    Zachowaj format pliku SRT (numery i znaczniki czasu).
    Tłumacz tylko treść dialogów.
    Nie dodawaj żadnych wyjaśnień, komentarzy ani dodatkowych tekstów.
    Zwróć tylko czysty plik SRT.

    {srt_text}
    """

    response = llm_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return response.choices[0].message.content




if "words" not in st.session_state:
        st.session_state.words = ""

if "subtitles" not in st.session_state:
        st.session_state.subtitles = ""

if "translation" not in st.session_state:
        st.session_state.translation = ""

st.title("Generator napisów")
st.text("Wgraj film by wygenerować tekst lub napisy")

uploaded_file = st.file_uploader(
    "Wybierz plik wideo",
    type=["mp4", "mov", "avi", "mkv"],
    accept_multiple_files=False
)

if uploaded_file is not None:
    st.video(uploaded_file)

    audio = AudioSegment.from_file(uploaded_file)
    audio.export("audio.mp3", format="mp3")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("Pokaż tekst"):
            if st.session_state.words == "":
                st.session_state.words = transcribe_audio_to_text("audio.mp3")
                langfuse.flush()
            if st.session_state.words:
                st.session_state.words = st.text_area("Tekst", value=st.session_state.words,)
            st.download_button(
                label="Pobierz napisy jako TXT",
                data=st.session_state.words,
                file_name="words.txt",
                mime="text/plain")
    with c2:
        if st.button("Generuj napisy"):
            if st.session_state.subtitles == "":
                st.session_state.subtitles = generate_subtitles("audio.mp3")
                langfuse.flush()
            if st.session_state.subtitles:
                st.text_area("Podgląd napisów (SRT):", st.session_state.subtitles, height=300, disabled=True)
            st.download_button(
                label="Pobierz SRT",
                data=st.session_state.subtitles,
                file_name="subtitles.srt",
                mime="application/x-subrip")
    
    if st.session_state.subtitles != "":
        st.text("Przetłumacz na język angielski")
        if st.button("Generuj tłumaczenie"):
                if st.session_state.translation == "":
                    st.session_state.translation = translate_srt(st.session_state.subtitles)
                    langfuse.flush()
                if st.session_state.translation:
                    st.text_area("Podgląd tłumacznia:", st.session_state.translation, height=300, disabled=True)
                st.download_button(
                    label="Pobierz Tłumaczenie",
                    data=st.session_state.translation,
                    file_name="translation.srt",
                    mime="application/x-subrip")

             