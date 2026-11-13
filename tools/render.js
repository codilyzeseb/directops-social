#!/usr/bin/env node
/* Render every .slide in an HTML file to a 1080x1350 PNG.

   node tools/render.js <slides.html> <out-prefix> [--preview <dir>]

   One slide   -> <out-prefix>.png
   Many slides -> <out-prefix>-1.png, <out-prefix>-2.png, ...
   --preview   -> also writes 390px-wide copies there, for the phone-size check.

   Uses the Chromium that ships with the cloud sandbox (require('playwright')).
   Fails loudly if a slide is not exactly 1080x1350, if text overflows a slide,
   or if a font did not load. */
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const [, , htmlArg, outArg, ...rest] = process.argv;
  if (!htmlArg || !outArg) {
    console.error('usage: node tools/render.js <slides.html> <out-prefix> [--preview <dir>]');
    process.exit(2);
  }
  const previewDir = rest[0] === '--preview' ? rest[1] : null;
  const html = path.resolve(htmlArg);
  const out = path.resolve(outArg);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  if (previewDir) fs.mkdirSync(previewDir, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 1 });
  await page.goto('file://' + html);
  await page.evaluate(() => document.fonts.ready);

  const problems = await page.evaluate(() => {
    const issues = [];
    const families = new Set();
    document.fonts.forEach((f) => { if (f.status === 'loaded') families.add(f.family.replace(/"/g, '')); });
    for (const need of ['Inter', 'Playfair Display']) {
      if (!families.has(need)) issues.push('font not loaded: ' + need);
    }
    document.querySelectorAll('.slide').forEach((s, i) => {
      const r = s.getBoundingClientRect();
      if (Math.round(r.width) !== 1080 || Math.round(r.height) !== 1350) issues.push(`slide ${i + 1} is ${r.width}x${r.height}`);
      if (s.scrollHeight > s.clientHeight + 1) issues.push(`slide ${i + 1} overflows vertically by ${s.scrollHeight - s.clientHeight}px`);
      if (s.scrollWidth > s.clientWidth + 1) issues.push(`slide ${i + 1} overflows horizontally by ${s.scrollWidth - s.clientWidth}px`);
      // nothing that carries text may sit inside the 3:4 grid-crop gutter or run off the slide
      s.querySelectorAll('*').forEach((el) => {
        if (!el.childNodes.length || ![...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim())) return;
        if (getComputedStyle(el).opacity === '0') return;
        const b = el.getBoundingClientRect();
        if (b.left < r.left + 40 || b.right > r.right - 40 || b.top < r.top + 40 || b.bottom > r.bottom - 40) {
          if (!el.closest('[data-bleed]')) issues.push(`slide ${i + 1}: text too close to the edge: "${el.textContent.trim().slice(0, 40)}"`);
        }
      });
    });
    return issues;
  });

  const slides = await page.$$('.slide');
  if (!slides.length) problems.push('no .slide found');
  const written = [];
  for (let i = 0; i < slides.length; i++) {
    const file = slides.length === 1 ? `${out}.png` : `${out}-${i + 1}.png`;
    await slides[i].screenshot({ path: file, type: 'png' });
    written.push(file);
  }

  if (previewDir) {
    const p2 = await browser.newPage({ viewport: { width: 390, height: 488 }, deviceScaleFactor: 1 });
    for (const file of written) {
      const b64 = fs.readFileSync(file).toString('base64');
      await p2.setContent(`<body style="margin:0"><img style="width:390px;display:block" src="data:image/png;base64,${b64}"></body>`);
      await p2.screenshot({ path: path.join(previewDir, path.basename(file).replace('.png', '-390.png')), clip: { x: 0, y: 0, width: 390, height: 488 } });
    }
  }
  await browser.close();

  written.forEach((f) => console.log('wrote', path.relative(process.cwd(), f)));
  if (problems.length) {
    console.error('\nPROBLEMS:\n- ' + problems.join('\n- '));
    process.exit(1);
  }
})();
