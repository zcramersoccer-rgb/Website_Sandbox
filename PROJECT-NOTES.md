# Project notes — read this first

Internal working notes for the sandbox rebuild. Not part of the site.
The whole sandbox is `Disallow: /` in `robots.txt` and every page carries
`noindex`, so nothing here is public.

**Keep this file updated at the end of every working session.** Anything that
only exists in a chat window is gone the next day — that is how we lost Zach's
interview answers and the first round of Semrush research.

---

## Where things stand — updated 2026-09-19

### ⚠️ The branch trap

**Work on `Site-revamp`.** A fresh session may start you on a stale or deleted
branch and everything will look like it vanished. First command of any session:

```
git fetch origin --prune && git checkout Site-revamp && git pull
```

**Published 2026-09-19.** `main` was fast-forwarded to `Site-revamp`, so the two
are identical and the live sandbox now shows all of this work, hero video
included. Before that, `main` had been frozen at the 2026-09-15 Divi replica with
no video files at all, 53 commits behind.

Keep publishing the same way — it stays a clean fast-forward as long as nothing
commits directly to `main`:

```
git checkout main && git merge --ff-only origin/Site-revamp && git push origin main
```

The sandbox is safe to publish at any time: `robots.txt` is `Disallow: /` and all
60 pages carry `noindex`. Check both still hold before each publish. Note that
this file is served publicly too (crawlers are blocked, but the URL is reachable),
so keep anything genuinely sensitive out of it.

### What's done

- Full static replica: 39 pages + 21 blog posts, no JavaScript beyond the chat widget
- Homepage rebuilt (hero video, trust strip, family intro, service tiles, featured projects)
- Portfolio curated 192 → 51 photos, grouped by service
- All images local WebP, self-hosted fonts, one minified stylesheet per page
- **`outdoor-kitchens.html` and `summerville-sc.html` rewritten from Zach's answers** — these are the quality bar
- `pergola-pavilion-installation-charleston-sc.html` re-aimed at "pergola vs pavilion" (2026-09-19)
- **Hero video finished (2026-09-19)** — see "Hero video" below

### What's next

Rewriting every service page one at a time, in the house pattern below, from
Zach's answers. **Currently mid-interview on Pergolas & Pavilions** — questions
are in the section at the bottom of this file, awaiting answers.

---

## Hero video — done

`assets/video/hero-1080.mp4` + `hero-720.mp4`, v4 cut, 37.2s silent loop.
Fades in from black and out to black, so the loop is a clean symmetric
fade-through-black. Poster is the opening frame (t=1.5s).

**Fixed 2026-09-19:** the encode was tagged `bt2020nc / arib-std-b67` (HLG HDR)
from the iPhone source. Any browser that does not tone-map HLG was showing it
badly desaturated — measured mean saturation 16.8 untagged vs 29.6 tone-mapped,
so roughly 75% of the colour was being lost. Re-encoded to proper bt709 SDR.

| File | Before | After |
|---|---|---|
| hero-1080.mp4 | 8.59 MB, bt2020 HLG | 8.42 MB, bt709, cropped, shot 2 swapped |
| hero-720.mp4 | 4.21 MB, bt2020 HLG | 4.23 MB, bt709, cropped, shot 2 swapped |
| hero-poster.webp | 207 KB | 189 KB, colour- and crop-matched |
| hero-poster.jpg | 347 KB, unreferenced | deleted |

Recipe, if it ever needs redoing from the HLG master:

```
-vf "zscale=t=linear:npl=100,tonemap=hable,zscale=p=bt709:t=bt709:m=bt709:r=tv,format=yuv420p"
-c:v libx264 -preset slow -crf 33 -pix_fmt yuv420p
-colorspace bt709 -color_primaries bt709 -color_trc bt709 -movflags +faststart -g 60
```

**Use `tonemap=hable` with its default desaturation.** `desat=0` was tried and
throws a magenta cast — white siding and pavers turn pink. Verified frame by frame.

### Person removed from shot 3 (2026-09-19)

A man in a grey t-shirt and white shorts, dragging a hose, walks out along the
**left edge at the start of shot 3**, visible from the shot-2 dissolve at
t≈15.0 until t≈17.8. He is in every cut from v4 back.

He never reached further than **x≈110 of 1920** (under 6% of frame width), so
instead of losing ~4s of footage he was cropped out with a small asymmetric
punch-in, all taken off the left:

```
crop=1760:990:160:45,<tonemap chain>,scale=1920:1080
```

1760x990 is exactly 16:9, so there is no distortion. That is a 9.1% punch-in,
applied to the whole video for uniform framing — checked shot by shot, nothing
of value is lost at any edge. Full duration and both dissolves are preserved.

Re-encoded from the **v4 HLG master** (`git show c3923cd:assets/video/hero-1080.mp4`),
with crop, tone-map and encode in one pass, so it is still only one generation
off the master rather than two. Poster regenerated with the same crop so it
matches the video behind it.

### Shot 2 replaced — fire bowls (2026-09-19)

The Mount Pleasant pool pavilion shot was visibly soft: sharpness 13.89 against
20.91 for the pergola opener, with smeared fence boards and chairs at 1:1. It
looked upscaled from a smaller source. Replaced with the travertine pool and
fire-bowl footage from the **v1 cut** (`git show 2e296d5:assets/video/hero-1080.mp4`,
t=8.6-13.9), which measures 15.32 and brings colour, flame movement and a
different property.

The reel runs at half speed, so the v1 clip was slowed 2x with motion
interpolation to match (`setpts=2*PTS,minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1`)
— about 100s to render 10.5s at 1080p.

Assembled in one pass from the v4 master plus that clip: shot 1 (master 0-7.2),
fire bowls, then shots 3-5 (master 16.2-37.2), joined with 1.2s crossfades to
match the existing dissolves, then cropped and tone-mapped. Runs 36.3s, down
from 37.2s. Files came out slightly larger (7.75 -> 8.42 MB) because flames and
moving water are expensive to encode.

Dissolve boundaries in the v4 master, if this needs redoing:
shot1->2 spans 7.3-8.6, shot2->3 spans 14.6-16.0.

**Current shot order:** pergola -> pool + fire bowls -> blue-house kitchen ->
putting green patio -> porch fireplace.

⚠️ **There is no pavilion shot in the hero any more.** Pavilions are the
highest-ticket service ($30-90k+), so this is worth filling.

### Footage wanted

- **Golden hour cabana video** — Zach is shooting this (mentioned 2026-09-19).
  Strong candidate to go back into the hero, and the obvious fix for the missing
  pavilion coverage. The West Ashley cabana is the flagship project (haint blue
  vaulted ceiling, cedar posts, TV wall).

**Lesson for checking footage:** he was missed on the first pass because contact
sheets were tiled at ~330px wide, where a figure at the extreme frame edge is a
few pixels and blends into the tile border. When checking for people, scan the
left and right 400-500px strips separately at high magnification, not just
full-frame thumbnails.

### Things tried that did NOT help

- **VP9 / WebM** — came out *larger* than H.264 (crf 36 ≈ 11 MB vs 8.6 MB). The
  cut is a half-speed interpolated recut, and the synthetic in-between frames
  compress badly. Not worth a second source.
- **Dropping frame rate** 30 → 24 or 20fps — saved only ~4%. x264 already encodes
  near-duplicate interpolated frames almost for free.

The existing encode was already efficient; there is no free size win left. Going
below ~8.3 MB at 1080p means visible quality loss (crf 34 ≈ 6.6 MB) or a shorter
cut. **Shortening from 37s to ~20s is the only large saving available, and that is
an editorial call — ask Zach.**

### Note for testing

Playwright's bundled Chromium has no H.264 decoder (`canPlayType('avc1')` is
empty) and the bundled ffmpeg is `--disable-everything`. Neither can play the
hero video. Install a real one for video work:
`npm i ffmpeg-static` in the scratch dir. Do not mistake either for a site bug.

---

## How to view the site locally

```
python3 -m http.server 8099      # then open http://127.0.0.1:8099/index.html
```

Chromium is at `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` for
screenshots via Playwright (install into a scratch dir, not the repo).
Full-page screenshots taller than ~8000px fail to upload — split them in two.

---

## The house pattern

Reverse-engineered from `outdoor-kitchens.html`. Every service page should have:

1. Specific H1 + short eyebrow line
2. Opening: what it is, that Cramers builds it in-house, Doug and Zach named
3. "Where most start, and what people add" — the real common build + popular additions
4. "Materials that last on the coast" — real brands and honest tradeoffs
5. **"The details that matter later"** — hard-won advice. This is the section that
   makes a page feel like a person wrote it. On the kitchens page it is the
   range-hood-and-grease explanation and the built-in-trash-can-attracts-rats warning.
6. One real project told in specifics (the sapele wood foot rail, the second fan in Summerville)
7. Real price table
8. Numbered process with real timelines
9. Cross-links to related services + service areas
10. FAQ with `FAQPage` JSON-LD schema

**Never invent** a price, timeline, brand, material or project story. If it did
not come from Doug or Zach, it does not go on the page.

---

## SEO strategy

Agreed model: **service pages must not compete with each other.** Blog posts may
repeat service-page content, but each must go deeper on one specific question
and link back up to its service page.

### Semrush findings (re-run 2026-09-19, `us` database)

Local money terms are nearly empty. They still matter for conversion — CPC is
$5–9, so the few people searching them are valuable — but they will not bring traffic:

| Keyword | Vol/mo | KD |
|---|---|---|
| landscaping charleston sc | 260 | 40 |
| landscape lighting charleston sc | 140 | 26 |
| artificial turf charleston sc | 110 | 16 |
| outdoor kitchen charleston sc | 50 | 12 |
| hardscaping charleston sc | 50 | 10 |
| pergola charleston sc | 20 | 0 |
| pool pavilion charleston | 20 | 0 |
| patio pavers charleston sc | 20 | 0 |

No measurable volume at all: `pergola builder charleston`, `custom pergola
charleston`, `outdoor pavilion charleston sc`, `retaining wall charleston sc`.

**Traffic has to come from the question cluster instead:**

| Question | Vol/mo | KD |
|---|---|---|
| what is the purpose of a pergola | 590 | 14 |
| how much does a pergola cost | 390 | 19 |
| do pergolas provide shade | 320 | 3 |
| do pergolas have roofs | 260 | 13 |
| how much does it cost to build a pergola | 260 | 14 |
| how much is a pergola | 260 | 17 |
| pergola vs gazebo (3 variants) | ~680 | 7–16 |
| **do I need a permit for a pergola** (3 variants) | **~590** | **6–9** |
| pergola vs pavilion | 210 | **1** |
| how tall should a pergola be | 210 | 2 |
| how to attach pergola to house | 210 | 5 |
| backyard pavilion | 1000 | 22 |
| outdoor pavilion | 1600 | 21 |

**Deliberately skip the DIY terms.** `how to build a pergola` (8,100/mo) and
`what is a pergola` (5,400/mo) attract people who will never hire a builder.

**The permit cluster (~590/mo, KD 6–9) is the biggest opportunity on the site.**
Cramers pulls permits in-house. Competitors say "check with your county"; we can
say exactly what Charleston, Mount Pleasant and Summerville require. Nobody else
can write that post as well. **Not yet written — needs Zach's answer to Q11.**

The pavilion keyword cluster is dominated by gazebo kits for sale (retail
intent). Pavilions are low-search, high-ticket: build that page to **convert**,
not to rank.

### Semrush usage notes

No saved project exists in the account, so research is not persisted there —
record findings in this file. `phrase_questions` costs ~1600 API units per call,
`phrase_related` ~1200, `phrase_these` ~140. Prefer `phrase_these` for batches.

---

## ⚠️ Facts that need Zach's confirmation

These were contradictions between pages. Each was resolved in favour of the
figure sourced from Zach's interview (on `outdoor-kitchens.html`), but **none of
them has been confirmed directly.** Ask before publishing.

| Fact | Now says | Previously said elsewhere |
|---|---|---|
| Pergola cost | $10,000–$30,000 | $8,000–$40,000+ (3 tiers) |
| Pavilion cost | $30,000–$90,000+ | $18,000–$100,000+ |
| Permit timeline | 4–6 weeks | 2–4 weeks |
| Pavilion build time | 6–8 weeks | 1–2 weeks |

---

## Page status

Bar to clear is `outdoor-kitchens.html`.

| Page | Status |
|---|---|
| outdoor-kitchens.html | ✅ done — from Zach's answers |
| summerville-sc.html | ✅ done — from Zach's answers |
| pergola-pavilion-installation-charleston-sc.html | ✅ blog re-aimed at "pergola vs pavilion" |
| pergolas.html | 🔄 **in progress** — interview sent, awaiting answers |
| pergolas-pavilions.html | 🔄 **in progress** — same interview |
| patios-pavers.html | ⬜ generic |
| retaining-walls.html | ⬜ generic — worst page on the site, 9× "near me" keyword stuffing |
| landscape-installation.html | ⬜ generic — carries most internal link weight |
| hardscape-installation.html | ⬜ generic |
| landscape-lighting.html | ⬜ generic |
| artificial-turf-installation.html | ⬜ generic |
| charleston-sod-installation.html | ⬜ generic |
| irrigation-system-installation.html | ⬜ generic |
| concrete-services.html | ⬜ generic |
| concrete-pool-decks.html | ⬜ generic |
| fireplaces.html | ⬜ generic |
| fountain-water.html | ⬜ generic |
| outdoor-structures.html | ⬜ generic |
| plants.html | ⬜ generic |
| mulching-bed-maintenance.html | ⬜ generic |
| landscape-drainage-services-charleston-sc.html | ⬜ generic |
| landscape-grading-services-charleston-sc.html | ⬜ generic |
| outdoor-shower-installation-charleston-sc.html | ⬜ generic |

Quick audit for whether a page has been done — generic pages score 0 on prices
and have no FAQ schema:

```
for f in *.html; do printf '%-50s prices:%-3s names:%-3s nearme:%-3s faq:%s\n' "$f" \
  "$(grep -oE '\$[0-9][0-9,]*' $f|wc -l)" "$(grep -oiE 'Doug|Zach' $f|wc -l)" \
  "$(grep -oiE 'near (you|me)' $f|wc -l)" "$(grep -c FAQPage $f)"; done
```

### Known structural issues

- **Four pages cover pergolas/pavilions.** `pergolas.html` and
  `pergolas-pavilions.html` are service pages (14 inbound links each);
  `pergola-pavilion-installation-charleston-sc.html` and
  `pool-pavilion-charleston-sc.html` are blog posts (2 each). The first blog post
  used to compete with both service pages on commercial terms — fixed 2026-09-19
  by re-aiming it at "pergola vs pavilion". **`pool-pavilion-charleston-sc.html`
  has not been checked for the same problem.**
- `landscape-design.html` is a redirect stub → `landscape-installation.html`
- The README's Pages URL points at `landmaster9000.github.io`, but the remote is
  `zcramersoccer-rgb/Website_Sandbox`. Stale, worth fixing.

---

## Open interview — Pergolas & Pavilions

Awaiting Zach's answers. **Highest value first:** Q8/Q9 (feeds a 390/mo query
and the service page), Q11 (unlocks the ~590/mo permit cluster), Q1 (becomes a
KD-1 blog post).

**The decision**
1. When someone is torn between pergola and pavilion, what do you tell them? Is there a question that settles it fast?
2. Roughly what is the split — do most people end up with pergola or pavilion?
3. Does anyone regret the choice afterward? Which direction?

**Materials & build**
4. What do you build pergolas out of by default — cedar, PT pine, aluminium? What do you steer people away from on the coast?
5. Same for pavilions: roof material, posts, ceiling finish. (Is the haint blue tongue-and-groove in the West Ashley photos typical or a one-off?)
6. Stain, paint or natural? How often does it need redoing here?
7. Anything about salt air, humidity or hurricane tie-downs that changes how you build?

**Money**
8. Are $10–30k pergola / $30–90k+ pavilion still right for 2026? What pushes someone to the top of each range?
9. Biggest cost driver people do not expect?

**Timeline & permits**
10. Pergola build time?
11. **Which structures need permits, and does it vary by town? Anything special about HOAs?** ← unlocks the permit blog post
12. What do you know from 30+ years that homeowners do not think about until too late? (Roof drainage, post footings, wiring run during vs after the build, where the sun actually lands at 5pm.)
13. What is a request you push back on?

**Project stories — pick one or two**
14. West Ashley pool cabana — the brief, what was hard, what you are proudest of
15. Mount Pleasant pool pavilion (shiplap bathroom) — what made it a "grand" build
16. North Charleston — a swing set around a fire pit under a pergola. What is that story?

**Objections**
17. Top 3 things people ask on the phone before booking?

### Photos available for these pages

`assets/work/` has 80+ pergola/pavilion masters (`*-800.webp` and `*-1600.webp`).
Distinct projects worth telling stories about:

- **West Ashley pool cabana** — haint blue vaulted tongue-and-groove ceiling, cedar posts, TV wall, hammock lounge, storage shed, stepping-stone walkway
- **Mount Pleasant pool pavilion** — open rafter, shiplap bathroom, kitchen, travertine deck
- **Daniel Island** — pergola over an outdoor kitchen, 6 angles
- **Summerville** — pergola + putting green + kitchen (already used on the kitchens page)
- **North Charleston** — pergola with a swing set around a fire pit
- **Johns Island** — pergola with bluestone path and Japanese maple
- **James Island** — pergola-covered outdoor bar patio, rustic back porch kitchen
- **Isle of Palms** — pool pavilion

### Blog posts to write once answers land

- **Do you need a permit for a pergola in Charleston County?** — ~590/mo, KD 6–9, our moat
- Pergola cost deep-dive — 390/mo, links back to `pergolas.html`
