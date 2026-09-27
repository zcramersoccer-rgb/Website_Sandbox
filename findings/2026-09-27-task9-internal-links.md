# Task 9 — Internal linking and orphan audit

Diagnosis only. No page, generator, or other findings file was touched. Built from the fresh
74-page live snapshot (`scratchpad/live2/*.html`) plus `scratchpad/live-urls.txt` (the canonical
URL list from the live sitemaps), with every canonical target re-confirmed by a direct, unfollowed
`curl -sI` against the live site on 2026-09-27 (~02:57–03:00Z). All counting done with Python
scripts (`html.parser`, no third-party libraries available in this sandbox); self-links never
count toward any total below.

## Summary

- **1 orphan**: `/blog/top-10-landscape-lighting-ideas-to-transform-your-outdoor-space/` — zero
  internal links from any of the other 73 pages, in chrome or content. **While auditing it, its
  live URL turned out to already 301 to `/landscape-lighting/`** (confirmed via the `Redirection`
  plugin's response header), which is not what `CLOUD-TASKS.md` / `DECISIONS.md #88` describe as
  of this session ("Task 4: proposal written, awaiting Zach; do not redirect anything"). Flagged
  below, not acted on.
- **Click depth: nothing deeper than 2.** Every reachable page is 1 or 2 clicks from the home
  page (home=0, 42 pages at depth 1, 30 at depth 2). Nothing to flag for depth >3.
- **2 starved money pages**: `/mulching-bed-maintenance/` (24 distinct referring pages) and
  `/landscape-grading-services-charleston-sc/` (29) — every one of the other 34 money pages sits at
  **73** (i.e., linked from literally every other page). Cause identified precisely: both are
  missing from the header mega-menu (17 service links, on all 74 pages) *and* the footer Services
  list (9 links, on all 74 pages) that every other service page appears in at least one of.
- **Anchor-text profile: no defects found.** Every one of the 36 money pages' single most common
  inbound anchor correctly names that page. The historical defect this exact check caught before
  (75 footer links reading "Pavilions & Pergolas" pointing at the pavilions page) stays fixed: 0
  occurrences of that combined string anywhere on the site now; `/pergolas/` top anchor is
  "Pergolas" (158×), `/pergolas-pavilions/` top anchor is "Pavilions" (160×).
- **Redirects/404s: 1 redirect, 0 broken links** — every one of the 73 distinct internal hrefs that
  actually gets linked to resolves 200 direct. The one redirect is the orphan above, which no
  internal link points at, so it currently wastes no on-site link equity.
- Sitewide, 72.9% of all internal link volume (4,460 of 6,118 non-self links) sits in chrome
  (header/nav/footer) versus content — confirms the brief's premise that chrome inflates raw counts
  and money-page ranking has to look past it.

## Method, briefly

- **Chrome vs. content**: every page has exactly one `<header>`, one `<main>`, one `<footer>` (74/74,
  no exceptions), so a link is "chrome" if it sits inside `<header>`/`<footer>`, or inside **any**
  `<nav>` even when that nav is physically inside `<main>` (breadcrumbs, and the `cl-tabs` cluster
  strip that repeats near-verbatim across sibling service pages) — otherwise it's "content." This
  matches the brief's own examples (`<header>`, `<nav>`, `<footer>`) and is the only way the two
  starved pages don't look artificially healthy (they still pick up 21–30 genuine in-content
  mentions; it's the sitewide menus they're missing from).
- **Normalization**: relative hrefs resolved against `https://cramerslandscaping.com`; `#fragments`
  stripped (13 links carry a real path + fragment, e.g. `/services/#how-a-project-works` — counted
  against `/services/`); scheme/host checked case-insensitively for `http`/`https` and `www`/non-`www`
  parity. **Nothing to normalize there in practice** — every internal `<a>` on the site already uses
  a bare root-relative path (`/services/`); zero absolute, zero `http://`, zero `www.` internal
  hrefs exist. **Zero hrefs carry a query string**, and **zero hrefs are missing/adding a trailing
  slash** relative to their canonical form — checked explicitly, none found.
- **Excluded from the graph** (not "pages," so out of scope for orphan/depth/inbound counts, though
  still visible to the task-5 redirect check by virtue of not needing it — see below): 260
  `tel:`/`mailto:` links, 345 external links (different domains — Task 2's territory), 129
  same-page `#fragment`-only jumps (skip-link, footnote refs, portfolio filter chips), and 132
  absolute `https://cramerslandscaping.com/wp-content/uploads/...` hrefs that are lightbox links to
  full-size images, not pages (all on `/portfolio/` and the 8 `/project-*/` pages).
- **Self-links** (a page linking to itself — mainly the header logo and "Home"/current-tab entries)
  are excluded from every count below: 83 found, all excluded, per the brief ("self-links do not
  count").
- **Money pages (36)**: `/services/` (top hub) + the 3 cluster hubs (`/hardscape-installation/`,
  `/landscape-installation/`, `/outdoor-structures/`) + the 19 individual service pages under them +
  the 12 `-sc/` town pages + `/contact-us/`.

## 1. Orphans

Only one sitemap URL has zero internal links, from anywhere, in any snapshot page:

> **`/blog/top-10-landscape-lighting-ideas-to-transform-your-outdoor-space/`** — 0 distinct
> referring pages, 0 total links, 0 in-content links.

This is the same URL `CLOUD-TASKS.md` Task 4 already flags as the first post-rebuild page Google
re-crawled and still declined to index — being completely unlinked internally is a very plausible
contributor to that, independent of whatever the content verdict said.

**Live discrepancy worth flagging, not fixing here:** re-requesting this exact URL live (not from
the snapshot) returned:

```
HTTP/2 301
location: /landscape-lighting/
x-redirect-by: redirection
```

`x-redirect-by: redirection` is the WordPress "Redirection" plugin — this is a deliberate, configured
rule, live right now, not a cache fluke. But `scratchpad/live-post-sitemap.xml` (captured minutes
earlier in this same session) still lists the pre-redirect URL as a normal entry, and the most
recent log entry (`DECISIONS.md #88`, 02:41–02:45Z) still describes Task 4 as "awaiting Zach" with
"do not delete or redirect anything" in force. Either Zach acted on it in the last few minutes, or
something else did — this audit can't tell which from here. **Recommend whoever reads this next
confirms with Zach before treating Task 4 as resolved**, and if the redirect is meant to stay,
regenerates the sitemap so it stops listing a URL that immediately 301s, and finishes the
content-merge into `/landscape-lighting/` that Task 4's own proposal describes (only some of the
old post's items are covered there today).

No other page in `live-urls.txt` is an orphan. Three pages are linked **only from chrome** (zero
in-content links despite normal chrome reach) — all three are structurally expected, not flagged as
defects: `/` (home; 365 total links, 73 distinct pages, logo/nav only — nothing links back to the
homepage from body copy, which is normal), `/blog/` (95 total, 73 distinct, same pattern), and
`/privacy-policy/` (73 total, 73 distinct, footer-only, as a legal utility page should be). No page
is linked from **only one** distinct page (the smallest is 3 distinct pages — see depth section).

## 2. Click depth from the home page

BFS over the non-self link graph, every one of the 74 pages accounted for:

| Depth | Pages | Notes |
|---:|---:|---|
| 0 | 1 | home page itself |
| 1 | 42 | every money page reachable via the header mega-menu or footer, plus `/about/`, `/blog/`, `/portfolio/`, `/privacy-policy/`, and 3 of the 11 project pages that the homepage links to directly |
| 2 | 30 | all 21 remaining blog posts, 8 remaining project pages, and `/landscape-grading-services-charleston-sc/` (reached via the landscaping cluster tab strip, not directly from home) |
| unreachable | 1 | the orphan above |

**Nothing exceeds depth 3.** Full depth-1 and depth-2 lists (for "every page," as asked):

- **Depth 1 (42):** `/about/`, `/artificial-turf-installation/`, `/blog/`, `/charleston-sc/`,
  `/charleston-sod-installation/`, `/concrete-pool-decks/`, `/concrete-services/`, `/contact-us/`,
  `/daniel-island-sc/`, `/fire-pits/`, `/fireplaces/`, `/folly-beach-sc/`, `/fountain-water/`,
  `/hardscape-installation/`, `/irrigation-system-installation/`, `/isle-of-palms-sc/`,
  `/james-island-sc/`, `/johns-island-sc/`, `/kiawah-island-sc/`,
  `/landscape-drainage-services-charleston-sc/`, `/landscape-installation/`, `/landscape-lighting/`,
  `/mount-pleasant-sc/`, `/mulching-bed-maintenance/`, `/north-charleston-sc/`, `/outdoor-kitchens/`,
  `/outdoor-shower-installation-charleston-sc/`, `/outdoor-structures/`, `/patios-pavers/`,
  `/pergolas-pavilions/`, `/pergolas/`, `/plants/`, `/portfolio/`, `/privacy-policy/`,
  `/project-mount-pleasant-pool-pavilion/`, `/project-mount-pleasant-wellness-center-fountains/`,
  `/project-west-ashley-pool-cabana/`, `/retaining-walls/`, `/services/`, `/sullivans-island-sc/`,
  `/summerville-sc/`, `/west-ashley-sc/`
- **Depth 2 (30):** all 21 blog posts except the orphan and `/blog/` itself, plus
  `/landscape-grading-services-charleston-sc/`, `/project-charleston-live-oak-landscape/`,
  `/project-charleston-stucco-retaining-wall/`, `/project-james-island-rustic-outdoor-kitchen/`,
  `/project-james-island-woodland-garden/`, `/project-mount-pleasant-modern-landscape/`,
  `/project-summerville-pool-patio-kitchen-fireplace/`,
  `/project-summerville-putting-green-pergola-kitchen/`,
  `/project-summerville-stone-fireplace-pool-deck/`

## 3 & 4. Inbound link counts and anchor-text profile, money pages (ranked, most starved first)

Distinct = number of *other* pages carrying at least one link to it; Total = every `<a>` counted;
In-content = the subset of Total inside `<main>` and outside any `<nav>`.

| Page | Type | Distinct pages | Total links | In-content | Distinct anchors | Top anchor (count) |
|---|---|---:|---:|---:|---:|---|
| `/mulching-bed-maintenance/` | service page | **24** | 30 | 21 | 7 | "mulch and bed edging" (14) |
| `/landscape-grading-services-charleston-sc/` | service page | **29** | 39 | 30 | 8 | "grading" (23) |
| `/daniel-island-sc/` | town page | 73 | 86 | 13 | 2 | "Daniel Island" (75) |
| `/services/` | top hub | 73 | 255 | 14 | 4 | "Services" (168) |
| `/north-charleston-sc/` | town page | 73 | 87 | 14 | 3 | "North Charleston" (75) |
| `/kiawah-island-sc/` | town page | 73 | 87 | 14 | 3 | "Kiawah Island" (75) |
| `/johns-island-sc/` | town page | 73 | 89 | 16 | 3 | "Johns Island" (75) |
| `/isle-of-palms-sc/` | town page | 73 | 89 | 16 | 3 | "Isle of Palms" (74) |
| `/sullivans-island-sc/` | town page | 73 | 90 | 17 | 3 | "Sullivan's Island" (79) |
| `/folly-beach-sc/` | town page | 73 | 91 | 18 | 3 | "Folly Beach" (80) |
| `/james-island-sc/` | town page | 73 | 93 | 20 | 2 | "James Island" (74) |
| `/fountain-water/` | service page | 73 | 106 | 24 | 8 | "Water Features" (84) |
| `/hardscape-installation/` | cluster hub | 73 | 182 | 26 | 7 | "Hardscaping" (170) |
| `/outdoor-shower-installation-charleston-sc/` | service page | 73 | 104 | 26 | 5 | "Outdoor Showers" (80) |
| `/outdoor-structures/` | cluster hub | 73 | 184 | 28 | 8 | "Outdoor Structures" (172) |
| `/charleston-sc/` | town page | 73 | 103 | 30 | 3 | "Charleston" (81) |
| `/west-ashley-sc/` | town page | 73 | 103 | 30 | 3 | "West Ashley" (81) |
| `/fireplaces/` | service page | 73 | 109 | 31 | 9 | "Fireplaces" (80) |
| `/retaining-walls/` | service page | 73 | 183 | 32 | 10 | "Retaining Walls" (153) |
| `/summerville-sc/` | town page | 73 | 105 | 32 | 3 | "Summerville" (81) |
| `/mount-pleasant-sc/` | town page | 73 | 107 | 34 | 4 | "Mount Pleasant" (82) |
| `/fire-pits/` | service page | 73 | 119 | 41 | 10 | "Fire Pits" (80) |
| `/concrete-pool-decks/` | service page | 73 | 119 | 41 | 9 | "Pool Decks" (82) |
| `/contact-us/` | contact | 73 | 261 | 42 | 10 | "Contact Us" (95) |
| `/charleston-sod-installation/` | service page | 73 | 125 | 43 | 7 | "Sod" (78) |
| `/concrete-services/` | service page | 73 | 124 | 46 | 13 | "Concrete & Driveways" (74) |
| `/landscape-drainage-services-charleston-sc/` | service page | 73 | 129 | 47 | 8 | "Drainage" (86) |
| `/pergolas/` | service page | 73 | 198 | 47 | 12 | "Pergolas" (158) |
| `/plants/` | service page | 73 | 130 | 48 | 15 | "Plants" (73) |
| `/artificial-turf-installation/` | service page | 73 | 132 | 50 | 9 | "Turf" (73) |
| `/landscape-installation/` | cluster hub | 73 | 215 | 51 | 13 | "Landscape Design & Installation" (153) |
| `/irrigation-system-installation/` | service page | 73 | 133 | 51 | 10 | "Irrigation" (93) |
| `/pergolas-pavilions/` | service page | 73 | 205 | 54 | 16 | "Pavilions" (160) |
| `/outdoor-kitchens/` | service page | 73 | 209 | 58 | 14 | "Outdoor Kitchens" (155) |
| `/landscape-lighting/` | service page | 73 | 223 | 68 | 11 | "Landscape Lighting" (87) |
| `/patios-pavers/` | service page | 73 | 220 | 69 | 23 | "Paver Patios" (77) |

**No misleading top anchor anywhere in this table** — every page's dominant anchor names the page
correctly (town names for town pages, the service name for service pages, "Contact Us", etc.). Full
distinct-anchor lists for the 34 healthy pages are omitted for length (all are minor variants of the
top anchor — plurals, lower-case, or a 1-off image-alt/card caption); none is empty and none points
a different page's name at this one. Full lists for the two starved pages, since their low volume
makes it worth showing completely:

- **`/mulching-bed-maintenance/`** (30 total): "mulch and bed edging" 14, "Mulch & Beds" 10, "mulch" 2,
  "Mulch and bed edging" 1, "mulch and beds" 1, "mulch and edging" 1, "edge and mulch" 1.
- **`/landscape-grading-services-charleston-sc/`** (39 total): "grading" 23, "Grading" 10,
  "Landscape Grading" 1, "landscape grading" 1, "regrade it" 1, "regrading" 1, "Extensive grading on
  a sloped waterfront lot" 1, "Excavation of organic backfill to 10 ft and compacted clean fill" 1.

Both are entirely on-topic — the starvation is structural (missing from two menus), not a wording
problem. No empty anchors and no image-alt anchors point at any money page.

**Non-money pages, for context (not the focus of this task):** the 22 blog posts and 11 portfolio
project pages range from 3–22 distinct referring pages, which is normal for content that's only
reachable editorially (via `/blog/`, `/portfolio/`, and cross-links between posts), not via sitewide
chrome — none is a money page, none is orphaned, and all sit at depth 1–2. Full per-post numbers are
in the JSON this file was built from, not reproduced here to keep the table to what matters.

## 5. Internal links that redirect or 404

75 distinct internal hrefs are written across the 74 pages (2 are the same target with a `#fragment`
appended); they resolve to 73 distinct canonical pages. Every one was requested live with
`curl -sI` (no `-L`), sequentially, ~0.5s apart, on 2026-09-27:

| Result | Count |
|---|---:|
| 200 direct | 73 |
| 301/302/307/308 | 0 (of the 73 that anything actually links to) |
| 404 | 0 |

**The only redirect found in this whole audit is the orphan's own URL** (see section 1) — and
because zero internal hrefs point at it, it costs zero link equity in practice today. Also checked,
as a bonus (it's not written as a href anywhere, but it is a sitemap page): the orphan's own
canonical URL, which is exactly that 301. Beyond that one case, there is nothing to correct at
source: no internal href is missing a trailing slash, none carries `http://` or `www.`, and none
points at a 404.

## Changes worth making, ranked

1. **HIGH — add the 2 missing service pages to the sitewide service menus.** The header mega-menu
   (17 service links, present on all 74 pages: Plants, Sod, Turf, Irrigation, Drainage, Lighting,
   Water Features, Patios, Retaining Walls, Fire Pits, Pool Decks, Concrete & Driveways, Pavilions,
   Pergolas, Outdoor Kitchens, Fireplaces, Outdoor Showers) and the footer Services list (9 links,
   also on all 74 pages) are the reason every other service page sits at 73 distinct referring pages.
   `/mulching-bed-maintenance/` and `/landscape-grading-services-charleston-sc/` are in neither.
   Add two entries to the header mega-menu — `<a href="/mulching-bed-maintenance/">Mulch &amp;
   Beds</a>` and `<a href="/landscape-grading-services-charleston-sc/">Grading</a>` — reusing the
   exact wording the landscaping cluster's own tab strip already uses for these two, which this
   audit confirms is descriptive and already the dominant, correct anchor for each. That alone would
   take both from 24/29 distinct referring pages to 73, matching every sibling service page. (Per
   `DECISIONS.md #69/#82`, the footer Services block is emitted by `nav_money_pages.py`; the header
   mega-menu is likely a sibling generator or the same shell include — grep the rendered `<header>`
   for one of the 17 existing entries, e.g. `Outdoor Showers`, to find the right source, then check
   both the generator and the rendered HTML per the standing "a generator only owns what it wrote"
   rule.)
2. **MEDIUM — confirm the lighting-post redirect before treating Task 4 as settled.** See section 1:
   the live site already 301s the orphaned post to `/landscape-lighting/`, which is ahead of what
   `CLOUD-TASKS.md`/`DECISIONS.md` currently record. Confirm with Zach it was intentional, then (a)
   finish the content-merge Task 4's proposal describes so the redirect target fully covers the old
   post, and (b) let the XML sitemap drop the pre-redirect URL once that's settled. Not a link-equity
   fix — no internal href points at the old URL — just a sequencing gap worth closing before the
   next person re-reads Task 4 and assumes nothing has happened yet.
3. **Nothing else rises to a fix.** Trailing slashes, query strings, protocol/`www` consistency, 404s,
   and click depth are all already clean (checked explicitly, all zero/none). The 3 chrome-only
   pages (`/`, `/blog/`, `/privacy-policy/`) are expected, not defects. The historical "Pavilions &
   Pergolas" anchor defect stays fixed at 0 occurrences — confirmed again here, not just assumed.

---

**Correction and addition by the parent cloud session, 2026-09-27 03:15Z.**

- **The lighting-post redirect was approved.** Zach: *"merge lighting pages"* (`DECISIONS.md` #71),
  applied by the local session in `6154b35`. So ranked fix (2) above needs no confirmation, and the
  "orphan" is simply the retired post, as expected.
- **Real leftover: the retired post is still in the live sitemap.** `https://cramerslandscaping.com/post-sitemap.xml`
  still lists `/blog/top-10-landscape-lighting-ideas-to-transform-your-outdoor-space/`, which now
  301s. That means the WordPress post is still published behind the Redirection rule, which is also
  why the same URL with a query string still serves the old post (see the Task 7 findings). Fix, local
  session: unpublish (draft or trash) that post so it drops out of `post-sitemap.xml`, and set the
  Redirection rule to ignore query parameters.
