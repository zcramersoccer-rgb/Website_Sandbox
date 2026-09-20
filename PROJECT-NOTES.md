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
- **Rewritten from Zach's answers:** `outdoor-kitchens.html`, `summerville-sc.html`,
  `pergolas.html`, `pergolas-pavilions.html`, `concrete-pool-decks.html`,
  `patios-pavers.html`, `retaining-walls.html`
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
| pergolas-pavilions.html | ✅ rewritten 2026-09-19 (Part B) |
| patios-pavers.html | ✅ rewritten 2026-09-19 (Part C) |
| retaining-walls.html | ✅ rewritten 2026-09-19 (Part C). No carousel — only 5 wall photos exist and 2 are fire-pit shots. Restore one when more photos arrive. |
| landscape-installation.html | ⬜ generic — carries most internal link weight |
| hardscape-installation.html | ⬜ generic |
| landscape-lighting.html | ⬜ generic |
| artificial-turf-installation.html | ⬜ generic |
| charleston-sod-installation.html | ✅ rewritten 2026-09-20 (Part D). No carousel — only 5 real-sod photos exist. |
| irrigation-system-installation.html | ⬜ generic |
| concrete-services.html | ⬜ generic |
| concrete-pool-decks.html | ✅ rewritten 2026-09-19 (Part C), retargeted to pool deck resurfacing |
| fireplaces.html | ✅ rewritten 2026-09-20 (Part C + D fire answers) |
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

## ✅ Zach's answers — 2026-09-19 (VERIFIED SOURCE, use these)

Everything below came directly from Zach. Safe to put on pages. Anything NOT
here is still unverified — do not invent.

### Cross-cutting (applies to every service page)

- **The four figures are CONFIRMED correct**: pergola $10-30k, pavilion
  $30-90k+, permits 4-6 weeks, pavilion build 6-8 weeks.
- **Cheaper competing quotes** usually mean they are quoting something
  different — cheaper materials, less trim or no trim. Response: we can design
  within your budget.
- **Top 3 phone questions**: timeline, price/design, and the
  construction/landscaping process.
- **Warranty/credentials confirmed accurate**: 1-year workmanship and plant
  warranty, licensed residential builder, insured.
- **What they push back on: rushing.** They would rather stage a project over
  years than build something the client will not love.
- **What people want first**: a rough budget, because they do not know what
  things cost. After that they usually know how they want to use the space but
  need help with ideas on how to actually pull it off.

### Pergola vs pavilion vs gazebo — the definition (Zach, final wording)

Use this wording. Two earlier versions were wrong and were corrected.

- **Pergola** — traditionally an **open** structure, with a **flat, slatted or
  gently sloped roof**. Cramers also build them closed in (solid roof, finished
  ceiling, electrical, post and beam trim) and it is **still a pergola**.
  The least expensive of the three, which is why most clients choose one.
- **Pavilion** — can have a flat or shed roof **as well**, but its options
  **expand** to **gable, hip** and other pitched forms. Open-sided or
  **partially enclosed**, and **generally larger**.
- **Gazebo** — closer to a pergola in scale, a smaller garden structure, but
  with more **decorative forms**, most recognisably a **domed roof**.

**Do not write** that the split is open vs covered, that a pergola cannot have a
roof, or that a pavilion is defined by a gable/hip/gambrel roof — a pavilion can
have a flat or shed roof too. The distinction is the **range** of roof forms
plus scale and enclosure.

### Pergola vs pavilion — earlier framing, now superseded

**The first question is how they want to use the space.**

A pergola is generally cheaper and smaller. **A pergola can be built with OR
without a roof, ceiling, electrical and post-and-beam trim.** It can be a
simple garden structure, or fully finished like the Summerville pergola
kitchen — roof, ceiling, post and beam trim, kitchen underneath.

A pavilion is a larger built structure, offering different roof framing styles
and more amenities, at a higher cost.

**Most people choose a pergola** — cheaper, and you still get the functionality
of a covered roof structure.

**No regrets reported**, which Zach attributes to the design process making
sure it is built for their needs.

> ⚠️ The old site copy said "a pergola filters light and keeps the space open;
> a pavilion has a solid roof and keeps the rain off." **That is wrong** — a
> pergola can have a solid roof and ceiling. The real distinction is scale,
> structure and amenities, not open vs solid roof.

### Materials and construction

- Structures are **mainly framed in pressure-treated lumber**. Finish trim
  boards can be various lumber types or **Hardie board**. **Cedar is a good
  lumber option.**
- **Metal-framed pergolas** are available: cost more, modern durable look, and
  allow a large **cantilever-style** pergola.
- Pavilion material choice comes down to **architectural style and budget**.
- People like the **storage/bathroom area at the back** of pavilions — as in
  the pool cabana and the Mount Pleasant pavilion.
- Ceilings: they prefer **individual tongue-and-groove boards**; the budget
  alternative is **T1-11 plywood**.

### Finish and maintenance

- **Stain**: reapply 8-12 months after the initial coat, then every few years
  as needed.
- **Paint**: every 5-10 years depending on product and exposure.
- **Posts and fascia in direct exposure need more maintenance** than a covered
  ceiling.
- They offer **linseed oil paint** for exterior wood — natural, long lasting,
  easy to maintain, costs more to install.
- Want it natural? A **clear sealer** works but will not stop the wood greying.
- **West Ashley pool cabana**: client wanted a natural cedar look, so they used
  a stain with a little pigment matched to the cedar — keeps the natural colour
  while protecting against greying.

### Coastal and hurricane

Builds are made to last through hurricanes and coastal weather. They add
**hurricane strapping or structural screws that do the same job**. The paint
and stain guidance above is also what protects against coastal weather.

### What drives the price

- **$10k pergola**: simple, no post/beam trim, no ceiling, maybe no roof.
- **$30k pergola**: post and beam trim, ceiling, roof, electrical, maybe a kitchen.
- **$30k pavilion**: small and bare bones.
- **$80k+ pavilion**: like the West Ashley cabana — trim, speakers, accent
  lighting, storage/bathroom at the back, larger size.
- **Patio material matters**: salt-void concrete was the cheaper option at West
  Ashley; Mount Pleasant used travertine.
- **No single big cost driver** (maybe foundation/patio). It is mostly the
  little things adding up — on complex structures with a bathroom and sauna
  there are a lot of steps and different trades involved.

### Timelines and permits

- **Pergola build: one week to three weeks.**
- **Almost all structures need permits**, except under a certain square footage
  in certain towns — Isle of Palms was the example given.

### The details that matter later (Zach's own list)

- Positioning and layout relative to the yard, the sun and how it will be used
- Planning ahead for a later kitchen project if the work is being staged
- Using the **classical orders for proportioning**
- Planning how electrical and other utilities are hidden
- Knowing the **finish grade**
- Making sure they have all the amenities they want — speakers, lights, sauna

### Project stories

**West Ashley pool cabana** — the showpiece is the trim. Cedar posts and beams
**mitered tight**, then a colour-matched **Big Stretch caulk** to hide the seams
as the wood moves over time. The **ridge and hip rafters were trimmed out larger**
to frame the structure better. Plus the small details: lighting, speakers, and
the trim on top of the beams where the rafters pass through.

**Mount Pleasant pool pavilion** — had everything, but what set it apart was
the **scale and the beams**. The **glulam beams cost $10k in material alone** and
weighed a significant amount. More like a **timber-framed structure** than a
traditional pavilion.

**North Charleston (swing set around a fire pit)** — Zach did not recognise it
from the description; photo sent 2026-09-19, awaiting his reply.

### Lead time from signed quote to start (A5)

Depends on how busy they are and whether permitting or HOA approval is needed.
**Structures often take 1-2 months** to start. **Simple sod jobs they try to fit
in within a few weeks at most.** Use the matching figure per service page.

### ⚠️ Splicing trap: rebuild the whole body, don't patch zones

Patching several separate zones around kept sections went wrong on
`retaining-walls.html` — it left two FAQ sections and dropped the process
section. **Do one splice:** from the end of the tabs nav to the final CTA
section, inserting all new content plus any kept widget (extract the carousel
with a div-balancing scan, not a `</figure>` search — other figures exist in the
page). Anchor on **tag-stripped text**, since headings like
`<h2><span>Request a</span> Free ... Consultation</h2>` break literal searches.

Afterwards check: div balance 0, exactly one "Frequently Asked", zero
"near me/you", and walk the carousel in a browser.

### ⚠️ Editing trap: carousel slides encode their own position

Each `<figure class="cl-slide">` carries its own `cl-prev` / `cl-next` labels and
a `cl-count` span with absolute slide numbers. **Reordering or replacing a slide
silently breaks navigation** — reordering scrambles the prev/next targets and the
counters, and replacing a whole `<figure>` drops its controls, leaving a slide
you can land on but cannot leave. Both happened on `pergolas.html`.

After touching any slide, rebuild every figure's nav from its position:
prev = n-1 (wrap to last), next = n+1 (wrap to 1), count = "n / total". Then walk
the carousel in a browser and confirm the counter runs 1..n and wraps.

### ⚠️ Image dimensions must match the file

`width`/`height` attributes reserve layout space. Writing 1600x1200 on a 900x1600
portrait causes layout shift and a wrong aspect box. After any image swap, re-derive
both attributes from the actual WebP header and verify in a browser against
`naturalWidth`/`naturalHeight`.

Carousel frames are **4:3 with `object-fit: cover`**, so a tall portrait loses up to
46% of its height and can sever posts at their base. Prefer images at or near 4:3
for slides.

### ⚠️ Editing trap: FAQ text lives in TWO places

Every FAQ answer appears **twice** in these pages: once in the visible
`<details>` block, and once inside the `FAQPage` JSON-LD in `<head>`. The JSON-LD
comes first in the file, so a naive `s.replace(old, new, 1)` silently edits the
**schema** copy and leaves the visible answer stale — and regenerating the schema
from the visible text then wipes the change entirely. This bit five answers on the
blog and one on each structure page before it was caught.

Always target the visible block, then rebuild the schema from it:

```python
pat = re.compile(r'(<summary>[^<]*'+re.escape(q)+r'[^<]*</summary><p>)(.*?)(</p>)', re.S)
```

Then verify schema and visible text agree before committing.

### Still unanswered

- B17 pergola/pavilion-specific objections beyond the budget answer above
- B16 North Charleston swing/fire pit: Zach did not recognise it and says not to
  prioritise it. Substitute a different project if a page needs more content.

---

## ✅ Zach's answers — hardscaping (2026-09-19, VERIFIED SOURCE)

### Base prep (C1) — the core differentiator

Poor base prep is what makes a pool deck sink and crack. The usual cause is the
**backfill from the pool dig-out being poor dirt that was not compacted well
enough**.

- **Best method:** mortar-set the pavers on top of a **solid concrete base**.
- **Alternatives:** compacted **ROC** base with mortar set on top, or sand /
  granite fines on top.
- Instead of ROC you can use **#57 stone**, and you can add **geotextile fabric**
  underneath.
- **#57 stone helps prevent tree roots** growing into the patio, because it
  leaves air gaps.
- Different systems suit different projects.

### Drainage (C2)

Proper **grading**, and/or **drain basins with piping** to carry water off.

**Lowcountry towns are getting stricter about the amount of impermeable
surface, so permeable pavers are becoming a necessity.** (Good, current, and
nobody else is saying it.)

### Sealing (C3)

They seal pavers occasionally — check the **manufacturer's specs** for the
process and maintenance rather than generalising.

- **Travertine is porous** and hard to keep clean without a sealer.
- They commonly use **rock glue** for gravel walkways and around stepping stones.

### What fails (C4)

**Settling and roots.** The fix is doing it right the first time: proper
compaction and a **root barrier**.

### Price (C5, C6)

- **$18/sqft is a good starting point for patios.**
- **Natural stone** (travertine, bluestone, marble) looks best and lasts longest,
  costs the most.
- **Concrete pavers** have their own range, cheap through pricey.
- **Poured concrete is cheapest**, and **salt-void / tabby concrete looks great**.
- Which one depends on the job and the budget, but natural stone is the best
  looking and longest lasting.

### Pool decks

- **Resurface vs replace (P1):** resurfacing works **if the deck is structurally
  OK**. Cracking and settling means replacement. **Concrete install around
  $12/sqft** depending on the job; **removing the old concrete is extra**.
  Coating cost depends on the deck's condition and which coating the customer wants.
- **Why they fail (P2):** poor base prep and compaction causing settling and
  cracking. For **resurfacing**, failures come from poor prep before the new
  coating — the deck must be cleaned and any failing prior coating stripped off.
- **Materials (P3):**
  - **Travertine** — most expensive, elegant, stays fairly cool, higher
    maintenance. Everything heats up in direct sun in our heat.
  - **Salt-void** — cheapest.
  - **Pavers** — vary by product.
  - Salt-void and pavers are both concrete, so they heat up, but low maintenance.
  - **Nothing they install is slippery.**
  - **Pavers and travertine can be repaired piece by piece**; a cracked concrete
    deck cannot.
- **Mount Pleasant (P4):** travertine was the most expensive option but gave the
  customer the best looks, heat resistance and that luxury feel.
- **Coping (P5):** recommend **at least 1.5 inch thick coping, 2 inch is better**.

### Patios and pavers

- **Size (PP1):** no standard size, it depends on use and available space.
  **10x10 is the smallest** they would recommend for chairs and a table. A fire
  pit needs more, to move around it. **$18/sqft starting point.**
- **Material (PP2):** natural stone pavers are the luxury choice. Poured
  concrete is cheapest, and tabby or salt-void finishes look great, especially
  **with brick borders**. Concrete pavers are a good middle ground and suit a
  modern minimalist look.
- **Brands (PP3):** **Techo-Bloc** is a good modern option and they like using
  the **larger sizes**. Plenty of other brands worth exploring.
- **Patterns (PP4):** borders look good. They have done tabby concrete with a
  brick border **both around the outside and running through the middle to break
  the patio into sections**. Most people like random patterns; **diamond patterns**
  are popular too.

### Retaining walls

- **Cost (RW1):** start around **$50/sqft** for a **CMU block wall with a stucco
  finish**. **Height and material** are the biggest factors in cost per sqft.
- **Material (RW2):** block is most affordable; **poured** makes more sense for
  strength and size; **natural stone** is a premium for a specific look.
- **Permits (RW3):** **at 6ft from the lowest point** a wall needs permitting.
  **Drainage and flood zones** can change the requirements too.
- **Why walls fail (RW4, corrected 2026-09-19):** improper drainage *can* cause
  failure, but the **more common causes are construction shortcuts**:
  - **No rebar.**
  - **CMU block left unfilled.** Beyond the strength it costs, it means the
    **caps don't bond well** because there is so little surface area to bond to,
    so the caps come loose before the wall does.
  - **Bad stucco work.**
  - Then drainage. Proper install is **fabric and gravel behind the wall with
    weep holes** to let water out.

  Do not write that drainage is the main cause &mdash; that was an earlier error.

### Fire pits

- **Gas vs wood (FP1):** gas is more convenient; wood is the fun of setting up
  and burning the logs, but more maintenance.
- **Placement (FP3):** mostly about **flow and use of the yard**. Smoke is not an
  issue **unless it is under a structure, and then it needs a chimney**.
- **The hero video fire bowls (FP4):** a **Summerville** project. They built the
  **stone pedestals with a quartzite countertop**, with a **door to store the
  propane tank**, and the fire bowls sat on top.

### Fire pits, continued (FP2, answered 2026-09-19)

- **Built-in is ideal for people with the space.** Many don't have it, and prefer
  a **freestanding pit they can move out of the way** so the patio can be used
  for other things too.
- **The fire bowls on pedestals are a different thing from fire pits** — don't
  conflate them.
- **A fire pit can be as cheap as $1,000 for a simple kit.** Custom ones in
  higher-end materials cost more.

### Photos chosen for the project stories

- **Patios (PP5):** `summerville-marble-patio`
- **Retaining walls (RW5):** `charleston-residential-driveway-retaining-wall-landscaping`

⚠️ **Descriptions still needed for both.** Zach picked the photos but has not yet
described either project, and nothing goes on a page unsourced.

⚠️ **Only 5 retaining wall photos exist** in the whole library, and two of them
are really fire-pit shots. The carousel was **removed from that page** rather
than run a two-slide gallery. Put it back when there are photos to support it —
worth a photo run on the next wall job.

### Project stories (answered 2026-09-19)

**Summerville marble patio (PP5)** — `summerville-marble-patio`
Installed with **mortar over a concrete slab**, which is what let them get a
perfect install on the pavers with **crisp edges**. It has a **brick border**, and
the marble is **tile imported from Italy**.

**Charleston driveway retaining wall (RW5)** —
`charleston-residential-driveway-retaining-wall-landscaping`
**CMU block with rebar in every other void**, sitting on a **2ft wide
foundation**. Finished with **stucco and a brick cap**, with **plantings to soften
the wall**.

---

## ✅ Zach's answers — Part D (2026-09-19, VERIFIED SOURCE)

### Sod

- **Varieties:** zoysia and St Augustine are the most common. Zach says to use
  publicly available horticultural information for the variety characteristics,
  since it is readily available — but keep business claims to what is here.
- **Price: $750 a pallet installed.** Moves up or down with job size.
  **Does NOT include the dig-out or grading before the sod goes down.**
- **Prep:** spray and kill the old grass if there is any, dig the old grass out,
  regrade the yard as necessary, then lay the new sod.
- **Watering:** every day for the first two weeks. **30 minutes is enough**,
  depending on heat. **Avoid watering late in the day or at night** — sod that
  stays wet can rot or pick up a fungus.
- **Timing:** best is **mid-summer to early fall**. Worst is **February to March**,
  as it is coming out of dormancy.
- **Why new sod fails:** poor grading gives a lumpy yard — they **roll the sod
  after install** to level it and put down a little fertiliser, fungicide and
  pesticide depending on the season. Then improper watering; dogs or heavy
  traffic in the first couple of weeks; and improper sunlight, from laying sod
  where it will not grow.

### Fireplaces and fire pits

- **Which one:** both give heat and function. A **fire pit suits smaller yards**
  and works where it sits toward the centre of the patio. With the space, a
  **fireplace makes more of a statement, can act as a screen wall**, and works
  well **built into a pavilion**.
- **Price: a cheap fireplace kit from $8,000; custom builds $20,000+**, depending
  on size, height, material, and gas against wood burning.
- **Materials:** stone, stucco or brick. They also offer **microcement and
  specialised lime plasters** as finishes — **and those work on outdoor kitchens
  too**.
- **Gas vs wood:** wood burning is great for people who want the experience, but
  costs more because it needs a **real chimney**, and it is higher maintenance.
  Gas is low maintenance. **Either way, use a blower** to push the hot air out and
  actually get warmth off the fireplace.

### Concrete and driveways

- **Price: $12/sq ft.** Stamping, colorant and cut patterns add cost. Otherwise
  it is mostly **prep** that moves the number: rebar, vapour barrier, wire mesh,
  dig-out, or removing old concrete.
- **Finishes:** **salt-void and tabby are the most popular.** Salt-void gives a
  nice texture and a weathered look; **tabby is perfect for the coastal beach
  vibe**.
- **How it should be built — the detail that separates a good slab from a bad one:**
  - **At least 4 inches thick.** Many companies frame with **2x4, which is only
    3.5 inches**, so if they dig out only to the bottom of the form the slab is
    under thickness.
  - **Mesh** holds it together; **rebar** resists bending and prevents cracking.
  - **Control joints no more than 15 ft apart**, and **no panel over 300 sq ft**.
  - A slab between other concrete or a building needs an **expansion board**.
  - **Fibre, and wetting the concrete as it cures**, helps curing and strength.
- **Cure times:** walk on it within **1 to 2 days**, wait **1 week before
  driving**. Cold and rainy weather extends that.
- **Why driveways crack:** improper install — **too wet a mix, too thin, no
  reinforcement** where it was needed. **Tree roots cause the most problems**,
  along with a base that has settled over time.

### Outdoor showers

- **Price: $8,000 to $15,000**, on size and material. Pressure-treated lumber is
  cheap, **sapele is expensive**. The hardscape material and the shower fixture
  also move the price.
- **Hot and cold**, not cold only.
- **Drainage: most outdoor showers use a dry well.**
- **Enclosure** is built from pressure-treated or **sapele** lumber.
- **Any material survives with proper maintenance, but hardwoods like sapele
  offer the best longevity.**
- **No permit required.** Some **HOAs need approval**, especially if the shower is
  visible from the street.

---

## Semrush — remaining services (run 2026-09-19)

| Keyword | Vol/mo | KD | CPC |
|---|---|---|---|
| **sod installation** | **18,100** | **27** | $4.71 |
| **outdoor fireplace** | **18,100** | **21** | $0.96 |
| artificial turf installation | 9,900 | 39 | **$6.40** |
| **sod installation cost** | **5,400** | **16** | $2.82 |
| **outdoor shower ideas** | **5,400** | **24** | $0.35 |
| concrete driveway cost | 4,400 | 21 | $3.67 |
| stamped concrete driveway | 3,600 | 29 | $3.06 |
| how much does sod cost | 2,900 | 28 | $0.80 |
| artificial turf cost | 2,400 | 28 | $2.02 |
| french drain cost | 2,400 | 18 | $4.13 |
| yard drainage solutions | 2,400 | 43 | $3.58 |
| sprinkler system cost | 1,300 | 19 | $2.26 |
| irrigation system cost | 880 | 30 | $2.25 |
| landscape design cost | 720 | 10 | $2.37 |
| mulch installation cost | 720 | 7 | $2.29 |
| how much does artificial turf cost | 590 | 20 | $1.76 |
| outdoor fireplace cost | 210 | 5 | $1.51 |
| landscape lighting cost | 110 | 12 | $2.86 |
| landscape grading cost | 110 | 24 | $2.87 |

**Too competitive:** landscape lighting (33,100 but KD 53).

**Order for the rest, by opportunity:**
1. **Sod** — 18,100 + 5,400 + 2,900, difficulty 16 to 28, $4.71 CPC. The biggest
   remaining opening on the site.
2. **Fireplaces and fire pits** — outdoor fireplace is 18,100 at difficulty 21,
   which is unusual for that volume, plus outdoor fireplace cost at difficulty 5.
   Partly answered already (FP1, FP3, FP4 and the built-in question).
3. **Concrete and driveways** — driveway cost 4,400/21 and stamped 3,600/29.
4. **Outdoor showers** — 5,400 at difficulty 24, and we have the photos.
5. **Artificial turf** — installation is hard at 39, but it carries the highest
   CPC on the site at $6.40, so the cost terms are worth having.
6. **Drainage** (french drain cost 2,400/18), **irrigation** (1,300/19).
7. **Mulch** (720/7) and **landscape design** (720/10) — small but nearly free.

## Open interview — Part D (sent 2026-09-19)

### Sod — do first
S1. Which sod varieties do you install here, and which do you put where — sun,
    shade, heavy foot traffic, pets?
S2. What does sod cost installed? Per pallet, per sq ft, however you quote it.
S3. What prep goes in before it is laid — grading, soil, killing the old grass?
S4. What do you tell people about watering in the first few weeks?
S5. Best and worst time of year to lay sod in Charleston?
S6. Why does new sod fail when it fails?

### Fireplaces and fire pits — finishing the set
F1. Outdoor fireplace against fire pit: when do you recommend each, and what
    does a fireplace cost?
F2. What do you build fireplaces out of — stone, stucco, brick?
F3. Draft and chimney: what do people get wrong?
F4. Gas logs, wood, or both in a fireplace?

### Concrete and driveways
CD1. Driveway cost per sq ft, and what moves it?
CD2. Stamped, broom, salt-void, exposed aggregate — when do you use each?
CD3. Thickness, mesh or rebar, control joints. What do you do that cheaper
     outfits skip?
CD4. How long before you can drive on it?
CD5. What cracks a driveway here?

### Outdoor showers
OS1. What does an outdoor shower cost?
OS2. Hot and cold, or cold only — what do most people do?
OS3. How do you handle drainage and privacy?
OS4. Which materials survive out here, and which do not?
OS5. Any code or permit issues?

---

## Semrush — hardscaping cluster (run 2026-09-19)

| Keyword | Vol/mo | KD | Note |
|---|---|---|---|
| **pool deck resurfacing** | **5,400** | **15** | best opportunity in the cluster, $5.83 CPC |
| **pool deck ideas** | **4,400** | **18** | |
| retaining wall ideas | 8,100 | 33 | |
| paver patio ideas | 6,600 | 39 | |
| retaining wall cost | 1,900 | 30 | |
| **travertine pool deck** | **1,900** | **8** | we built one at Mount Pleasant |
| paver patio cost | 1,300 | 27 | |
| how much does a retaining wall cost | 720 | 10 | |
| stamped concrete cost | 720 | 20 | |
| how much does a paver patio cost | 210 | 12 | |
| do pavers need to be sealed | 110 | 9 | easy win, practical |
| concrete pool deck cost | 70 | 8 | |

**Too competitive, do not chase:** retaining wall (27,100 / KD 42), outdoor fire
pit (18,100 / KD 47), patio pavers (14,800 / KD 40), fire pit ideas (14,800 /
KD 46), paver patio (12,100 / KD 48), stamped concrete patio (12,100 / KD 43).

**Order to rewrite the hardscape pages, by opportunity:**
1. **Pool decks** — resurfacing 5,400/KD15 plus ideas 4,400/KD18 plus travertine
   1,900/KD8. Nearly 12,000/mo of winnable volume, the highest-CPC terms in the
   cluster, and Cramers has the Mount Pleasant travertine deck to show.
2. **Patios & pavers** — the cost cluster is winnable; head terms are not.
3. **Retaining walls** — cost cluster winnable, and it is the worst page on the
   site (nine "near me" stuffs, zero specifics).
4. **Fire pits** — head terms are hard and "built in fire pit cost" is only
   20/mo. Lowest priority of the four.

## Open interview — Part C: hardscaping (sent 2026-09-19)

### Cross-cutting, all hardscape pages
C1. What do you lay on — base prep. How deep, what material, what do cheap
    installers skip that you don't?
C2. Drainage: what goes wrong in the Lowcountry, and what do you do about it?
C3. Do you seal pavers? If so when, how often, and is it worth it?
C4. What fails here after a few years, and why? Settling, weeds, washout, roots?
C5. Rough price per square foot, or however you actually quote it, for pavers
    vs poured concrete vs travertine?
C6. Which material do you steer people toward and why?

### Pool decks (do first)
P1. Resurfacing an existing deck vs tearing out and replacing — how do you
    decide, and what does each cost?
P2. What is wrong with most existing pool decks you are called out to?
P3. Travertine vs salt-void concrete vs pavers around a pool — heat underfoot,
    slip, salt, cost?
P4. The Mount Pleasant travertine deck: why travertine there, and how did it
    come out?
P5. Anything specific about coping, drainage or the pool edge?

### Patios & pavers
PP1. Most common patio size and what it runs?
PP2. Paver vs poured concrete vs stamped — when do you recommend each?
PP3. Brands or paver lines you use, and any you avoid?
PP4. Patterns, borders and banding — what actually looks good vs dated?
PP5. A patio project you are proud of, and what made it work?

### Retaining walls
RW1. What does a wall actually cost, and what drives it — height, length, material?
RW2. Block vs natural stone vs poured — when does each make sense?
RW3. At what height does engineering or a permit kick in here?
RW4. Drainage behind a wall: what do you do, and what happens when it is skipped?
RW5. A wall you have built that you would point to.

### Fire pits & fireplaces
FP1. Gas vs wood — what do most people pick and what would you tell them?
FP2. Built-in vs freestanding, and what does a built-in run?
FP3. Placement mistakes — smoke, wind, distance from the house?
FP4. The fire bowls on the pool wall in the hero video — whose project, what were they?

---

## Open interview — Part A: answer once, unlocks EVERY service page

These are cross-cutting, so the answers get reused on all 20+ service pages.
Worth getting first.

A1. **Confirm the four unconfirmed figures** in the table above (pergola
    $10-30k, pavilion $30-90k+, permits 4-6 weeks, pavilion build 6-8 weeks).
    They are live on the sandbox and came from the kitchens interview, never
    confirmed directly.
A2. When someone has a cheaper quote in hand, what do you tell them? What do
    you actually do differently?
A3. What are the top 3 questions people ask on the phone, whatever the service?
A4. What job or request do you turn down, or talk people out of?
A5. From signed quote to boots on the ground, what is the typical wait?
A6. The site claims a 1-year workmanship and plant warranty, licensed
    residential builder, insured. All still accurate?

---

## Open interview — Part B: Pergolas & Pavilions

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

---

## Semrush — sod question cluster (run 2026-09-20)

Do **not** run `phrase_questions` on the bare word "sod" — the results come back
almost entirely as "soda" (dirty soda, baking soda, club soda). Use "new sod",
"sod installation" or "laying sod" instead.

Useful from `phrase_questions` on **"sod"**:

| Keyword | Vol/mo |
|---|---|
| what is sod | 6,600 |
| how to lay sod | 4,400 |
| how to put sod grass / sod lawn | 3,600 each |
| how much does sod cost | 2,900 |
| how much is sod | 2,900 |

From `phrase_questions` on **"new sod"** — this is the real opportunity. Three
clusters dominate, and Zach has answered two of them outright:

| Cluster | Combined vol/mo (approx) | Do we have the answer? |
|---|---|---|
| **Watering** — how often / how long / how much to water new sod | **~4,500** | ✅ every day, 2 weeks, 30 min, never at night |
| **Mowing** — when to mow / cut new sod, how long to wait | **~2,500** | ❌ **no timing from Zach — open question** |
| **Fertilising** — when / should I / can I fertilize new sod | **~1,500** | ✅ a little at install, season-dependent |
| Care generally — how to care for / take care of new sod | ~1,000 | ✅ partly |

Top single terms: how often to water new sod (1,300), how long to water new sod
(1,000), when to mow new sod (720), how much to water new sod (590), how often
should you water new sod (590).

**The "don't water at night" answer is the differentiator.** Every competing page
says "water twice a day". Zach's answer (30 minutes, morning only, because wet
sod rots or gets a fungus) is more specific and contradicts the generic advice,
which is exactly what wins these queries.

---

## ⚠️ Photo trap: three "lawn" images are artificial turf

The filenames and alt text lie. Verified visually 2026-09-20 — **do not put these
on the sod page**, they are artificial turf:

- ~~`north-charleston-bluestone-patio-and-new-lawn`~~ → renamed
  `north-charleston-bluestone-patio-and-artificial-turf`
- ~~`sullivans-island-waterfront-backyard-pool-and-lawn`~~ → renamed
  `sullivans-island-waterfront-pool-and-artificial-turf`
- ~~`daniel-island-residential-turf-lawn-landscaping`~~ → renamed
  `daniel-island-artificial-turf-front-lawn`

**Fixed 2026-09-20.** All three were renamed, their alt text and portfolio
captions corrected, and they were pulled off the sod page.

Also: `lawn-landscaping-brick-border-c7e5` was a byte-identical duplicate of
`daniel-island-lawn-landscaping-brick-border`. Deleted 2026-09-20 with 71 others
(see below).

**The only genuine sod/lawn photos on the site (5 total):**

| File | Size | What it shows |
|---|---|---|
| `daniel-island-stepping-stone-lawn-pathway` | 1600×1400 | best one — real lawn, stepping stones (sod page hero) |
| `daniel-island-lawn-landscaping-brick-border` | 1400×1600 | established lawn, brick border, mulch bed |
| `charleston-sod-installation-and-landscape-edging` | 1200×1600 | fresh sod, seams visible, commercial |
| `charleston-fresh-sod-turf-and-mulch-landscaping` | 1600×1200 | same job, wider landscape framing |
| `mount-pleasant-luxury-modern-home-backyard-lawn` | 1600×900 | big lawn, modern house, backlit/dark |

Ask Zach for more sod photos — especially a pallet being laid, a roller in use,
and a before/after of a regraded yard. That would unlock a carousel.

---

## ❓ Open question for Zach — sod

**When can someone mow new sod?** ~2,500 searches a month ask this and we have no
answer from him. The FAQ currently answers it with the root-tug test (lift a
corner, if it resists it has rooted) and no week number, which is true but
generic. **Get his actual number and rewrite that FAQ.**

Related, if he wants to go further: what he tells people about fertilising after
the install, and whether they offer a sod warranty.

---

## 🖼️ Image & alt-text conventions (established 2026-09-20)

The whole image library was audited and normalised. **Keep to these rules** when
adding the new cabana photos or anything else.

### Filenames
`<place>-<what-it-is>-<size>.webp`, all lowercase, hyphenated, e.g.
`west-ashley-haint-blue-plywood-cabana-ceiling-1600.webp`.
Two sizes per image: `-800` and `-1600`, where the number is the **long edge**,
not the width. So a portrait shot at `-1600` is 1200×1600, and its `-800` is
600×800 — that is why the `srcset` says `800w` on a file that is only 600px
wide. That is the existing site-wide convention; do not "fix" it per-image.

### `width` / `height` attributes
Set them from the **`-1600` file's real dimensions**, which is what `src` points
at. What matters is that the ratio is right, because that is what reserves the
space and stops layout shift. Read them out of the WebP header — do **not**
assume 1600×1200; eleven images were wrong that way before.

### Alt text
- One canonical alt per image file, used identically everywhere it appears.
- Written as a readable phrase, not a keyword list. "Herringbone brick walkway
  with brick edging between new planting beds in Charleston, SC", not
  "Brick walkway edging modern plantings".
- **Always ends in a place**: `... in <Town>, SC` or `... on <Island>, SC`.
  Never "by Cramers Landscaping" — that names no location and wastes the slot.
- **Islands and beaches take "on"**: Daniel Island, James Island, Johns Island,
  Isle of Palms, Sullivan's Island, Kiawah Island, Folly Beach, Edisto.
  **Mainland towns take "in"**: Charleston, North Charleston, Mount Pleasant,
  West Ashley, Summerville, Awendaw.
- Capitalise properly: Japanese maple, Adirondack, TV, BBQ.
- Decorative icons keep `alt=""`. There are 397 of those; leave them.
- **Describe what is actually in the photo.** Three images were captioned as
  lawns for years and are artificial turf. Look at the picture before writing
  the alt.

### Figcaptions
Derived from the alt: `Description &mdash; Place, SC`. Split at the **last**
"in/on/at <Place>, SC", not the first, or you get
"Backyard fire pit — artificial turf on Sullivan's Island, SC".

### Cleanup done 2026-09-20
- **72 duplicate files deleted** (12 MB). Every one was a byte-identical copy of
  a properly-named file, distinguishable only by a 4-hex-digit suffix
  (`-b815`, `-c7e5`, …) and carrying a location-less
  "… by Cramers Landscaping" alt. 162 references across the nine location pages
  were repointed at the canonical file first.
- **196 alt attributes and 173 figcaptions** rewritten.
- Verified afterwards: 0 broken image references, 0 alts without a location,
  0 images with more than one alt, 17 pages rendered clean in a browser.

**Checks to re-run after any image work:**
```
0 broken src/srcset (strip the ?v= query before checking the path)
0 alts not matching  /\b(in|on) [A-Z][^,]*, SC$/
0 files with more than one distinct alt
no "by Cramers Landscaping" inside an alt attribute
```

---

## ❓ Open question for Zach — "Sullivan's Island" spelling

The site writes it **"Sullivans Island"** with no apostrophe, ~100 times, in
page titles, H1s and body copy. The official name is **Sullivan's Island**.

Alt text and figcaptions were switched to the apostrophe on 2026-09-20. The
**page titles, H1s and prose were left alone**, because changing the H1 and
title of `sullivans-island-sc.html` is a targeting decision, not a typo fix.
Google treats the two forms nearly identically, so this is low-risk either way —
but it should be one or the other, not both. **Ask Zach which he wants.**

---

## Semrush — fire features (run 2026-09-20)

**The head terms are a trap.** `outdoor fireplace` is 18,100/mo at difficulty 21,
which looked like the best remaining opening on the site. It is not, because of
what people actually type after it:

| Question | Vol/mo | Who is asking |
|---|---|---|
| how to build an outdoor fireplace | 880 | DIY |
| how to make an outdoor fireplace | 720 | DIY |
| do it yourself outdoor fireplace | 480 | DIY |
| how to build outdoor fireplace | 320 | DIY |
| how do you build an outdoor fireplace | 210 | DIY |
| **how much does an outdoor fireplace cost** | **140** | **buyer** |
| **how much does it cost to build an outdoor fireplace** | **90** | **buyer** |
| **how much is an outdoor fireplace** | **50** | **buyer** |

Same story on fire pits: `how to build a fire pit` is **90,500/mo**, and the rest
of the cluster is smokeless-pit product questions, how to light a fire, and what
to do with the ashes. **None of that is a customer.**

**So the page does not chase the head terms.** It targets:
- the **cost cluster** &mdash; `outdoor fireplace cost` (210/mo, **KD 5**) plus the
  three buyer questions above, roughly **490/mo of genuinely commercial volume at
  very low difficulty**. Zach's numbers ($8k kit, $20k+ custom, $1k fire pit kit)
  answer it with figures competitors do not publish.
- **`how far should a fire pit be from house`** &mdash; 390 + 320 + 320 =
  **~1,030/mo at 0.03 competition**, and a placement question a builder can
  legitimately own.
- the **decision queries** (fireplace vs fire pit, gas vs wood, built-in vs
  freestanding). No volume data needed &mdash; these are what people ask on the phone.

**Do not write DIY how-to content to chase the 18,100.** It would rank for people
who have already decided not to hire anyone.

### The differentiator on this page
**The blower.** Zach's point that without one you get a fire you can look at
rather than a fire you can feel is not on competitor pages, and it is the kind
of specific, useful thing that wins a page trust. Same with fire bowls being a
different product from fire pits.

---

## ⚠️ Photo trap: a half-built fireplace was the lead carousel image

`summerville-modern-fireplace` is a **construction shot** &mdash; the fireplace is
wrapped in black weather barrier with the gas firebox just set in. It was
**slide 1 of the fireplaces carousel**, captioned "Modern fireplace in
Summerville, SC". Removed from the page 2026-09-20. The file is still in
`assets/work/` and is now used nowhere; leave it unless Zach wants a
before/after somewhere, and if it is ever used again, caption it as in progress.

**Fire photos, grouped by project** (several are the same job from two angles &mdash;
do not put two of one project in the same carousel):

| Project | Files |
|---|---|
| Summerville stacked-stone fireplace (best shot on the page) | `summerville-rustic-stone-fireplace` (hero), `summerville-stone-outdoor-fireplace-patio-landscaping` |
| Charleston brick back-porch fireplace | `charleston-back-porch-fireplace-design` |
| Charleston tabby fire pit | `charleston-tabby-fire-pit-with-adirondack-seating`, `charleston-tabby-firepit-retaining-wall` |
| Mount Pleasant block fire pit + wall | `mount-pleasant-modern-fire-pit-retaining-wall`, `mount-pleasant-backyard-retaining-wall-fire-pit` |
| West Ashley cabana fire table | `west-ashley-backyard-hardscape-fire-pit-and-pavilion`, `west-ashley-patio-fire-table-adirondack-chairs` &mdash; **use sparingly, Zach asked not to lean on this project** |
| Summerville fire bowls (the project story) | `summerville-custom-pool-fire-features-landscape` |
| Singles | `edisto-backyard-fire-pit-paver-patio`, `summerville-paver-patio-fire-pit`, `summerville-fire-pit-patio-with-pergola`, `daniel-island-tabby-fire-pit-sitting-wall`, `sullivans-island-backyard-fire-pit-on-artificial-turf`, `mount-pleasant-fire-feature-fountain` |
| Deprioritised | `north-charleston-pergola-swing-set-around-a-fire-pit` &mdash; Zach did not recognise it and said not to prioritise it |

---

## ❓ Open question for Zach — fire pit clearance

`how far should a fire pit be from house` is ~1,030 searches a month at almost no
competition, and we have no number from him. The page answers it honestly &mdash;
placement is about flow and use of the yard, smoke only matters under a structure
where you need a chimney, and we follow the manufacturer's clearances and local
code. **A real number, or his rule of thumb, would make that answer much
stronger.**

---

## ✅ Sullivan's Island apostrophe — resolved 2026-09-20

Zach chose the apostrophe. 102 replacements across 59 pages, covering page
titles, H1s, meta descriptions and body copy. Filenames, links and element ids
are unchanged (`sullivans-island-sc.html`, `assets/work/sullivans-island-*`).
House style is the entity: `Sullivan&rsquo;s Island`.
