# news-image-20261124 — Tuesday 24 November 2026 in one image

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/c/news-image-20261124/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/meongs123/news-image-20261124/rank.svg)](https://make.fun/c/news-image-20261124/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/meongs123/news-image-20261124/reward.svg)](https://make.fun/c/news-image-20261124/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A make.fun bounty entry: a newspaper front page summing up the world's news
of **Tuesday 24 November 2026** — 44 stories, 7 regions, 13 drawn
illustrations, a dotted world map with numbered pins, one-line briefs, and a
DATE CHECK box naming the stories that are *not* 24 November news.

## The image

- Masthead: **Tuesday 24 November 2026**, with the count strip
  (44 stories · 7 regions · 13 illustrated), a numbers strip
  (Nvidia +31%, AWACS to Poland, 26 confirmed dead in Cikande,
  NPR 24,000-crore Nepal package, 11 killed in Dymer, Nikkei +3.9% /
  Tue: Nvidia -5% pre-market)
  and a segmented region bar (Americas 10 · Asia 10 · Europe 9 ·
  Africa 6 · Middle East 5 · World/Global 3 · Oceania 1).
- Lead stories: **Huang returns to Nvidia (+31%)**, **NATO sends AWACS
  to Poland**, and the **Russian jets that sparked a shelter alert off
  Ulleungdo** (Tuesday morning, genuinely 24 November news).
- 3 big + 10 small illustrated lead cards, a dotted world map with 13
  numbered pins, 31 numbered one-line briefs, and a red-bordered DATE CHECK
  box (COP31 collapse and Bisleri water ruling — Sun 22 Nov; Putin
  Article 5 report — 22–23 Nov; Hormuz tankers, PIF Tower, ICJ Rohingya
  verdict — Thu 19 Nov; BepiColombo Mercury arrival — Sat 21 Nov).
- Every picture is an original flat-vector drawing made in code. No
  photographs. Sources are tagged per story.

## Facts, frozen at build time (Tue 24 Nov ~20:15 WIB)

- Nvidia: **+31% Monday**, S&P 500 +4.7%, Nasdaq +6.4%; Huang reinstated
  11 days after resigning; the alleged link to a suspected Chinese
  intelligence asset is attributed, not stated as fact.
- Ulleungdo: Russian jets entered the Korea Air Defence Identification
  Zone (KADIZ) — **not sovereign airspace**; Seoul summoned Russia's
  defence attaché Col. Marchenko Tue; he gave no answer on intent.
- Cikande fire: **26 confirmed dead, ~30 missing** — toll rose Tue
  (was 24 Mon); 26 body bags await DNA ID.
- Nepal package: **NPR 24,000 crore** (wires split $1.62bn vs $1.63bn).
- Colombia car bomb: **12 hurt** (later El Tiempo report, not the first 5).
- Gaza: **1,675 killed since the ceasefire**, as attributed by the Gaza
  Health Ministry.
- Dymer: **final toll 11 dead, 5 in hospital**; search over Monday night.
- The IRGC claim of 2 destroyed Patriot radars, the claim that the
  Khartoum drones launched from Bahir Dar, Ethiopia, the China "Ma"
  spying case, and Putin's reported openness to Article 5-style
  guarantees are all **attributed, not stated as fact**.
- Gauteng coalition: **agreed in principle; signing pending** — not signed.
- US ports: a surge in cyberattack **attempts**, not breaches.
- No toll is decked for the El Chapo Isidro arrest shootout (wires
  split 11 vs 20).
- **Still developing at build time — freeze pass ~20:00 WIB Tue 24 Nov:**
  Cikande toll, IG Metall Tuesday strike, the Russian defence attaché
  summons, Hasina follow-up, Zelenskyy four-way talks, Champions League
  Tuesday results, Tuesday markets, COP31 aftermath.
- Do-NOT-write, kept out of the image: "Trump–Japan trade deal" and
  "Trump–Indonesia deal" (both July 2025); any "COP31 deal" — COP31
  collapsed Sunday 22 November.

## Files

- `main.ts` — the entrypoint (Node 22, stdlib only): copies `entry.png`
  to `/output/entry.png` and guards the PNG signature, the 1 MiB cap,
  the 1024×1024 size, and a byte-identical round trip.
- `entry.png` — the image (1024×1024), drawn by `compose.py`.
- `compose.py` — the deterministic renderer (PIL, no clock, no randomness,
  no network). It fails loudly instead of truncating: any headline, deck
  or brief that needs more lines than its box allows raises, and every
  illustration is audited to paint only inside its own box.
- `stories.py` — the 44-story slate with regions, fields and sources.

## Verify locally

```sh
python3 compose.py            # regenerates entry.png (deterministic)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see `LICENSE` (SPDX: MIT).
