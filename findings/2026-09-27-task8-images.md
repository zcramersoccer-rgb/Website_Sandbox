# Task 8 — `assets/work/` image audit — 2026-09-27

Diagnosis only. Nothing edited, nothing committed, no file renamed or deleted.

**The brief's "64" cannot be reproduced.** `photos.json` is not in this repo (it lives in an
unversioned local folder), so the exact 64 images it's missing can't be listed. Per the brief,
audited every image base name in `assets/work/` instead — 339 of them, a superset that contains
those 64. Everything below is checked against **live**, not the sandbox: the 74-page snapshot at
`scratchpad/live2/*.html` (from `scratchpad/live-urls.txt`), fetched fresh this session. Live pages
load work photos from `https://cramerslandscaping.com/wp-content/uploads/2026/09/<file>`, lazy-load
via `data-src`/`data-srcset` (real `src` is a placeholder GIF), and occasionally carry a WordPress
upload-collision suffix (`-1600-1.webp`) or `-scaled`; both are normalized back to `<base>-<size>`
before comparing to `assets/work/`. Sandbox pages (78 `*.html` files at the repo root — the 74 real
pages plus `_all-pages.html`, `_draft-pay-invoice.html`, the `landscape-design.html` redirect stub,
and `thank-you.html`, none of which reference any work photo) load the same files directly from
`assets/work/`. Everything was hashed (SHA-256) and cross-checked with Python; nothing here was
eyeballed except the one image called out in the "incidental" note, which was viewed directly to
confirm what it shows. Scripts: `scan.py`, `analyze.py`, `towns.py`, `captions.py`, `dupes.py`,
`orphans2.py`, `multiref.py` — all in the scratchpad, not the repo.

**Context read first, per the brief:** `DECISIONS.md` #35 (2026-09-24) is the source of the "24
phantom fixes" caution `CLOUD-TASKS.md` repeats for this task: it found that a brief reading
`photos.json`'s `same_file_two_towns` report as 24 cases of one photo published under two towns was
wrong — that field's `names` holds old vendor filenames, while the resolved `town`/`slug` are what
actually reaches a page, and all 24 groups resolve to a town Zach allows. #35's own sitewide check
found 0 live wrong-town bugs, and it already flagged these same 64 photos.json-uncovered images as
checked (naming no banned town). `PROJECT-NOTES.md`'s "Image & alt-text conventions" (2026-09-20)
sets the filename/alt/figcaption rules applied below, and its "photo trap" notes (artificial turf
captioned as lawn; a James Island job once mislabeled Johns Island) are the precedent for two things
found again here. This audit is three days newer than #35 and independently confirms the same
conclusion still holds, with more detail on the orphan/duplicate side than #35 recorded.

## Summary counts

| | |
|---|---|
| Files in `assets/work/` | **693** (`.webp` only) |
| Distinct base images (strip `-400`/`-800`/`-1600`) | **339** — 324 with `{800,1600}`, 15 with `{400,800,1600}`. 0 filenames fail the `<base>-<size>.webp` pattern. |
| Actually-distinct photographs (by byte content) | **249** — i.e. 90 of the 339 base names are pure duplicate content of another base under a different name. |
| Referenced by at least one live or sandbox page | **221 / 339 bases** (455 live (base,size) pairs; 457 sandbox pairs) |
| **Orphans** (in `assets/work/`, linked from no live and no sandbox page) | **118 bases / 236 files / 42.6 MB** (34.6% of the library's bytes) |
| **Reverse orphans** (live/sandbox reference resolves to no file in `assets/work/`) | **0** |
| **Size mismatches** (a page requests a variant the base doesn't have) | **0** |
| Sandbox vs. live disagreement | **1 base** (see below) — otherwise every referenced base agrees |
| **Duplicate groups** (byte-identical files, different names) | **149 groups / 330 files** — 181 files beyond one-per-group, ~36.8 MB |
| **Town-label defects** (Kiawah / Sullivan's Island / Folly Beach / Johns Island claimed for a real photo) | **0** |
| **Needs Zach** | **None.** Every anomaly below resolved from hashes + rendered HTML; nothing required guessing what a photo shows or where it was taken. |

## 1–2. Inventory and page references

339 bases, 693 files, no naming exceptions (details above). Per-base page lists exist in the
scratchpad (`state.pkl`) but aren't reproduced here in full — 221 rows of "which of 74 pages use
this" is not itself actionable; the orphan, mismatch and town tables below are the parts of that
mapping worth reading.

**The one sandbox/live disagreement:** `mount-pleasant-modern-outdoor-kitchen-string-lights` is
referenced only by sandbox's `blog.html` (both variants), as the thumbnail on the
`top-10-landscape-lighting-ideas-to-transform-your-outdoor-space` post's card. It is **absent from
every one of the 74 live pages** — confirmed by a plain string search of the whole live snapshot,
not just `blog.html`. The reason isn't a broken image reference: live's `/blog/` currently lists
**21** post cards where sandbox's `blog.html` lists **22** — the entire card for that post (image,
title and link) is missing from the live archive, though the post's own page is still live at its
URL (`blog__top-10-landscape-lighting-ideas...html` exists in the snapshot) and doesn't use this
image itself either way. This is the same post CLOUD-TASKS Task 4/7 already flags as a genuine
post-rebuild indexing refusal under consideration for consolidation — not a new bug, and not
something to fix by re-adding the card.

## 3. Orphans

**118 of 339 base images (236 files, 42.6 MB) are linked from nothing** — not one of the 74 live
pages, not one sandbox page. They split into two very different kinds:

- **57 bases are dead alternate names** — a byte-identical copy of the same photo *is* live, just
  under a different base name. No content is missing; these are pure leftover files.
- **61 bases are true orphans** — this exact photo (by content, not just by name) appears under
  **no** name on any live or sandbox page. 122 files, 19.9 MB.

Reverse direction: **zero.** Every live and sandbox reference to a `<base>-<size>.webp`-shaped file
(455 live pairs, 457 sandbox pairs, after normalizing WordPress's `-1`/`-2`/`-scaled` upload
artifacts) resolves to a file that exists in `assets/work/`. The 11 distinct live filenames that
*don't* fit that size pattern (`logo-white-accent-620`, `hero-poster-3`, `container-10`...`13`,
`contact-hero-section`, two WordPress `-300x300-1` menu icons) all belong to `assets/img/`, not
`assets/work/` — checked individually, not assumed.

### True orphans (61) — this photo isn't placed on any page under any name

| Base image | Sizes | | Base image | Sizes |
|---|---|---|---|---|
| `awendaw-historic-brick-paver-driveway-installation` | 1600, 800 | | `mount-pleasant-travertine-front-walk` | 1600, 800 |
| `back-porch-fireplace-design` | 1600, 800 | | `mount-pleasant-travertine-paver-walkway-design` | 1600, 800 |
| `backyard-pergola-swing` | 1600, 800 | | `neighborhood-brick-pillar-entrance-89ec` | 1600, 800 |
| `brick-and-bluestone-front-entry-steps` | 1600, 800 | | `neighborhood-landscaping-21b8` | 1600, 800 |
| `charleston-artificial-turf` | 1600, 800 | | `north-charleston-wood-privacy-fence` | 1600, 800 |
| `charleston-back-porch-fireplace-design` | 1600, 800 | | `outdoor-bar-with-painted-paneling-2228` | 1600, 800 |
| `charleston-backyard-pergola-swing` | 1600, 800 | | `outdoor-kitchen-island-6fcf` | 1600, 800 |
| `charleston-brick-and-tabby-side-yard-walkway` | 1600, 800 | | `outdoor-kitchen-pergola-ab2a` | 1600, 800 |
| `charleston-custom-fence-gate` | 1600, 800 | | `pergola-patio` | 1600, 800 |
| `charleston-entry-gates-3` | 1600, 800 | | `pergola-patio-2` | 1600, 800 |
| `charleston-front-entry-garden-lighting-at-night` | 1600, 800 | | `rollings-school-planters` | 1600, 800 |
| `charleston-herringbone-brick-pathway-installation` | 1600, 800 | | `summerville-curved-patio-steps` | 1600, 800 |
| `charleston-herringbone-brick-patio-waterfront` | 1600, 800 | | `summerville-custom-outdoor-kitchen-2` | 1600, 800 |
| `charleston-irrigation-system-running-backyard` | 1600, 800 | | `summerville-custom-outdoor-kitchen-patio-design` | 1600, 800 |
| `charleston-pergola-patio` | 1600, 800 | | `summerville-fire-pit-patio-with-pergola` | 1600, 800 |
| `charleston-pergola-patio-2` | 1600, 800 | | `summerville-neighborhood-brick-pillar-entrance` | 1600, 800 |
| `charleston-sabal-palm-and-pine-landscape-design` | 1600, 800 | | `summerville-neighborhood-landscaping` | 1600, 800 |
| `charleston-stepping-stone-paver-walkway-installation` | 1600, 800 | | `summerville-outdoor-bar-with-painted-paneling` | 1600, 800 |
| `charleston-tabby-firepit-retaining-wall` | 1600, 800 | | `summerville-outdoor-kitchen-island` | 1600, 800 |
| `charleston-wood-privacy-fence` | 1600, 800 | | `summerville-outdoor-kitchen-pergola` | 1600, 800 |
| `custom-outdoor-kitchen-1ddb` | 1600, 800 | | `summerville-patio-steps-with-white-railings` | 1600, 800 |
| `custom-outdoor-kitchen-patio-design-1bb1` | 1600, 800 | | `summerville-pergola-over-an-outdoor-kitchen` | 1600, 800 |
| `folly-beach-backyard-path` | 1600, 800 | | `tabby-firepit-retaining-wall` | 1600, 800 |
| `historic-brick-paver-driveway-installation-6ed2` | 1600, 800 | | `west-ashley-backyard-entertainment-patio-seating-area` | 1600, 800 |
| `james-island-backyard-path` | 1600, 800 | | `west-ashley-pool-house-storage-shed-door` | 1600, 800 |
| `james-island-custom-fence-gate` | 1600, 800 | | | |
| `james-island-entry-gates-3` | 1600, 800 | | | |
| `james-island-herringbone-brick-pathway-installation` | 1600, 800 | | | |
| `louvered-pergola-over-a-paver-patio` | 1600, 800 | | | |
| `mount-pleasant-gravel-driveway-and-slat-fence` | 1600, 800 | | | |
| `mount-pleasant-interior-window-view-landscape-design` | 1600, 800 | | | |
| `mount-pleasant-open-rafter-pool-pavilion` | 1600, 800 | | | |
| `mount-pleasant-pool-pavilion-bathroom` | 1600, 800 | | | |
| `mount-pleasant-pool-pavilion-outdoor-kitchen` | 1600, 800 | | | |
| `mount-pleasant-stepping-stone-paver-walkway` | 1600, 800 | | | |
| `mount-pleasant-stepping-stone-paver-walkway-installation` | 1600, 800 | | | |

Several of these are exactly the "80+ pergola/pavilion masters" `PROJECT-NOTES.md` says exist for
future blog posts (`pergola-patio`, `pergola-patio-2`, `outdoor-kitchen-pergola-ab2a`,
`louvered-pergola-over-a-paver-patio`...) — unused inventory, not a defect. A few pairs here are
mutually-orphaned duplicates of each other (e.g. `charleston-pergola-patio` / `pergola-patio`,
`neighborhood-brick-pillar-entrance-89ec` / `summerville-neighborhood-brick-pillar-entrance`) — same
dead content under two names, neither one live.

### Renamed orphans (57) — dead alternate name; the photo is live under another name

<details><summary>Full list (57 rows)</summary>

| Dead alternate name | Same photo is actually live as |
|---|---|
| `artificial-turf-putting-green-pergola-kitchen-b815` | `summerville-artificial-turf-putting-green-pergola-kitchen` |
| `backyard-artificial-turf-pool-landscaping-d602` | `james-island-backyard-artificial-turf-pool-landscaping` |
| `brick-steps-front-entryway-landscaping-5409` | `charleston-brick-steps-front-entryway-landscaping` |
| `brick-walkway-edging-modern-plantings-f265` | `charleston-brick-walkway-edging-modern-plantings` |
| `charleston-backyard-pergola-swing-pavers` | `backyard-pergola-swing-pavers` |
| `charleston-entry-gates` | `james-island-entry-gates` |
| `charleston-entry-gates-2` | `james-island-entry-gates-2` |
| `charleston-entry-gates-stepping-stones` | `james-island-entry-gates-stepping-stones` |
| `charleston-front-yard-landscaping` | `charleston-stucco-flood-wall-with-iron-fence` |
| `charleston-tabby-fire-pit-sitting-wall` | `tabby-fire-pit-sitting-wall` |
| `charleston-tabby-fire-pit-with-adirondack-seating` | `tabby-fire-pit-with-adirondack-seating` |
| `covered-poolside-patio-cabana-with-seating-d544` | `west-ashley-covered-poolside-patio-cabana-with-seating` |
| `curved-stucco-retaining-wall-brick-steps` | `charleston-curved-stucco-retaining-wall-brick-steps` |
| `custom-concrete-driveway-brick-borders-9230` | `charleston-custom-concrete-driveway-brick-borders` |
| `custom-outdoor-kitchen-c6d2` | `summerville-custom-outdoor-kitchen` |
| `daniel-island-artificial-turf-front-lawn` | `charleston-residential-turf-lawn-landscaping` |
| `daniel-island-flagstone-stepping-stone-pathway` | `charleston-flagstone-stepping-stone-pathway` |
| `daniel-island-lawn-landscaping-brick-border` | `charleston-lawn-landscaping-brick-border` |
| `daniel-island-luxury-home-landscaping-design` | `luxury-home-landscaping-design-e5b7` |
| `daniel-island-pergola-over-an-outdoor-kitchen` | `daniel-island-open-pergola-with-a-seating-wall` |
| `daniel-island-pergola-over-an-outdoor-kitchen-2` | `daniel-island-covered-pergola-with-a-metal-roof` |
| `daniel-island-residential-turf-lawn-landscaping` | `charleston-residential-turf-lawn-landscaping` |
| `daniel-island-salt-void-stepping-stones` | `charleston-salt-void-stepping-stones` |
| `daniel-island-side-yard-artificial-turf-pathway` | `charleston-side-yard-artificial-turf-pathway` |
| `daniel-island-stepping-stone-lawn-pathway` | `charleston-stepping-stone-lawn-pathway` |
| `daniel-island-tabby-fire-pit-sitting-wall` | `tabby-fire-pit-sitting-wall` |
| `folly-beach-backyard-plantings-pathway` | `james-island-backyard-plantings-pathway` |
| `front-porch-stone-steps-landscaping-a9b8` | `charleston-front-porch-stone-steps-landscaping` |
| `james-island-brick-walkway-night-lighting` | `charleston-brick-walkway-night-lighting` |
| `james-island-brick-walkway-path-lighting-at-night` | `charleston-brick-walkway-path-lighting-at-night` |
| `james-island-custom-wooden-outdoor-shower` | `mount-pleasant-custom-wooden-outdoor-shower` |
| `james-island-front-entry-steps-lighting-at-night` | `charleston-front-entry-steps-lighting-at-night` |
| `johns-island-backyard-pathway-plantings-pergola` | `james-island-backyard-pathway-plantings-pergola` |
| `johns-island-bluestone-path-japanese-maple-plantings` | `bluestone-path-japanese-maple-plantings-7ed7` |
| `johns-island-pergola-bluestone-path` | `pergola-bluestone-path-bfe5` |
| `johns-island-pergola-japanese-maple-landscaping` | `james-island-pergola-japanese-maple-landscaping` |
| `johns-island-pergola-with-bluestone-path` | `james-island-pergola-with-bluestone-path` |
| `johns-island-plantings-pathway` | `plantings-pathway-cf16` |
| `johns-island-wooden-arbor-bluestone-walkway` | `james-island-wooden-arbor-bluestone-walkway` |
| `modern-pergola-kitchen-d406` | `summerville-modern-pergola-kitchen` |
| `mount-pleasant-custom-outdoor-kitchen` | `mount-pleasant-pool-pavilion-kitchen-glulam-beams` |
| `mount-pleasant-exposed-aggregate-driveway-landscaping` | `mount-pleasant-plantation-mix-gravel-driveway` |
| `mount-pleasant-travertine-patio` | `summerville-travertine-patio` |
| `mount-pleasant-travertine-patio-and-porch-steps` | `summerville-travertine-patio-and-porch-steps` |
| `north-charleston-bluestone-patio-and-new-lawn` | `north-charleston-bluestone-patio-turf-and-plant-bed` |
| `outdoor-kitchen-patio-landscaping-a32c` | `summerville-outdoor-kitchen-patio-landscaping` |
| `outdoor-kitchen-stone-bar-patio-bcf0` | `summerville-outdoor-kitchen-stone-bar-patio` |
| `poolside-cabana-with-stepping-stone-walkway-a77e` | `west-ashley-poolside-cabana-with-stepping-stone-walkway` |
| `poolside-herringbone-pavers-landscaping-0d98` | `james-island-poolside-herringbone-pavers-landscaping` |
| `residential-outdoor-kitchen-pavilion-design-cad2` | `charleston-residential-outdoor-kitchen-pavilion-design` |
| `stone-outdoor-kitchen-b509` | `summerville-stone-outdoor-kitchen` |
| `stucco-granite-outdoor-kitchen-7f23` | `summerville-stucco-granite-outdoor-kitchen` |
| `sullivans-island-backyard-fire-pit-on-artificial-turf` | `backyard-fire-pit-on-artificial-turf-5eda` |
| `sullivans-island-waterfront-backyard-pool-and-lawn` | `waterfront-backyard-pool-and-lawn-b5cd` |
| `sullivans-island-waterfront-pool-and-artificial-turf` | `waterfront-backyard-pool-and-lawn-b5cd` |
| `travertine-patio-and-porch-steps-2469` | `summerville-travertine-patio-and-porch-steps` |
| `west-ashley-haint-blue-tongue-and-groove-cabana-ceiling` | `west-ashley-haint-blue-plywood-cabana-ceiling` |

</details>

Note the last three rows: `sullivans-island-waterfront-pool-and-artificial-turf` is the filename
`PROJECT-NOTES.md`'s 2026-09-20 fix renamed the old "-and-lawn" file *to* — and it is **itself now
also an orphan**, sitting unused next to the very "-and-lawn" name it was meant to replace. Neither
is live; a third, hex-suffixed copy is (see the Town labels section below). Likewise
`west-ashley-haint-blue-tongue-and-groove-cabana-ceiling` is a dead byte-identical twin of the
"beadboard" ceiling photo `PROJECT-NOTES.md:1091` corrected the wording for — the old material name
survives only in this unused filename, not on any page.

## 4. Town labels — Kiawah Island, Sullivan's Island, Folly Beach, Johns Island

**Result: 0 defects, confirmed on all 74 live pages.** Every `alt="..."`, `title="..."`,
`<figcaption>...</figcaption>` and portfolio-grid `pj-card-town` label across the full live snapshot
(and, separately, the full sandbox) was checked for the four town names — **zero** contain "Kiawah",
"Sullivan's/Sullivans Island", "Folly Beach" or "Johns Island." This re-confirms `DECISIONS.md` #35
three days later; nothing regressed.

**Every real photo on the four no-photo-town pages is labelled "Charleston area,"** per
`PROJECT-NOTES.md`'s rule. All 14 image slots across the four pages, as rendered live:

| Page | File | Rendered label |
|---|---|---|
| `kiawah-island-sc.html` | `luxury-home-landscaping-design-e5b7` | alt = title = "Luxury home landscaping design by Cramers Landscaping, Charleston area" |
| `kiawah-island-sc.html` | `pergola-japanese-maple-landscaping-ef9c` | alt = title = "Pergola japanese maple landscaping by Cramers Landscaping, Charleston area" |
| `folly-beach-sc.html` | `pergola-covered-outdoor-bar-patio-68d7` | CSS hero background image, no alt/title (H1 "Landscaping & Outdoor Living on Folly Beach, SC" is the accessible text) |
| `folly-beach-sc.html` | `covered-patio-outdoor-bar-lounge-6052` | alt = title = "Covered patio outdoor bar lounge by Cramers Landscaping, Charleston area" |
| `folly-beach-sc.html` | `custom-wooden-outdoor-shower-6fa6` | alt = title = "Custom wooden outdoor shower by Cramers Landscaping, Charleston area" |
| `folly-beach-sc.html` | `rustic-outdoor-kitchen-and-porch-d081` | alt = title = "Rustic outdoor kitchen and porch by Cramers Landscaping, Charleston area" |
| `sullivans-island-sc.html` | `waterfront-backyard-pool-and-lawn-b5cd` | alt = title = "Waterfront backyard pool and lawn by Cramers Landscaping, Charleston area" |
| `sullivans-island-sc.html` | `backyard-fire-pit-on-artificial-turf-5eda` | alt = title = "Backyard fire pit on artificial turf by Cramers Landscaping, Charleston area" |
| `sullivans-island-sc.html` | `pool-pavilion-36c7` | alt = title = "Pool pavilion by Cramers Landscaping, Charleston area" |
| `johns-island-sc.html` | `backyard-pathway-plantings-pergola-8092` | CSS hero background image, no alt/title (H1 "Landscaping & Outdoor Living on Johns Island, SC" is the accessible text) |
| `johns-island-sc.html` | `pergola-bluestone-path-bfe5` | alt = title = "Pergola bluestone path by Cramers Landscaping, Charleston area" |
| `johns-island-sc.html` | `pergola-japanese-maple-landscaping-ef9c` | alt = title = "Pergola japanese maple landscaping by Cramers Landscaping, Charleston area" |
| `johns-island-sc.html` | `bluestone-path-japanese-maple-plantings-7ed7` | alt = title = "Bluestone path japanese maple plantings by Cramers Landscaping, Charleston area" |
| `johns-island-sc.html` | `plantings-pathway-cf16` | alt = title = "Plantings pathway by Cramers Landscaping, Charleston area" |

None uses `<figcaption>` — that markup only appears in the portfolio/homepage gallery style, not
these pages' inline layout. Sandbox matches live on every one of these 14 rows.

**Filename-vs-label disagreement:** 12 `assets/work/` base images literally name one of the four
towns (`folly-beach-*` ×2, `johns-island-*` ×7, `sullivans-island-*` ×3 — **0 files are named
`kiawah-*`**). Per the brief, filename-only disagreement is not itself a defect — and here it can't
be one, because **every single one of these 12 is an orphan** (11 renamed, 1 true — see Section 3),
never rendered on any live or sandbox page:

| Filename names | Base | Status |
|---|---|---|
| Johns Island | `johns-island-backyard-pathway-plantings-pergola` | renamed orphan → live as `james-island-backyard-pathway-plantings-pergola` |
| Johns Island | `johns-island-bluestone-path-japanese-maple-plantings` | renamed orphan → live as `bluestone-path-japanese-maple-plantings-7ed7` (the "Charleston area" file above) |
| Johns Island | `johns-island-pergola-bluestone-path` | renamed orphan → live as `pergola-bluestone-path-bfe5` (the "Charleston area" file above) |
| Johns Island | `johns-island-pergola-japanese-maple-landscaping` | renamed orphan → live as `james-island-pergola-japanese-maple-landscaping` |
| Johns Island | `johns-island-pergola-with-bluestone-path` | renamed orphan → live as `james-island-pergola-with-bluestone-path` |
| Johns Island | `johns-island-plantings-pathway` | renamed orphan → live as `plantings-pathway-cf16` (the "Charleston area" file above) |
| Johns Island | `johns-island-wooden-arbor-bluestone-walkway` | renamed orphan → live as `james-island-wooden-arbor-bluestone-walkway` |
| Sullivan's Island | `sullivans-island-backyard-fire-pit-on-artificial-turf` | renamed orphan → live as `backyard-fire-pit-on-artificial-turf-5eda` (the "Charleston area" file above) |
| Sullivan's Island | `sullivans-island-waterfront-backyard-pool-and-lawn` | renamed orphan → live as `waterfront-backyard-pool-and-lawn-b5cd` (the "Charleston area" file above) |
| Sullivan's Island | `sullivans-island-waterfront-pool-and-artificial-turf` | renamed orphan → live as `waterfront-backyard-pool-and-lawn-b5cd` |
| Folly Beach | `folly-beach-backyard-plantings-pathway` | renamed orphan → live as `james-island-backyard-plantings-pathway` |
| Folly Beach | `folly-beach-backyard-path` | **true orphan** — this shot isn't live under any name |

This is precisely the `PROJECT-NOTES.md` "Johns Island — corrected 2026-09-21, this is a JAMES
ISLAND job" situation, still holding: the site never rebuilt a Johns Island page from those files;
the real James Island photos serve James Island's own pages, and separate hex-suffixed generic
copies (proven byte-identical, not assumed) serve the four no-photo towns under "Charleston area."

**Incidental, adjacent finding (not a town-label defect — flagging because it turned up directly in
this file's hashing, not from a separate sweep):** the file actually rendered on
`sullivans-island-sc.html`, `waterfront-backyard-pool-and-lawn-b5cd`, is byte-identical (confirmed by
hash, and the image was viewed directly to confirm it shows artificial turf, not grass) to
`charleston-waterfront-backyard-pool-and-lawn`, which **is** correctly captioned "Waterfront backyard
pool and **artificial turf lawn** in Charleston, SC" where it's used on
`does-artificial-grass-save-money-charleston.html` and `concrete-pool-decks.html`. The copy on the
Sullivan's Island page still carries the pre-fix wording, "Waterfront backyard pool **and lawn**...,"
with no mention of turf. The town label itself is fine (it says "Charleston area," not Sullivan's
Island), so this isn't a Task 8 defect — but it's the same "photo trap" `PROJECT-NOTES.md` already
documented for this exact image, resurfacing under the hex-suffixed duplicate. Out of this task's
core scope to chase further (that's a wording sweep, not a town/orphan/duplicate question).

## 5. Duplicates

**149 byte-identical groups, 330 files, 181 files beyond one canonical copy per group (~36.8 MB).**
Three shapes:

- **82 groups** have exactly one referenced member (the rest are already listed as "renamed orphans"
  in Section 3 — not repeated here).
- **34 groups** have zero referenced members (both/all names dead — already inside the "true
  orphans" table in Section 3, since each name independently qualifies).
- **33 groups have 2+ differently-named copies that are each actually used somewhere** — the
  genuinely new case, and the one that matters for town labels: a real job photo, correctly
  attributed on its own town's page, reused a second time as generic "Charleston area" filler on one
  of the four no-photo towns. Both captions are independently true; nothing conflicts. Collapsing
  each base's `-800`/`-1600` pair into one row (most of these 33 are the same photo's two sizes,
  each byte-identical to the matching size of its twin), that's **16 distinct photos**, listed below.

Page counts below are **live pages only** (the 74-page snapshot), counted per distinct URL so the
`index.html`/`home.html` and bare-slug/`blog__`-slug naming differences between sandbox and live
don't inflate anything.

| Live under name A (page) | AND live under name B (page) | Dead extra name(s) |
|---|---|---|
| `charleston-luxury-home-landscaping-design` (20 live pages) | `luxury-home-landscaping-design-e5b7` (`kiawah-island-sc.html`) | `daniel-island-luxury-home-landscaping-design` |
| `charleston-waterfront-backyard-pool-and-lawn` (5 live pages) | `waterfront-backyard-pool-and-lawn-b5cd` (`sullivans-island-sc.html`) | `sullivans-island-waterfront-backyard-pool-and-lawn`, `sullivans-island-waterfront-pool-and-artificial-turf` |
| `backyard-fire-pit-on-artificial-turf-5eda` (`sullivans-island-sc.html`) | `charleston-backyard-fire-pit-on-artificial-turf` (2 live pages) | `sullivans-island-backyard-fire-pit-on-artificial-turf` |
| `isle-of-palms-pool-pavilion` (5 live pages) | `pool-pavilion-36c7` (`sullivans-island-sc.html`) | — |
| `backyard-pathway-plantings-pergola-8092` (`johns-island-sc.html`) | `james-island-backyard-pathway-plantings-pergola` (2 live pages) | `johns-island-backyard-pathway-plantings-pergola` |
| `bluestone-path-japanese-maple-plantings-7ed7` (`johns-island-sc.html`) | `james-island-bluestone-path-japanese-maple-plantings` (5 live pages) | `johns-island-bluestone-path-japanese-maple-plantings` |
| `james-island-pergola-bluestone-path` (13 live pages) | `pergola-bluestone-path-bfe5` (`johns-island-sc.html`) | `johns-island-pergola-bluestone-path` |
| `james-island-pergola-japanese-maple-landscaping` (`pergolas.html`, `project-james-island-woodland-garden.html`) | `pergola-japanese-maple-landscaping-ef9c` (`kiawah-island-sc.html`, `johns-island-sc.html`) | `johns-island-pergola-japanese-maple-landscaping` |
| `james-island-plantings-pathway` (`blog.html`) | `plantings-pathway-cf16` (`johns-island-sc.html`) | `johns-island-plantings-pathway` |
| `covered-patio-outdoor-bar-lounge-6052` (`folly-beach-sc.html`) | `james-island-covered-patio-outdoor-bar-lounge` (2 live pages) | — |
| `custom-wooden-outdoor-shower-6fa6` (`folly-beach-sc.html`) | `mount-pleasant-custom-wooden-outdoor-shower` (4 live pages) | `james-island-custom-wooden-outdoor-shower` |
| `james-island-pergola-covered-outdoor-bar-patio` (6 live pages) | `pergola-covered-outdoor-bar-patio-68d7` (`folly-beach-sc.html`) | — |
| `james-island-rustic-outdoor-kitchen-and-porch` (8 live pages) | `rustic-outdoor-kitchen-and-porch-d081` (`folly-beach-sc.html`) | — |
| `charleston-artificial-turf-front-lawn` (`blog.html`, `blog__does-artificial-grass-save-money-charleston.html`) | `charleston-residential-turf-lawn-landscaping` (`blog__artificial-turf-vs-natural-grass...html`) | `daniel-island-artificial-turf-front-lawn`, `daniel-island-residential-turf-lawn-landscaping` |
| `entry-gates-stepping-stones-4f5f` (`charleston-sc.html`) | `james-island-entry-gates-stepping-stones` (`project-james-island-woodland-garden.html`) | `charleston-entry-gates-stepping-stones` |
| `north-charleston-bluestone-patio-and-artificial-turf` (3 live pages) | `north-charleston-bluestone-patio-turf-and-plant-bed` (3 live pages) | `north-charleston-bluestone-patio-and-new-lawn` |

The first 13 rows are the four no-photo towns' generic photos, each traced to the real job it's
actually a photo of. The last 3 rows are unrelated to town labels (Charleston/Daniel Island turf
naming and North Charleston's already-fixed lawn→turf rename, both landing on the same conclusion:
old name dead, current name correctly worded).

**One more oddity, unrelated to naming:** `west-ashley-live-oak-spanish-moss-uplighting-at-night`'s
`-800` and `-1600` files are byte-identical to **each other** — the "1600" variant isn't actually a
larger image, just a copy of the 800 one under the bigger-size name. Cosmetic (no broken layout,
since width/height attributes still reserve the right aspect ratio); flagging because it turned up in
the same hash pass.

**Context:** `PROJECT-NOTES.md` records a 72-file duplicate cleanup on 2026-09-20 with the identical
signature (vendor-era hex-suffixed or wrong-town-prefixed copy of a properly-named file). This
sweep's 181 redundant files are the same class of leftover — either not fully swept that day or
re-accumulated since; nothing in this repo dates the individual files precisely enough to say which.
No action taken; the brief for this task is diagnosis only.

---

**Note by the parent cloud session, 2026-09-27 03:20Z.** The `blog.html` "drift" above is not a site
defect. This branch had not yet pulled `6154b35`, the local session's lighting merge, which removed
that card. After merging `origin/Site-revamp`, the sandbox `blog.html` has 21 cards, matching live.
