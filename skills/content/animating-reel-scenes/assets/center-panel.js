// For top-panel split scenes: centre the drawing inside the 1080x960 panel, with equal space above and below
// and at least 170 px at the top, scaling it down when it does not fit. Wrap the drawing in <div id="grp">
// (position: absolute; inset: 0) and load this after the scene script. Scenes that repeat one drawing share
// one box, <div id="grp" data-box="top bottom">, measured on the fullest of them, so nothing jumps at the cut.
document.fonts.ready.then(() => {
  const g = document.getElementById('grp');
  let top = 1e9, bot = -1e9;
  if (g.dataset.box) [top, bot] = g.dataset.box.split(' ').map(Number);
  else for (const el of g.querySelectorAll('*')) {
    if (el.tagName === 'svg' || (el.closest('svg') && el.tagName !== 'path')) continue;
    const r = el.getBoundingClientRect(); if (!r.height) continue;
    top = Math.min(top, r.top); bot = Math.max(bot, r.bottom);
  }
  const h = bot - top, s = Math.min(1, (960 - 2 * 170) / h), c = (top + bot) / 2;
  g.style.transformOrigin = `540px ${c}px`;
  g.style.transform = `translateY(${480 - c}px) scale(${s.toFixed(3)})`;
  console.log('grp box', top.toFixed(1), bot.toFixed(1));  // copy into data-box for the scenes that repeat this drawing
});
