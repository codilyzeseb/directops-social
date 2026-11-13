# directops-social

The working memory of the Direct Ops Instagram and Facebook routine, and the images it posts.

**This repository is public.** Nothing secret, personal or client-confidential belongs in it.

| Path | What it is |
|---|---|
| `CONTROL.md` | The switch: calibration, autopilot or paused. Questions for Sebastian and his answers |
| `STATE.json` | What has been made and queued, with Metricool ids |
| `PLAN.md` | The rolling two-week plan |
| `LOG.md` | One entry per run |
| `LEARNINGS.md` | What works, and the sources |
| `BRAND.md` | Voice, pillars, look, platform rules |
| `templates/` | The four HTML templates, one stylesheet, fonts |
| `posts/` | One folder per post: `slides.html` and `post.json` (captions, alt text, schedule) |
| `media/` | Rendered PNGs. Metricool reads them from the raw URLs |
| `bank/` | Real photos, clips and notes from Sebastian |
| `reports/` | The weekly review, `YYYY-WW.md` |
| `tools/` | `render.js` (HTML to PNG) and `lint.py` (the house rules) |

The PNG and MP4 files in the root are from the June 2026 posts. They are kept as they are.

## Making a post

```bash
cp -r posts/p001-late-arrival posts/p00N-slug        # or start from templates/
node tools/render.js posts/p00N-slug/slides.html media/YYYY-MM/p00N-slug --preview /tmp/preview
python3 tools/lint.py posts/p00N-slug
```

Then look at every PNG at full size and at 390px, read the caption aloud, commit, check each
raw URL answers 200 with an image type, and create the two Metricool entries.

Fonts are Inter and Playfair Display, under the SIL Open Font License (`templates/fonts/OFL-*.txt`).
