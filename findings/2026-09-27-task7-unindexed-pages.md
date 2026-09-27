# Task 7: content verdicts on the three unindexed pages (2026-09-27, cloud session)

Diagnosis only. No page, generator or other findings file was changed.

**How this was checked.** Everything was measured on the live snapshot (`live2/`, fetched 02:42Z). The three pages were also re-fetched live with a Googlebot user agent. Each returned HTTP 200 with the same bytes as the snapshot. Each is self-canonical, `index, follow`, has no `X-Robots-Tag`, and is in the sitemap. **There is no technical block on any of them.**

**Changed since the brief.** The lighting post now 301s to `/landscape-lighting/` (commit `6154b35`, verified live). So three pages are unindexed, not four. Every count below is over the **73 pages that still resolve**.

**Google has never seen the current copy of any of them.** It last crawled them on 09-03, 09-16 and 09-17. The earliest sandbox version of each page is from 09-18.

**Why the 8-gram figures look reassuring and the topic read does not.** All three pages are 85-92% textually unique. None shares more than 3.1% of its 8-grams with its real competitor. Yet a fact-by-fact read, checked with regex across all 73 pages, finds heavy overlap on all three. The overlap is the same facts in different words, which shingles cannot see (the method limit recorded in `DECISIONS.md` on 09-26).

## Summary

| | `/services/` | `/blog/pool-pavilion-charleston-sc/` | `/blog/outdoor-living-space-ideas-charleston/` |
|---|---|---|---|
| Last crawled | 09-17 | 09-03 | 09-16 |
| Main-content words | 539 | 1,131 | 1,381 |
| 8-grams found on no other page | 89.9% | 85.1% | 91.6% |
| Top 3 8-gram matches (share of this page) | `/landscape-installation/` 3.9%, `/summerville-sc/` 3.4%, `/outdoor-structures/` 2.8% | outdoor-kitchen planning post 8.3%, lighting-guide post 8.2%, pergola-vs-pavilion post 6.6%. The first two are only the shared NEC-citation block and blog boilerplate | design-build post 3.8%, add-value post 3.8%, cost post 3.7%. All three are the shared "See It Built" cards and CTA |
| Inbound (linking pages) | all 72 (header and footer); 14 in body; 22 breadcrumbs | 8, all in body | 7, all in body (8 before the lighting redirect). Blog median is 5 |
| Outbound links in main content | 33 internal links to 27 pages; 0 external | 13 to 10 pages; 3 external (SC LLR ×2, NFPA) | 12 to 10 pages; 0 external |
| Real competitor (topic read) | Homepage. For the process: `/outdoor-kitchens/` and the "How We Work" post | `/pergolas-pavilions/` ("Backyard & Pool Pavilions") and `/concrete-pool-decks/` | `/blog/backyard-design-ideas-charleston-sc/` and the cost post. Service hub: `/outdoor-structures/` |
| Substantive reason to decline? | **Yes.** It is a subset of the homepage and of the process pages | **Partly.** About 60% restates two service pages; about 25% is pool-only | **Partly.** Almost every fact is published elsewhere; 5 of its 12 ideas are in an indexed sibling post |
| Verdict | **No change. Wait, and expect it may stay out.** Do not make the process its spine | **No change. Wait.** Fallback below | **No change. Wait.** Fallback below |

---

## 1. `/services/`

- **Title:** "Landscaping & Outdoor Living Services in Charleston, SC"
- **H1:** "Landscape, Hardscape & Outdoor Living Services in Charleston, SC"
- **Meta description:** "Landscape installation, hardscaping, outdoor structures and landscape design in Charleston, SC, designed and built by the Cramer family."
- **Canonical and robots:** self-canonical; index, follow.
- **Body inbound links:** 12 town pages link to `/services/#how-a-project-works` with the anchor "how a project works". The How We Work post and `/contact-us/` link to the page itself.

**What the page is.** About 230 words of catalog: an intro plus three category blocks, linking to 22 service pages. Then "How a Project Works" (204 words), three project cards and a CTA.

**What it duplicates.**
- **The catalog is the homepage's.** The homepage block "Everything for your outdoor living, under one roof" uses the same three categories.
  - 24 of the 27 pages `/services/` links to are also linked from the homepage body.
  - All but one of its service links are in the header menu or on the homepage. The exception is Grading, which 24 other pages link to.
  - Its 8-gram overlap with the homepage is 0.0%, which is why the shingle test never caught this.
  - The titles are close ("Landscaping & Outdoor Living in Charleston, SC | Cramers"), but `/portfolio/` and `/blog/` share that template and are not unindexed. The title alone is not the cause.
- **The process is `/outdoor-kitchens/`'s.** Its "How We Build Yours" section has the same five steps in the same order with the same figures.
  - Shorter versions are on `/outdoor-structures/` ("How a Project Runs"), `/landscape-installation/` ("How the Work Goes") and `/hardscape-installation/` ("How We Work").
  - The site's dedicated process page is `/blog/why-cramers-landscaping-is-charlestons-top-landscaping-company/`: H1 "How We Work: Design, Build and What Happens After", meta *"How a Cramers project runs: …"*, 1,101 words.

**Testing the 09-26 claim.** The claim was that "How a Project Works" is unique and that "none of that is on any service page". It does not hold:

| Claim in "How a Project Works" | Also published on |
|---|---|
| Doug or Zach comes out in person | `/about/`, `/summerville-sc/`, `/james-island-sc/` |
| Consultation usually within a week of your call | `/outdoor-kitchens/` (twice), `/summerville-sc/` |
| Budget first ("no point designing something you can't afford") | Same idea on `/outdoor-structures/` ("starting with a rough budget"), on `/about/` and in the How We Work post. Only the sentence itself is unique |
| Budget usually within a week of the consultation | `/outdoor-kitchens/` ("Budget within about a week") |
| Drawings, with optional 3D at extra cost | 15 other pages |
| A larger project carries a design fee | `/landscape-installation/` and `/summerville-sc/`, word for word |
| Design takes 1 to 4 weeks; final quote once the design is set | `/outdoor-kitchens/`. "Exact quote once the design is set" is also on `/pergolas/` and `/pergolas-pavilions/` |
| Small jobs skip design, pay nothing for it, and get a quote after the consultation | `/summerville-sc/`: "we do not charge for it, and we quote and plan those right after the consultation" |
| HOA and town-board applications prepared and submitted by us | 13 other pages, including `/outdoor-structures/`, `/landscape-installation/`, `/hardscape-installation/` and five town pages |
| Those reviews fit in **before the permit** | **No other page. This is the one unique fact** |
| Permit 4 to 6 weeks; kitchen and pergola 1 to 3 weeks; pavilion 6 to 8 weeks | `/outdoor-kitchens/` (all three figures), `/pergolas-pavilions/`, `/outdoor-structures/` |

Making the process the spine would therefore create a second "how a Cramers project runs" page, competing with the How We Work post. That swaps overlap with the homepage for overlap with that post, built from facts already published.

**Verdict: no change needed. Wait for the re-crawl, and expect it may stay out.** If a post-rebuild crawl still declines it, treat that as expected and stop counting it as an indexing gap. The reasons:
- **Its job is navigation, which does not need an index slot.** Everything it links to is reachable from the header, the homepage or other body links.
- **The homepage owns its query.** "Landscaping services in Charleston" belongs to the homepage, and an indexed `/services/` would split that query.
- **There is nothing unique to add yet.** No published copy, and nothing recorded from Zach, would give it substance that another page does not already own. Anything new **needs Zach**.
- **Do not noindex or redirect it.** The header "All Services" link and the 12 town-page "how a project works" links use it, and they work for visitors.
- **This hub being declined is not the serious signal the brief feared.** The real category hubs beneath it are substantive and not among the unindexed: `/landscape-installation/` (1,798 words), `/outdoor-structures/` (1,378) and `/hardscape-installation/` (1,081).

## 2. `/blog/pool-pavilion-charleston-sc/`

- **Title:** "Pavilion at a Pool: Deck, Storage and Scale | Cramers"
- **H1:** "Building a Pavilion at a Pool: What Changes"
- **Meta description:** "Building a pavilion at a pool: the deck as its floor, coping and drainage, storage and a bathroom at the back, and whether a pergola would do for less."
- **Canonical and robots:** self-canonical; index, follow.
- **Inbound (8 pages):** `/blog/`, `/pergolas-pavilions/`, `/concrete-pool-decks/`, `/outdoor-shower-installation-charleston-sc/`, and the cost, Mount Pleasant, pergola-vs-pavilion and pool-deck posts.

**The competitor is `/pergolas-pavilions/`, not `/outdoor-structures/` (the page the 09-26 verdict compared against).** `/pergolas-pavilions/` is titled "Backyard & Pool Pavilions in Charleston, SC". Its meta description sells pool pavilions at $30,000 to $90,000+, with "Kitchens, bathrooms and storage at the back". That is the same query as this post, yet the two share only 3.1% of their 8-grams.

| Post section (words) | Also on | Only on this post |
|---|---|---|
| A Pool Changes the Build (54) | nothing | all of it |
| The Deck Is the Pavilion's Floor (142) | `/concrete-pool-decks/`: salt-void at West Ashley, travertine at Mount Pleasant, coping 1.5 to 2 inches, grading then drain basins | wet bare feet; moving water away from the structure |
| Put the Utility Side at the Back (109) | `/pergolas-pavilions/`, "The Back of the Building Is Where the Value Hides" | not walking through the house wet; towels, floats, pump and filter gear, chemicals |
| Scale: $30,000 and $80,000 (84) | `/pergolas-pavilions/`, "What $30,000 Buys, and What $80,000 Buys", nearly word for word; the $10,000 beams | nothing |
| Do You Actually Need a Pavilion Here? (103) | `/pergolas-pavilions/`, `/pergolas/`, pergola-vs-pavilion post | "shade and shelter beside the water … leaves budget for the deck" |
| What the Code Says Around a Pool (243) | The NEC 210.8 paragraphs, "References are to…" and the Sources list, word for word on two or three other posts | **NEC 680.22(A): outlet distances around a pool (6 ft / 20 ft), settled before the slab is poured. On no other page** |
| FAQ (220) | Cost, bathroom and "could a pergola work" are all in the `/pergolas-pavilions/` FAQ; the surface question is covered on `/concrete-pool-decks/` | nothing |

About 290 words (a quarter) are on no other page, counting the five passages named in the table. About 60% restates `/pergolas-pavilions/` and `/concrete-pool-decks/`, and the rest is navigation.

**Verdict: no change needed. Wait for the re-crawl.** The pool-only material is specific, sourced and genuinely additive, which is a legitimate reason to index the post. Trimming the restated sections to chase indexing would cost readers the prices.

**Fallback, only if a post-rebuild crawl still declines it** (the lighting-post pattern; Zach decides):
- Move these passages into `/pergolas-pavilions/`, using the post's own sentences, condensed:
  - the "A Pool Changes the Build" paragraph
  - the utility-side reasons
  - the 680.22(A) paragraph with its three sources
  - the "shade beside the water" line
- 301 the post to `/pergolas-pavilions/`.
- Repoint its 8 inbound links.

## 3. `/blog/outdoor-living-space-ideas-charleston/`

- **Title:** "Outdoor Living Ideas in Charleston, SC, With Real Costs"
- **H1:** "Outdoor Living Ideas, and What Each One Cost"
- **Meta description:** "Twelve ideas from our own Charleston projects, each with the decision behind it and the cost: ceilings, bar rails, fire pits, lighting, turf and patios."
- **Canonical and robots:** self-canonical; index, follow.

**The competitor is the sibling post `/blog/backyard-design-ideas-charleston-sc/`, which is indexed.** Its title is "Backyard Design Ideas in Charleston, SC, With Real Costs", the same template.
- Both are cross-category idea round-ups with costs, anchored to Cramers' own jobs.
- Every price in both is also in the cost post, `/blog/outdoor-living-space-cost-charleston/`.
- The service hub for the topic is `/outdoor-structures/`.

So the 09-26 note that "nothing else on the site does that" does not hold.

What the 12 ideas overlap with:
- **Also in the backyard-ideas post, with the same projects and prices: 5 of 12, about 350 words.**
  - 1, the ceiling (West Ashley, tape light above the beams)
  - 5, the fire pit ($1,000 kit, from $2,500, 6 ft clearance)
  - 6, lighting ($200 a light; uplight one tree)
  - 7, moving water (kit around $1,000, small courtyard)
  - 9, turf where grass fails ($13 including base; shade, dog run)
- **Not in that post, but published elsewhere: 7 of 12.**
  - 2: `/project-mount-pleasant-pool-pavilion/` and the Mount Pleasant post
  - 3: `/outdoor-kitchens/` (the sapele foot rail) and the Summerville project
  - 4: `/outdoor-kitchens/`
  - 8: `/daniel-island-sc/` and `/north-charleston-sc/` ("Hedges are a better answer … than a taller fence")
  - 10: `/outdoor-shower-installation-charleston-sc/`
  - 11 and 12: `/patios-pavers/`
  - The resale section is largely the add-value post.
- **Almost no fact in it is new.** Even the turf-for-games point is on `/artificial-turf-installation/` and `/folly-beach-sc/`. What it adds is framing: a one-line decision per idea, such as "A counter you cook at is a work surface; add a bar top and a rail and it becomes somewhere guests stand and talk to whoever is cooking."

**Verdict: no change needed. Wait for the re-crawl.** Its value is curation: twelve decisions, each with its reason and cost, side by side. It is textually the most original of the three and better linked than most posts. Google has not seen this version.

**Fallback, only if a post-rebuild crawl still declines it** (Zach decides):
- Merge it into the backyard-ideas post rather than rewriting it. Its five shared ideas are already there.
- Carry the other seven across as the post's own sentences, condensed, into the matching sections ("If You Want to Host", "If You Want Somewhere to Sit in the Evening").
- Hedging for privacy and the outdoor shower have no matching section, so each would need a new one.
- Then 301 the post to `/blog/backyard-design-ideas-charleston-sc/`.

The shared title template is worth breaking whenever titles are next touched. It is not worth a deploy on its own, because retitling does not pay at positions 11-50 (`DECISIONS.md` #52).

---

## Method and limits

- **Main content:** `<main>` minus the breadcrumb nav, forms, scripts and JSON-LD, and SVG. A word is a whitespace-separated token containing a letter or digit. The counts are within 1% of the 09-26 figures (543 / 1,139 / 1,391).
- **8-grams:** lowercased word tokens with punctuation stripped. "Share" means this page's 8-grams found on the other page, divided by this page's 8-grams. Sitewide boilerplate (8-grams that appear on 10 or more pages) is 1.9% of each page.
- **Links:** every `<a href>` on each page, classed as header, footer, breadcrumb or body, with fragments stripped.
- **Could not verify:**
  - Which page Google actually ranks for each query. There is no Search Console or Semrush access here, so the competitors above are inferred from titles, meta descriptions and content.
  - What the pre-rebuild pages said when Google crawled them.
  - The index status of the comparator pages. The only source is `DECISIONS.md`, which lists just these pages as crawled but not indexed.

## Noticed in passing (not Task 7)

- **Task 6:** the How We Work post says "The consultation at your home is free." twice (body and FAQ), with no geography qualifier.
- **Task 9:** on the cost post, the anchor "Mount Pleasant pool pavilion" (in the sentence about the beams) links to the pool-pavilion post, not to `/project-mount-pleasant-pool-pavilion/`.

---

**Added by the parent cloud session, 2026-09-27 03:10Z.** Verified the lighting merge (`6154b35`) on
the live site: the exact old URL returns **301 to `/landscape-lighting/`**, but the same URL **with
any query string** (for example `?utm_source=...` or `?cb=1`) still returns **200 and serves the
retired post**. The Redirection rule is matching the exact URL only. Fix: set that rule's query
parameter option to ignore (or pass through) parameters, so tagged links also redirect.
