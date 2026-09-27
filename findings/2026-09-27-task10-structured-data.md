# Task 10 — JSON-LD / structured data audit — 2026-09-27

Diagnosis only. Nothing edited, nothing committed. Scope: all 74 live pages, fetched fresh into
`scratchpad/live2/*.html` and listed in `scratchpad/live-urls.txt`. Extracted every
`<script type="application/ld+json">` block with a Python regex, parsed each with `json.loads`
(handling `@graph` arrays and bare arrays of objects), then recursively walked every nested object
so `areaServed`, `address`, `founder`, etc. are covered, not just top-level nodes. Scripts used:
`extract_jsonld.py`, `check_breadcrumbs.py`, `check_faq.py` (all in the scratchpad, not the repo).

227 JSON-LD blocks total across 74 pages (17 pages ×2 blocks, 35 ×3, 22 ×4). Version of record used
for comparison: name **Cramers Landscaping**, telephone **(843) 614-9773**, address **9153 Markleys
Grove Blvd, Summerville, SC 29485**, url **https://cramerslandscaping.com** (`CLOUD-TASKS.md`
Standing rules; `DECISIONS.md` #15, #59, #61, #72).

## Summary by check

1. **JSON that fails to parse — clean.** 0 of 227 blocks failed. No entity-escaping, no trailing
   commas, no truncation.
2. **Duplicate `@type`s on one page — clean.** Every singleton type (`BreadcrumbList`, `FAQPage`,
   `WebPage`, `WebSite`, `Organization`, `LocalBusiness`/`HomeAndConstructionBusiness`, `Article`,
   `CollectionPage`) appears at most once per page, on all 74 pages. The **duplicate `BreadcrumbList`
   on 73 pages fixed per DECISIONS.md #15 has not regressed.** Types that legitimately repeat
   per page — `Question`/`Answer` (FAQ entries), `City` (12 per `areaServed`), `ImageObject` (2-3:
   primary image, logo, sometimes an author avatar), `ListItem` (breadcrumb rungs), 2×
   `OpeningHoursSpecification` (weekday/Saturday), 2× `Person` (Doug + Zach as founders) — are
   distinct real entities, not copy-paste duplicates. No page has two conflicting definitions of the
   same `@id`, and no page repeats a byte-identical script block.
3. **NAP inconsistency — 2 defects, both below.** `telephone` and the `LocalBusiness`/`Organization`
   `name` are otherwise fully consistent; **no casing/apostrophe variant of the brand name
   ("Cramer's Landscaping", "cramers landscaping", etc.) exists anywhere in live JSON-LD** — the old
   lower-cased `HomeAndConstructionBusiness` block noted in DECISIONS.md #59/#61 is confirmed absent
   from every rendered page, consistent with it being inert.
4. **`843-709-6140` in any format — clean.** Zero occurrences in any of the 74 live pages, any
   sandbox `*.html`, `chat-widget.js`, or any other repo file. The only matches for the digits are in
   `CLOUD-TASKS.md` and `DECISIONS.md`, which is the rule being recorded, not a leak.
5. **BreadcrumbList problems — clean.** All 73 pages that carry one: positions run exactly `1..n`,
   every `item` URL is a real `live-urls.txt` entry (0 invalid, 0 trailing-slash-only mismatches),
   the last item's URL always equals the page's own URL, and every name — including the 6
   mid-trail categories (Home, Services, Blog, Landscaping, Hardscaping, Outdoor Structures,
   Portfolio) — correctly names its target page. `home.html` carries no `BreadcrumbList`, which is
   normal for a homepage, not a defect.
6. **FAQPage vs visible FAQ — 2 defects out of 311 Q/A pairs on 56 pages** (below). One additional
   pair differs by a stray space before a period in the *visible* HTML only (not a JSON-LD problem,
   words identical) — excluded as formatting.
7. **priceRange / aggregateRating / review / offers / price / award — clean.** Zero instances of any
   of these keys anywhere in JSON-LD on any of the 74 pages. Nothing to reconcile against visible
   content because nothing is asserted.
8. **Other — clean.** `@context` present on all 227 blocks (none missing). Zero `http://` (non-`s`)
   URLs in any JSON-LD string value, site-wide. 10/10 spot-checked image URLs returned HTTP 200 live
   (see Method notes).

## Defects

| Page(s) | Block / type | Field | Found value | Correct value |
|---|---|---|---|---|
| All 74 pages | `WebSite` | `name` | `"cramerslandscaping.com"` | `"Cramers Landscaping"` |
| `/` (home.html) and `/contact-us/` | `LocalBusiness`/`HomeAndConstructionBusiness` → `address` (`PostalAddress`) | `postalCode` | key absent — no postal code at all | `"29485"` |
| `/blog/outdoor-living-space-cost-charleston/` | `FAQPage` → `mainEntity[3]`/`[4]` | order | JSON-LD position 3 = "Why does an outdoor kitchen range from $8,000 to $20,000 or more?", position 4 = "What makes a pergola or pavilion cost more?" | Visible page order is the reverse: position 3 = "What makes a pergola or pavilion cost more?", position 4 = the kitchen question. Both Q&A pairs are complete and accurate — only the pairing/order is swapped, an adjacent transposition. |
| `/blog/top-10-landscape-lighting-ideas-to-transform-your-outdoor-space/` | `FAQPage` → `mainEntity[4].acceptedAnswer` | `text` | `"Yes. Every system needs a transformer and a timer, and the nicer controllers can be run from an app on your phone."` | Visible answer: `"Yes, and we recommend a timer over a photocell. Every system needs a transformer and a timer, and the nicer controllers can be run from an app on your phone."` — JSON-LD silently drops the timer-over-photocell recommendation. |

## Informational only (not defects — formatting differences on an otherwise-correct value)

| Page(s) | Field | Found value | Version of record | Why informational |
|---|---|---|---|---|
| `/` and `/contact-us/` (the only 2 pages with a `LocalBusiness` node) | `telephone` | `"+1-843-614-9773"` | `(843) 614-9773` | Same digits, international-dash format vs domestic-parens format. Per task instructions, formatting-only phone differences are informational. |
| All 74 pages (`Organization`/`WebSite` `url`; both pages' `LocalBusiness` `url`) | `url` | `"https://cramerslandscaping.com/"` | `https://cramerslandscaping.com` | Trailing slash only. Matches the site's own canonical scheme — every one of the 74 `live-urls.txt` entries (including the homepage) uses a trailing slash — so this is the consistent, correct live form, not drift. |

## Method notes / spot-checks

- **843-709-6140 sweep:** regex `(\+?1[\s\-.]?)?\(?843\)?[\s\-.]?709[\s\-.]?6140` (also plain
  `7096140`/`709.6140`/`709 6140`) run case-insensitively over `scratchpad/live2/*.html` (all 74) and
  over the whole `/home/user/Website_Sandbox` tree. Zero hits in any `.html`/`.js`/asset file; the
  only hits are the rule itself in `CLOUD-TASKS.md:159,230,334` and `DECISIONS.md:36,51,180`.
- **Image URL spot-check (10/63 distinct JSON-LD image URLs, sequential `curl -sI` against the live
  site):** the shared logo, the shared blog-author avatar, the shared `hero-poster-3.webp`, and 7
  distinct page thumbnails chosen to spread across service/blog/project/town pages (including two
  oddly hash-suffixed filenames — `pergola-covered-outdoor-bar-patio-68d7-1600-1.webp` and
  `waterfront-backyard-pool-and-lawn-b5cd-1600.webp` — as the likeliest candidates for a broken
  reference). **All 10 returned HTTP 200.** Not exhaustive of all 63 distinct image URLs referenced.
- **FAQ comparison** normalised both sides (HTML-entity decode, tag strip, curly→straight quotes,
  em/en dash → hyphen, whitespace collapse) before comparing question text to `Question.name` and
  answer text to `acceptedAnswer.text`, per `<details><summary>Q</summary><p>A</p></details>` inside
  `<div class="cl-faq">` — the same markup pattern on all 56 FAQ pages (verified no multi-`<p>`
  answers, no nested `<div>`s, so nothing was truncated by the extraction).
- **NAP name search** matched every `name` field anywhere in JSON-LD containing "cramer"
  case-insensitively (not just on business-typed nodes), plus a second raw-text regex pass for any
  `cramer's?\s*landscaping` spelling anywhere in the JSON (any field), to catch a variant hiding
  outside the `name` key. Only the `WebSite.name` finding above and ordinary page-title strings
  (e.g. `"... | Cramers"`) matched.
