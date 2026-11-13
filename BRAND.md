# BRAND

How Direct Ops sounds and looks on Instagram and Facebook. Read it before writing anything.

## Who we are, who we talk to

Direct Ops installs and runs an AI front desk for villas, hotels and resorts with up to about
100 keys, in Switzerland, the EU and the UAE. It answers guests day and night, in their language,
on the website, WhatsApp, Booking.com and Airbnb, and only from what the operator has told it.
Complaints and refunds go straight to a person. It is live today at properties in Thailand and Italy.

We talk to the person who owns the phone at night: the owner, the general manager, the family
running fifteen rooms. They are not looking for software. They are tired of the Wi-Fi question.

## Voice

Write as someone who has stood behind a front desk, not as a company describing a product.

- **Start in the building.** A time, a room number, a guest with a late flight. The product comes
  second, or not at all.
- **Short and warm, a little informal.** Contractions are fine. One idea per post.
- **Specific over impressive.** "No hot water in room 7" beats "urgent guest issues".
- **Say what it does not do.** It hands complaints to a person. It only knows what you told it.
  Saying so is what makes the rest believable.
- **Ask plain questions.** "Which message wakes you most often?" End most posts on one.
- **Vary the shape.** Never the same template twice in a row, never three captions of the same length.
- **Sign "Sebastian, Direct Ops" only on a note he wrote** in `bank/notes.md`.

Read every caption aloud once. If a sentence sounds like an advert, it is one. Cut it.

| Like this | Not like this |
|---|---|
| 23:40. A guest's flight is delayed. | In today's fast-paced hospitality world |
| It answers from what you've told it. | Our intelligent solution uses your data |
| That one goes to a person. | Smart escalation workflows |
| Which message wakes you most often? | Ready to transform your guest experience? |

## Words

**Always:** AI front desk, the desk, proposal, free AI audit, keys, guests, operators.

**Never:** quote (say proposal), chatbot, bot, AI agent, cheap, beta, no obligation,
guaranteed results. No "Imagine". No game-changer, revolutionise, unlock, seamless, elevate,
cutting-edge. No em dashes. No exclamation marks. No prices. No model or vendor names.

**German:** the "Sie" form, always. Swiss spelling, as on the German landing page (ss, never ß:
"grösser", "schliessen"). KI-Front-Desk, kostenloses KI-Audit, Festpreis-Angebot, Einheiten, Gäste.
Never "Kostenvoranschlag", "unverbindlich", "garantiert". German has to read as written by a
native hotelier, not translated: write it fresh from the idea, don't translate the English caption.

## Truth

- Never invent a client, a number, a result, a testimonial, a review or a quote from a person.
- Example conversations carry the "Example" label on the image and say so in the caption.
- An industry fact needs a source opened and read that day, and a dated line in `LOG.md`.
  Candidates wait in `LEARNINGS.md` section 5.
- Behind-the-build posts use only what is in `bank/notes.md` or already public on directops.ai.
- Never use a live property's chat or website to make content.

**Properties we may name:** none on file yet. Until Sebastian lists a written OK here, write
"a beach villa resort in Thailand", "a private villa in Thailand", "a villa near Rome".

| Property | Written OK | Date | Notes |
|---|---|---|---|
| (none yet) | | | |

## Pillars

| Pillar | Share | What it is | Usual template |
|---|---|---|---|
| The desk at work | about 40% | One guest moment and the answer the desk gives. Always labelled "Example" | Chat card, night log |
| The operator's night and day | about 20% | The 30 questions, commissions, slow-reply reviews. The problem, then the relief | Night log, statement |
| Behind the build | about 15% | What we shipped, told simply. Only from `bank/notes.md` or public facts | Statement |
| Practical tips | about 15% | Checklists and templates operators save | Checklist carousel |
| The offer | about 10% | The free AI audit. At most one post in four is a direct ask | Statement |

The split moves with the data, in the Monday review. The current split lives in `STATE.json`.

## Formats

- **Carousel** (3 to 8 slides) for teaching and anything worth saving.
- **Single image** for one sharp idea.
- **Real photos and screenshots** from `bank/` whenever they fit. They come first.
- **Reels** only when `bank/` holds real video. Never stock footage, never generated people or places.
- If a generated image is ever used, the post is flagged `isAiGenerated: true`. So far: never.

## Look

Navy is the room, porcelain is the page, brass is the jewellery. Calm, premium, hospitality.
No robots, no glowing brains, no neon, no gradients doing a show.

| Token | Hex | Use |
|---|---|---|
| Navy | `#1F1B4F` | Dark slides, desk bubbles |
| Porcelain | `#F6F4EF` | Light slides |
| Brass | `#BF9F66` | Numerals, rules, one word in a navy headline |
| Brass ink | `#6D521F` | Eyebrows and small labels on light slides |
| Slate | `#5B6670` | Body text on light slides |

- **Type:** Playfair Display for statements, times and numerals. Inter for everything functional.
- **Canvas:** 1080 x 1350. Keep 88px clear left and right: the profile grid crops to 3:4.
- **Smallest text:** 26px for labels, 34px for anything meant to be read on a phone.
- **Brass** is never body text, and at most one word per headline.
- **Wordmark:** the mark, then "Direct" with "·Ops" in brass, bottom left of every slide.
- **Alternate** light and dark from post to post so the grid reads as a set, not a wall.

### The four templates

All in `templates/`, all styled by `templates/base.css`. Each file opens with its own rules.

1. **`chat-card.html`** Porcelain. A clock, two lines of Playfair, one conversation in a white card,
   a brass line showing what the team sees afterwards. The "Example" pill never comes off.
2. **`statement.html`** Navy. One idea in Playfair, one brass word, a short supporting paragraph.
3. **`checklist-carousel.html`** Porcelain with a navy close. A numeral cover, two items a slide,
   an optional "Copy this" card. Built to be saved.
4. **`night-log.html`** Navy or porcelain. Five times down the left, five messages, one of them
   marked for a person.

Render: `node tools/render.js posts/<id>-<slug>/slides.html media/<yyyy-mm>/<id>-<slug> --preview <dir>`.
It refuses a slide that overflows, sits too close to the edge, or lost its fonts.
Refresh one template every four weeks so the feed never looks machine-made.

## Platform rules

**Instagram**
- At most five hashtags in total, counting the first comment. We use three or four, in the first comment.
- No links in captions. "Link in bio" sparingly: about one post in four.
- Alt text on every image.

**Facebook**
- No hashtags by default, two at most.
- One direct link per post, with UTM. In the caption on at most two posts a month, in the first
  comment otherwise (see `LEARNINGS.md` section 3, Facebook).
- Link format, English: `https://systems.directops.ai/?utm_source=facebook&utm_medium=organic&utm_campaign=social_autopilot&utm_content=<post-id>`
- German posts link to `https://systems.directops.ai/de` with the same parameters.

**Metricool**
- Brand `getdirectops`, blogId 6353442, timezone Asia/Dubai. No other brand, ever.
- Each post is two entries at the same minute, one for Instagram and one for Facebook, because the
  two captions and first comments differ. `STATE.json` holds both ids under one post id.
- Never a boost field. Never an account setting. Never delete a published post.

### Hashtag sets

Pick three or four. Rotate; never the same four twice running.

| Pillar | English | German |
|---|---|---|
| The desk at work | #hoteliers #boutiquehotels #villamanagement #guestexperience #frontdesk | #hotellerie #gastgeber #ferienvermietung #gästeerlebnis |
| Night and day | #hoteliers #frontdesk #hospitalitymanagement #independenthotels #hotellife | #hotellerie #hotelalltag #gastgeber #rezeption |
| Behind the build | #hoteltech #hospitalitytech #hoteliers #independenthotels | #hotellerie #hoteltechnologie #digitalisierung |
| Practical tips | #hoteliers #hotelmanagement #holidayrentals #guestexperience #directbookings | #hotellerie #hotelmanagement #ferienwohnung #direktbuchung |
| The offer | #hoteliers #hotelmanagement #boutiquehotels | #hotellerie #hotelmanagement #gastgeber |

### Call-to-action lines

Soft (most posts):
- Which message wakes you most often?
- How do late arrivals reach you today?
- What's in yours that isn't on this list?
- Save it for the next time you rewrite yours.

Facebook link lines:
- You can put the same question to the live desk yourself: [link]
- This is the front desk we install and run with small properties. You can ask it something here: [link]
- We set up and run front desks for small hotels, villas and resorts. More here: [link]

Direct (the offer, at most one post in four):
- The free AI audit is a 30-minute call. The written report and a fixed-price proposal follow within 24 hours.
- Instagram: The audit is free. Link in bio.

German:
- Welche Nachricht weckt Sie am häufigsten?
- Das kostenlose KI-Audit: ein Gespräch von 30 Minuten, danach ein schriftlicher Report und ein Festpreis-Angebot innerhalb von 24 Stunden.

## Before anything is queued

1. Every image opened at full size and at 390px wide. Readable, nothing cut off, on brand.
2. Caption read aloud. Human, specific, no advert sentences, no typos. German at native level.
3. `python3 tools/lint.py posts/<id>-<slug>` passes with no errors.
4. Every claim has a checked source, or there is no claim.
5. If any of it fails: fix it, or don't post it.
