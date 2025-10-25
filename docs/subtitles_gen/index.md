
# Aplikacja do generowania napisów

Oto prosta aplikacja, którą stworzyłęm do generowania napisów i tłumaczenia ich na język angielski. Stworzona została w celu łątiwjszego dostępu do starych filmów, które są ciężkie do zdobycia i czasami tylko dostępne w orginalnej wersji dzwiękowej.

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
