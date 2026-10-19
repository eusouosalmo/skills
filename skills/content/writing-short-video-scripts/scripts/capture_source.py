#!/usr/bin/env python3
"""Capture a source page for the edit: the top of the page and the passage with the spoken claim marked in yellow.

usage: python3 capture_source.py URL OUT_PREFIX --highlight "text" [--highlight "text" ...] [--click "text" ...]

Writes OUT_PREFIX-topo.png (the page as it opens) and OUT_PREFIX-trecho.png (the first highlight about a third
from the top). Cookie banners, pop-ups, fixed bars and ads are removed before each shot, ad slots included, so no
empty "Publicidade" box is left in the print. --click opens a collapsed part first (a question in an FAQ).
Prints a JSON report. Exits 2 when a highlight is not on the page: the shot is then not proof of the claim, so look
at the page's text (its language may differ from the claim's) and run again with the words the page uses.
Needs python3 with playwright and its Chromium (pip install playwright && python3 -m playwright install chromium).
"""
import argparse, json, sys
from playwright.sync_api import sync_playwright

# Desktop width of the prints the author approved in a posted reel; 1400 px tall fits a headline and its lede.
WIDTH, HEIGHT = 1280, 1400

CLEAN = r"""
() => {
  const kill = '[id*="cookie" i],[class*="cookie" i],[id*="consent" i],[class*="consent" i],[id*="onetrust" i],'
    + '[class*="lgpd" i],[class*="modal" i],[class*="popup" i],[class*="newsletter" i],[class*="paywall" i],'
    + 'iframe,ins.adsbygoogle,[id^="google_ads" i],[id*="-ad-" i],[class*="ad-slot" i],[class*="adslot" i],'
    + '[class*="advert" i],[class*="publicidade" i],[id*="publicidade" i],[class*="banner-ad" i],[data-ad],[data-ad-slot]';
  document.querySelectorAll(kill).forEach(e => e.remove());
  // An ad slot often keeps only its label: a small box whose whole text is "Publicidade" or "Advertisement".
  const label = /^\s*(publicidade|advertisement|anúncio|anuncio|ads?|patrocinado|sponsored)\s*$/i;
  document.querySelectorAll('body *').forEach(e => {
    if (label.test(e.textContent || '') && e.querySelectorAll('p,h1,h2,h3').length === 0) {
      let box = e;
      while (box.parentElement && box.parentElement !== document.body && label.test(box.parentElement.textContent || '')) box = box.parentElement;
      box.remove();
    }
  });
  document.querySelectorAll('body *').forEach(e => {
    const s = getComputedStyle(e);
    if (s.position === 'fixed' || s.position === 'sticky') e.remove();
  });
  // What an ad leaves once its iframe is gone: a box with height and nothing in it (no text, no image).
  [...document.querySelectorAll('body div, body aside, body section, body figure')].reverse().forEach(e => {
    if (e.offsetHeight > 40 && !(e.textContent || '').trim() && !e.querySelector('img,picture,video,svg,canvas')
        && getComputedStyle(e).backgroundImage === 'none') e.remove();
  });
  // A pop-up also darkens the page behind it: its backdrop, or a filter or opacity set on the page itself.
  document.querySelectorAll('[class*="backdrop" i],[class*="overlay" i]:empty').forEach(e => e.remove());
  for (const e of [document.documentElement, document.body, ...document.body.children]) {
    e.style.filter = 'none'; e.style.opacity = '1';
  }
  document.documentElement.style.overflow = 'auto';
  document.body.style.overflow = 'auto';
}
"""

MARK = r"""
(phrase) => {
  const norm = s => s.replace(/\s+/g, ' ').toLowerCase();
  const target = norm(phrase);
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    const el = n.parentElement;
    if (!el || el.closest('script,style,noscript') || !el.offsetParent) continue;
    const i = norm(n.nodeValue).indexOf(target);
    if (i < 0) continue;
    const r = document.createRange();
    r.setStart(n, i); r.setEnd(n, Math.min(n.nodeValue.length, i + phrase.length));
    const m = document.createElement('mark');
    m.className = 'capture-mark';
    m.style.cssText = 'background:#ffe14d;color:inherit;padding:0 2px';
    r.surroundContents(m);
    return 'inline';
  }
  // The phrase crosses tags (a link or bold in the middle): mark the smallest block that holds it.
  const blocks = [...document.querySelectorAll('p,li,td,h1,h2,h3,blockquote,dd')]
    .filter(e => e.offsetParent && norm(e.textContent).includes(target));
  if (!blocks.length) return null;
  blocks[0].classList.add('capture-mark');
  blocks[0].style.background = '#ffe14d';
  return 'block';
}
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url"); ap.add_argument("out_prefix")
    ap.add_argument("--highlight", action="append", default=[])
    ap.add_argument("--click", action="append", default=[])
    a = ap.parse_args()
    report = {"url": a.url, "found": [], "missing": [], "files": []}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT}, locale="pt-BR")
        page.goto(a.url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)  # late banners and lazy ads arrive in the first seconds
        for name in ("Aceitar", "Aceito", "Concordo", "Accept", "Allow all", "Permitir todos"):
            try:
                b = page.get_by_role("button", name=name).first
                if b.is_visible(timeout=300):
                    b.click(timeout=1500); page.wait_for_timeout(500); break
            except Exception:
                pass
        for text in a.click:
            try:
                page.get_by_text(text, exact=False).first.click(timeout=5000); page.wait_for_timeout(1000)
            except Exception as e:
                report.setdefault("click_failed", []).append(f"{text}: {e.__class__.__name__}")
        page.evaluate(CLEAN)
        report["lang"] = page.evaluate("document.documentElement.lang")
        page.evaluate("window.scrollTo(0, 0)"); page.wait_for_timeout(300)
        page.screenshot(path=f"{a.out_prefix}-topo.png"); report["files"].append(f"{a.out_prefix}-topo.png")
        for h in a.highlight:
            (report["found"] if page.evaluate(MARK, h) else report["missing"]).append(h)
        if report["found"]:
            page.evaluate("""() => { const m = document.querySelector('.capture-mark');
                window.scrollTo(0, m.getBoundingClientRect().top + window.scrollY - window.innerHeight / 3); }""")
            page.wait_for_timeout(500)
            page.evaluate(CLEAN)  # scrolling can bring new ads and sticky bars
            page.screenshot(path=f"{a.out_prefix}-trecho.png"); report["files"].append(f"{a.out_prefix}-trecho.png")
        browser.close()
    print(json.dumps(report, ensure_ascii=False, indent=1))
    sys.exit(2 if report["missing"] or report.get("click_failed") else 0)

if __name__ == "__main__":
    main()
