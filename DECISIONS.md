# Zach's decisions log

Every instruction Zach gives, dated, with where it was applied and whether it is settled.

**Why this file exists.** Zach, 2026-09-23: *"Lets make sure you are logging all my input so we
arent working in circles."* He asked for the sago palm line to be removed for a second time. It had
not been re-added — git shows `9e79f83` ("sago line out") removed it from `plants.html` and missed
the identical sentence on `landscape-installation.html`, which a different commit had put there.
One ask, two copies, half a fix, and it stayed broken for two days without anyone noticing.

**How to use it.**
- Read this file at the start of a session, before touching content.
- Add an entry when Zach gives an instruction, **before** acting on it, and quote him.
- When a decision is reversed, do not delete the old entry — strike it and link the new one. The
  history is the point; three of these reversed within a single day.
- **A page is not a fix.** Before marking anything Done, `grep -rn "<the string>" site-build/*.py` —
  the generators are what quietly put content back. This has now caused the same bug three times
  (sago, the West Ashley ceiling, the Sullivan's Island photo).

Newest first.

---

## 2026-09-23

| # | Zach said | What was done | Status |
|---|---|---|---|
| 27 | *"use logo B and fix the issues the audit has found"* | **Logo B is live** as the WordPress Site Icon (attachment 7418). Audit: 32 confirmed, 12 rejected on verification. **Done so far:** the trailing-slash cache regression (swapping visitors' tracking params); all 11 project breadcrumbs, which said "Home / Summerville" because a regex stopped matching after the markup changed; "Isle Of Palms" capital O; the free-consultation promise on 22 pages; mobile price tables clipping. **Still open:** /thank-you/ (every lead lands on the one page never rebuilt), the trust strip on 1 of 77 pages, the Johns Island page publishing a James Island job, /favicon.ico 404, and the accessibility / performance / tech-SEO tails. | **Partly done** |
| 26 | *"you can add some planting requirements for the kiawah page. Kiawah requires a certain amount of plants around the foundation of the house and yard and they require them to be a certain size. See if you can research that for specific"* | Read the governing document directly — the ARB's *Designing with Nature* (2026 edition), 82pp, from arb.kiawahisland.com. Added a "How Much You Have to Plant, and How Big" block with the real numbers: one 3"+ caliper tree per 1,000 sq ft of lot (palms count as a third) plus 70% of existing trees; two-thirds of new trees native and anything counted toward the minimum native and 4"+ caliper; foundation shrubs at half the foundation height or 4 ft, whichever is greater, wrapping the whole building; 50% of shrubs 7-gallon minimum and the rest 3-gallon; double evergreen screening; lawns 10 ft off property lines. **Also corrected a live error** — the page said oaks of 24 inches are preserved. 24 inches is the size at which an oak must be highlighted in red on the submitted survey; the preservation threshold is 16 inches, and approval is needed to touch any oak of 3 inches or more. `kiawah_planting.py`, generator patched too. | **Done, live** |
| 25 | *"send me the two logo options"* | Sent. A = emblem on the dark green badge (already in the sandbox as favicon-512.png), B = emblem on white, both 512px, plus the live one for comparison. Confirmed the live site icon measures chroma 0.0 / luminance 229 at 18% opacity - a white logo on transparent, invisible on Google's white results page - and /favicon.ico 404s. | **Waiting on Zach to pick** |
| 24 | *"you can add a detail for the game day pergola and potentially the pergola page if it fits. We inset the rafters between the beam making the ceiliing taller and providing a more modern look."* | Added to the Game Day project page (prose + spec list) and to `/pergolas/` in the Covered Pergolas section, which links the Game Day page as the worked example. Checked against the photo first: flat fascia, no projecting rafter tails. Generators `project_pages.py` and `pergola_split.py` patched in the same pass. `inset_rafters.py`. | **Done, live** |
| 23 | *"remove the 'we do not plant sago palms' text. We have done this before and i think youve readded it."* | Removed from `landscape-installation.html` and from its generator `page_landscape_installation.py`. Not re-added — `9e79f83` removed only the `plants.html` copy. `sago_out.py`, whose check fails if the word reappears on any page or in any generator. | **Done** |
| 22 | *"Lets make sure you are logging all my input so we arent working in circles"* | This file. | **Done** |
| 21 | *"can you make the video on the homepage not stutter so much in the first clip"* | Only that clip is 24 fps; the rest are 30 or 29.75. `fps=30` ran *before* motion interpolation, padding 24&nbsp;&rarr;&nbsp;30 by duplicating one frame in five; the interpolator then read zero motion across each duplicated pair. Now conformed by a motion-compensated pass instead. Measured unevenness of frame-to-frame motion in the finished file: **CV 0.537 &rarr; 0.222**, and the coarse 10-frame beat became the 2-frame alternation every other clip already has (a 30&nbsp;fps clip measures 0.197). `hero_video.py` v10. | **Done, live** |
| 20 | *"the beadboard ceiling was a cost decision"* | Restored as a saving on `/pergolas-pavilions/`, `/west-ashley-sc/` (body + FAQ JSON-LD) and `/project-west-ashley-pool-cabana/`, plus generators `town_pages.py` and `project_pages.py`. Ceiling and floor now given as two savings, not one blurred sentence. `ceiling_saving.py`. | **Done, live** |
| 19 | *"go ahead with the trailing slash fix"* | `trailing_slash.py` patches `deploy_shell.py` (backup first — that file has no version control and renders all 77 pages). Verified live: six pages now 301 to the slashed form, slashed forms still 200 with no loop, `/wp-json/` untouched, 404s still 404, robots and sitemap untouched, `.well-known` excluded, and **POST to /contact-us still returns 200** — a 301 there would have dropped form leads. **Regression found and fixed the same day:** LiteSpeed caches the 301 keyed on PATH ONLY, so the first visitor's query string was being served to everyone after them — `/about?gclid=BBB` returned `Location: /about/?gclid=AAA` on a cache hit, silently reassigning one ad click to another. Reproduced, then fixed by marking the redirect no-cache. Re-verified: four different tracking params now each come back with their own. | **Done, live** |
| 18 | *"its beadboard sheets"* | The West Ashley cabana ceiling. Corrected across 4 pages, `photos.json`, `PROJECT-NOTES.md:1090` and **six generators** — four of which would have silently restored the old wording. `beadboard.py`. | **Done, live** |
| 17 | *"the homepage video is glitching now"* | Not a delivery or performance problem — 0 dropped frames of 1401. The file faded out to black and back in, so the hero went black ~1.5s every 38s. Loop point is now the same 1.2s crossfade as every other cut; first frame equals last. `hero_video.py` v9. | **Done, live** |
| 16 | Six answers: fences/gates yes but not pushed; pool-deck photo *"your call"*; *"many diffrent photos of that stucco wall"*; *"The kitchen has the porch addition over it with the clear roof"*; form title yes; jasmine line yes | `about_fences.py`; pool-deck hero kept (only 1600-wide hero-shaped shot of that job); retaining-walls hero swapped to the driveway view; Pitmaster's Kitchen photo confirmed correct; WPForms 1123 title → "Tell us about your project". | **Done, live** |
| 15 | *"use a fleet to knockout the entire audit. Ignore the searchxpro offboarding stuff."* | 87 verified edits. Also fixed two of my own regressions found by the fleet: a duplicate `BreadcrumbList` on 73 pages, and a pool-deck H1 rewritten into a title tag. | **Done, live** |
| 14 | Vines, iteratively: trellis/vines work with pergolas → *"we do build trellis supply and plant vines the carolina jasmine is the most popular"* → integrate into `/plants/` → *"confederate jasmine might be more popular but i dont think it really matters"* → tree damage with verified research → spacing/layering + the Japanese maple example | "Vines and Climbers" and "Spacing and Layering" on `/plants/`. Neither jasmine is ranked. Horticulture cited from Clemson HGIC, NC State Extension, Missouri Botanical Garden, PSU and UMD Extension, Morton Arboretum. | **Done, live** |
| 13 | *"the covered pergolas and metal roof section needs a photo"* / *"A gazebo sits closer to a pergola in scale... doesnt necessarily fit the text block"* / pergola and pavilion maintenance facts / *"some structures being more finished with roof and kitchen and others being open but more tied into the garden"* | Pergola and pavilion pages split into two distinct pages; gazebo line dropped; roof/finish and engineer-drawing facts added. | **Done, live** |
| 12 | *"leave the video"* (after seeing trim and speed examples) | No change to length or speed. Superseded for a different reason by #17 and #21, which fix defects rather than re-cut it. | **Settled** |
| 11 | *"go ahead with lite speed guest mode, can we just rename and re use searchxpro container, you can drop recaptcha but we had issues with spam in the past, keep the first 4 parts of the video... schedule handling the cache mobile"* | Guest Mode, reCAPTCHA off (modern anti-spam left on). Cache-mobile delegated to the daily-index session: **stays off**, because the site does no server-side device branching. | **Done** |
| 10 | *"fix the title on the concrete page too and the mobile menu is still off to the side"* | Mobile Services panel centred without depending on `transform` (a `:hover` rule was overriding it on tap). Concrete and pool-deck titles fixed. | **Done, live** |
| 9 | *"add outdoor showers... driveways goes to the concrete page should those match... water features are higher priority... it doesnt fit on mobile so center the drop down"* | Services dropdown. | **Done, live** |

## 2026-09-23 — indexing, off-boarding and Drive (daily-tasks session)

Separate workstream, so lettered rather than numbered to avoid colliding with the content log above.

| # | Zach said | What was done | Status |
|---|---|---|---|
| D9 | *"When i google cramers landscaping the website link either shows up a blank logo or our logo is black and white. Also can we make sure the text descriptions are good."* | **Logo is a real defect:** the site icon is a *white* logo on a transparent background — measured chroma 0.0 (no colour at all), luminance 229/255, 81% transparent. White on Google's white results background renders as nothing; confirmed on the live SERP as a blank circle. Two 512px replacements cropped from the colour emblem in `photos-inbox/archive/logo_no_background.png` (transparent and white-backed) sent to Zach. **Descriptions need no work** — sampled 12 pages, all 136–160 chars, specific, no duplication. What Google *displays* is its own stale snippet ("premier…"), from the 21 Sep crawl, and clears on re-crawl. | **OPEN — waiting on Zach to pick an icon**, then set as WordPress Site Icon + add a root `/favicon.ico` (currently 404) |
| D8 | *"yes bump it to tomorrow"* | `/project-west-ashley-pool-cabana/` out of tonight's batch — crawled 22 Sep and already indexed, so a rationed slot was better spent on a blog Google has refused to index since July. Added `indexing.py defer URL DATE`, which **clears itself** on the date, rather than reusing `hold` (a forgotten hold keeps a page out of the queue forever). | **Done** |
| D7 | *"collapse it to one hop"* | `/tree-shrub-trimming/` was `→ /landscape-maintenance/ → /plants/`. Now a single 301 to `/plants/` (Redirection rule id 22). All 24 enabled rules verified single-hop. | **Done, live** |
| D6 | *"yeah fill the last three with those blogs or location pages that need indexing"* | Checked every location page first: 11 of 12 are indexed and were crawled post-rebuild; the only one needing indexing, `/folly-beach-sc/`, was requested 22 Sep and is inside its 5-day cooldown. So the three slots went to the oldest not-indexed blogs. | **Done** |
| D5 | *"Switch the non indexed blogs to tomorrow and lets get the high priority service pages reindexed first"* | Reversed D4's ordering: `rank()` now sorts **priority first**, then not-indexed, then oldest crawl. Money pages re-crawl before blog posts. | **Done** |
| D4 | *"prioritize pages that arent indexed or hasnt been crawled since we completly redid the website"* | Half was already enforced — `done()` only counts a page finished if crawled after the 2026-09-20 flip **and** indexed. Added ordering by not-indexed, and `indexing.py recrawl` so a page whose content changed can re-enter the queue **without clearing its `requested` stamp**. Superseded next by D5. | **Superseded by D5** |
| D3 | *"You can rerequest those three"* (`/about/`, `/concrete-pool-decks/`, `/west-ashley-sc/`) | Two of the three had **not** been crawled since the rebuild (9 and 16 Sep), so they were already queue-eligible and in cooldown until the 27th. Only `/west-ashley-sc/` needed a flag. | **Done** |
| D2 | *"grab the brand assets and strategy documents too"* then *"grab the luxurious renovations folders too but put it into the LR session database"* | Brand assets and strategy links were **not** in the e-mail — they were hyperlinks inside the .docx, recovered by unzipping it and reading `word/_rels/document.xml.rels`. Cramers: 86 files total. LR: 41 files, with its record filed in the LR project, not here. **The February 2026 photos are stock, not Cramers work** (Drive's own captions; the outdoor-kitchen one is a 3D render) — check before any page reuses them. | **Done** |
| D1 | *"log all of the relevant info mostly all the past blog posts"* | `tracking/data/searchx-offboarding-email-2026-09-23.md` — month-by-month inventory of everything SearchX produced, reconciled against the 22 live posts. Seven drafts were written and never published. Their off-boarding document **e-mails the `seo@searchxpro.com` WordPress login password in plain text**; rotate it when reclaiming user 1. Their Google access checklist is entirely unticked. | **Done** |

**Note on the standing rule below.** "Do not touch the SearchXPro offboarding" still holds for *access
revocation* — Zach owns that. It does not cover the archive work in D1–D2, which he directed himself after
their off-boarding e-mail arrived.

## Earlier — backfilled from git, 2026-09-20 to 09-22

Partial. Reconstructed from commit messages, which quote Zach but were not written as a log, so
treat entries below as a pointer to the commit rather than a verbatim record.

| Date | Zach's input, as recorded | Commit |
|---|---|---|
| 09-22 | Follow-up answers: shower price, non-refundable rule, Doug's two numbers, design fee | `ce9b9a4` |
| 09-22 | Answers: Doug's number only, trip-charge towns, sod watering, Doug's tenure, address labels | `6806c2b` |
| 09-22 | Game Day Backyard is the builder landscaping rework; Doug is 30+ years of experience | `3b36383` |
| 09-22 | Outdoor showers need no permit | `e891054` |
| 09-21 | Corrections batch 1, incl. **sago line out** (only half applied — see #23) | `9e79f83` |
| 09-21 | Town pages from real jobs, neighborhood rules, James and Daniel Island | `8ab0f32` |
| 09-21 | Strip leftover maintenance, mowing and rental-maintenance claims | `a95feb9` |
| 09-21 | Photo-by-photo answers behind the portfolio project stories | `7b7218b`, `e4e5bb5` |
| 09-21 | Ideas post: fountain reason in Zach's words; invented pool-deck claim out | `02b3192`, `265d57a` |

---

## Standing rules

Not one-off decisions — these apply to everything.

- **Never invent facts.** Content uses only what Zach or Doug supplied, or already-published copy.
  General horticultural and regulatory facts may be cited from reputable sources, named in the
  script that adds them. He spots filler ("the paving stopping at the posts").
- **843-709-6140 is Zach's personal mobile and must never appear on the site.** Doug's
  (843) 614-9773 is the public number.
- **No maintenance or mowing claims**, and nothing implying a maintenance service.
- **No unsupported superlatives** ("Charleston's trusted name").
- **Free consultations are geography-qualified** — free around Charleston, Mount Pleasant and
  Summerville; a trip charge beyond, non-refundable, deducted from the build.
- **App passwords yes, login passwords never.**
- **Do not touch the SearchXPro offboarding** — Zach's explicit instruction. Reclaim WordPress user
  1, never delete it.
- **`site-build/` is NOT under version control.** It is a sibling of this repo, not inside it. No
  undo. Back up before editing `deploy_shell.py`, which renders all 77 pages.
