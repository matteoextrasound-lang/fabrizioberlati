// Avvia le animazioni SVG delle guide solo quando sono visibili; "Rivedi" le fa ripartire.
// Con "riduci movimento" attivo mostra direttamente l'ultimo fotogramma (data-still, in secondi).
(function () {
  var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('figure.anim').forEach(function (fig) {
    var svg = fig.querySelector('svg'), btn = fig.querySelector('.anim-replay');
    if (!svg || !svg.pauseAnimations) return;
    var end = parseFloat(svg.getAttribute('data-still') || '0');
    svg.pauseAnimations();
    svg.setCurrentTime(still ? end : 0);
    if (still) { if (btn) btn.hidden = true; return; }
    var play = function () { svg.setCurrentTime(0); svg.unpauseAnimations(); };
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) { if (!fig.dataset.started) { fig.dataset.started = 1; play(); } else svg.unpauseAnimations(); }
          else if (fig.dataset.started) svg.pauseAnimations();
        });
      }, { threshold: .35 });
      io.observe(fig);
    } else play();
    if (btn) btn.addEventListener('click', function () { fig.dataset.started = 1; play(); });
  });
})();
