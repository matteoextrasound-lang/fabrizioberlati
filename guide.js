// Calcolatore dell'altezza degli stand per diffusori
(function () {
  var root = document.getElementById('calc');
  if (!root) return;
  var STANDS = JSON.parse(document.getElementById('stands-data').textContent);
  var ear = root.querySelector('#ear'), tw = root.querySelector('#tw'), ft = root.querySelector('#ft');
  var chips = root.querySelectorAll('.chips button');
  var outH = root.querySelector('#out-h'), outTxt = root.querySelector('#out-txt'), picks = root.querySelector('#picks');
  var mail = root.querySelector('#out-mail'), svg = root.querySelector('.scene');

  function num(el, d) { var v = parseFloat(String(el.value).replace(',', '.')); return isFinite(v) ? v : d; }
  function fmt(v) { return (Math.round(v * 2) / 2).toLocaleString('it-IT'); }

  chips.forEach(function (b) {
    b.addEventListener('click', function () {
      chips.forEach(function (c) { c.setAttribute('aria-pressed', c === b ? 'true' : 'false'); });
      ear.value = b.dataset.v; update();
    });
  });
  ear.addEventListener('input', function () {
    chips.forEach(function (c) { c.setAttribute('aria-pressed', c.dataset.v === ear.value ? 'true' : 'false'); });
    update();
  });
  [tw, ft].forEach(function (el) { el.addEventListener('input', update); });

  function scene(E, T, F, H) {
    // 1 cm = 1.7 px, pavimento a y = 250
    var k = 1.7, fy = 250, X = function (cm) { return fy - cm * k; };
    var boxH = Math.max(T + 12, 28), standTop = X(H), boxTop = X(H + F + boxH), twY = X(H + F + T), earY = X(E);
    var seat = 45, seatY = X(seat), headR = 11;
    var s = '';
    s += '<line x1="10" y1="' + fy + '" x2="410" y2="' + fy + '" stroke="#2a1d14" stroke-opacity=".35"/>';
    // stand
    s += '<rect x="58" y="' + (fy - 6) + '" width="54" height="6" fill="#c9a774"/>';
    s += '<rect x="78" y="' + (standTop + 5) + '" width="14" height="' + Math.max(0, fy - 6 - standTop - 5) + '" fill="#d9bb8c"/>';
    s += '<rect x="60" y="' + standTop + '" width="50" height="5" fill="#c9a774"/>';
    // piedini + diffusore
    if (F > 0) s += '<rect x="64" y="' + (standTop - F * k) + '" width="6" height="' + (F * k) + '" fill="#8b7a66"/><rect x="100" y="' + (standTop - F * k) + '" width="6" height="' + (F * k) + '" fill="#8b7a66"/>';
    s += '<rect x="58" y="' + boxTop + '" width="54" height="' + (boxH * k) + '" rx="2" fill="#3b2a1e"/>';
    s += '<circle cx="85" cy="' + twY + '" r="5" fill="#e8d6b4"/>';
    s += '<circle cx="85" cy="' + Math.min(twY + 22, X(H + F) - 14) + '" r="11" fill="#5b4636"/>';
    // divano e ascoltatore
    s += '<rect x="300" y="' + seatY + '" width="100" height="' + (fy - seatY) + '" fill="#e6dccb"/>';
    s += '<rect x="372" y="' + X(85) + '" width="28" height="' + (X(seat) - X(85)) + '" fill="#d9ccb5"/>';
    s += '<path d="M340 ' + seatY + ' L340 ' + (earY + headR + 4) + '" stroke="#6f6254" stroke-width="16" stroke-linecap="round"/>';
    s += '<path d="M340 ' + (seatY - 2) + ' L300 ' + (seatY - 2) + ' L300 ' + fy + '" fill="none" stroke="#6f6254" stroke-width="12" stroke-linejoin="round"/>';
    s += '<circle cx="338" cy="' + earY + '" r="' + headR + '" fill="#6f6254"/>';
    s += '<circle cx="333" cy="' + earY + '" r="2.4" fill="#e8d6b4"/>';
    // linea di ascolto
    s += '<line x1="90" y1="' + twY + '" x2="327" y2="' + earY + '" stroke="#a87a2f" stroke-width="1.5" stroke-dasharray="5 4"/>';
    // quota stand
    s += '<line x1="40" y1="' + fy + '" x2="40" y2="' + standTop + '" stroke="#a87a2f"/><line x1="35" y1="' + standTop + '" x2="45" y2="' + standTop + '" stroke="#a87a2f"/>';
    s += '<text x="30" y="' + ((fy + standTop) / 2) + '" transform="rotate(-90 30 ' + ((fy + standTop) / 2) + ')" text-anchor="middle" font-size="12" fill="#a87a2f" font-family="Instrument Sans,system-ui,sans-serif">stand ' + fmt(H) + ' cm</text>';
    // quota orecchie
    s += '<line x1="418" y1="' + fy + '" x2="418" y2="' + earY + '" stroke="#6f6254" stroke-opacity=".6"/>';
    s += '<text x="338" y="' + (earY - headR - 8) + '" text-anchor="middle" font-size="12" fill="#6f6254" font-family="Instrument Sans,system-ui,sans-serif">orecchie ' + fmt(E) + ' cm</text>';
    svg.innerHTML = s;
  }

  function update() {
    var E = Math.min(Math.max(num(ear, 100), 60), 160), T = Math.min(Math.max(num(tw, 22), 3), 80), F = Math.min(Math.max(num(ft, 0), 0), 15);
    var H = E - T - F;
    if (H < 5) H = 5;
    outH.innerHTML = fmt(H) + ' <small>cm</small>';
    var lo = H - 5, hi = H + 3;
    outTxt.textContent = 'Va bene uno stand tra ' + fmt(lo) + ' e ' + fmt(hi) + ' cm: con qualche centimetro in meno il tweeter resta poco sotto le orecchie, ed è la situazione più naturale.';
    var list = STANDS.filter(function (s) { return !s.low; }).map(function (s) { return { s: s, d: s.h - H }; })
      .sort(function (a, b) { return Math.abs(a.d) - Math.abs(b.d); });
    var good = list.filter(function (x) { return x.d >= -5 && x.d <= 3; });
    var show = good.slice(0, 3);
    list.forEach(function (x) { if (show.length < Math.max(2, Math.min(3, good.length + 1)) && show.indexOf(x) < 0) show.push(x); });
    var html = '';
    show.forEach(function (x) {
      var tag = (x.d >= -5 && x.d <= 3) ? '<span class="ok">adatto</span>' : '<span class="d">' + (x.d > 0 ? '+' : '') + fmt(x.d) + ' cm</span>';
      html += '<li><a href="' + x.s.url + '"><img src="' + x.s.img + '" alt="" loading="lazy"><span><b>' + x.s.name + '</b><span class="d">' + x.s.note + '</span></span><span class="h">' + x.s.h.toLocaleString('it-IT') + ' cm<br>' + tag + '</span></a></li>';
    });
    if (!good.length) html = '<li class="d" style="font-size:.9rem;color:var(--muted)">Nessuno dei miei stand è nell\'altezza giusta: questi sono i più vicini. Posso costruirlo su misura.</li>' + html;
    if (H < 35) html = '<li><a href="stand-ground.html"><img src="images/ground-card.jpg?v=6" alt="" loading="lazy"><span><b>Extrasound Ground</b><span class="d">Stand bassi, per diffusori grandi o da pavimento</span></span><span class="h">24 cm</span></a></li>';
    picks.innerHTML = html;
    mail.href = 'mailto:info@fabrizioberlati.com?subject=' + encodeURIComponent('Stand su misura alto ' + fmt(H) + ' cm') +
      '&body=' + encodeURIComponent('Ciao Fabrizio,\n\nvorrei una coppia di stand alti circa ' + fmt(H) + ' cm.\n\nDiffusori (marca e modello): \nMisure della base del diffusore (larghezza x profondità): \nPeso di ciascun diffusore: \nEssenza preferita: \nCittà: \n\nAltezza orecchie ' + fmt(E) + ' cm, tweeter a ' + fmt(T) + ' cm dalla base' + (F ? ', piedini ' + fmt(F) + ' cm' : '') + '.\n');
    scene(E, T, F, H);
  }
  update();
})();
