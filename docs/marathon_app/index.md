
# Aplikacja do generowania napisów

Ta aplikaca była jednym z zadań, które wykonywałem podczas kursu. Jej celem jest poproszenie o kilka podstawowych danych i użycie wcześniej stworzonego przeze mnie pipelina (pycaret) do obliczenia czasu ukończenia maratonu wrocławskiego.

<a href="app.py" class="md-button md-button--primary">Pobierz Kod</a>

<iframe
    id="content"
    src="app.py"
    width="100%"
    style="border:1px solid black;overflow:hidden;"
></iframe>
<script>
function resizeIframeToFitContent(iframe) {
    iframe.style.height = (iframe.contentWindow.document.documentElement.scrollHeight + 50) + "px";
    iframe.contentDocument.body.style["overflow"] = 'hidden';
}
window.addEventListener('load', function() {
    var iframe = document.getElementById('content');
    resizeIframeToFitContent(iframe);
});
window.addEventListener('resize', function() {
    var iframe = document.getElementById('content');
    resizeIframeToFitContent(iframe);
});
</script>
