# Tasks for the cloud session — queued 2026-09-26

Written by the **Cramers Landscaping company overview** session. You have this repo; it cannot
message you back, so this file is the handover. Read `DECISIONS.md` first — it is the record of
every instruction Zach has given, newest first.

---

## READ THIS BEFORE YOU CHANGE ANY PAGE

**`site-build/` is NOT in this repository.** It is a *sibling directory* on the local machine,
unversioned, and it holds **every generator** plus `deploy_shell.py`, the single PHP snippet that
renders all 74 live pages.

**This matters more than anything else in this file.** The generators re-emit page content on every
run. A fix applied only to sandbox HTML has a half-life of "whenever someone next runs a generator."
**This has silently reverted the same class of fix three times** — the sago palm line, the West
Ashley ceiling wording, and 81 dropped CSS selectors.

**So: if you cannot reach `site-build/`, do not ship page edits.** Do the diagnosis, write the
finding and the proposed change into this file or a new `findings/` file, commit it, and let the
local website-editor session apply it through the generator. **Diagnosis is genuinely the valuable
half** — every task below has been scoped so the analysis stands on its own.

Related rule: **a generator only owns what it wrote.** On 2026-09-25 a rename patched the generator
constant and still missed the one occurrence that was static markup — on the page that mattered most.
Grep the rendered HTML as well as the sources.

---

## Task 1 — Identify the 2 pages with duplicate h1 and title

Semrush Site Audit, campaign **31306158**, flags 2 pages where the `<h1>` and `<title>` are identical.
Semrush credentials are not in this repo; **derive it from the sandbox HTML instead** — parse each
page, compare `<title>` (minus the ` | Cramers` suffix) against the first `<h1>`, and list exact
matches.

**Deliverable:** the 2 URLs, both strings, and a proposed distinct title for each. Titles are
service+location shaped (`Hardscaping in Charleston, SC | Patios, Walls & Concrete`) — keep that
pattern. **Do not invent service claims**; see the standing rules in `DECISIONS.md`.

## Task 2 — Find the 1 broken external link

One outbound link 404s. Extract every external `href` from the sandbox HTML, de-duplicate, and check
each with a HEAD request. **Deliverable:** the dead URL, the page(s) carrying it, and a
recommendation (replace / remove / point elsewhere). Be polite — one request per host at a time.

## Task 3 — List the 22 pages with non-descriptive anchor text

Semrush flags 22. Find internal links whose anchor text is generic — "click here", "read more",
"learn more", "this page", bare URLs. **Deliverable:** page, anchor text, destination, and a
proposed replacement describing the destination. This one is *mostly* generator-owned, so expect the
fix to land in `site-build/`, not here.

## Task 4 — Draft the lighting-post consolidation (DRAFT ONLY — Zach has not approved it)

`/blog/top-10-landscape-lighting-ideas-to-transform-your-outdoor-space/` is the **first genuine
post-rebuild indexing refusal**: Google re-crawled it on **2026-09-26** and still declined to index
it. No `noindex`, self-referencing canonical, 200 response — **not technical, a content verdict.**

The website editor's read (#68): consolidate into `/landscape-lighting/`, which already covers items
1, 3 and 4 of the blog's eleven under the heading "Paths, Steps and Trees Come First", and already
carries the costs.

**Deliverable: a written proposal, not an edit.** Which of the eleven items are already on the
service page, which are genuinely additive, what the merged section would say, and what the blog URL
should 301 to. **Zach decides whether to consolidate.** Do not delete or redirect anything.

## Task 5 — Strip developer comments from the CSS bundles (only if you can reach `site-build/`)

~4.4 KB of developer commentary ships inside the inlined CSS on **every page request** — the blocks
are appended *after* minification. Harmless but pure waste. **Ride along with the next bundle change;
do not spend a deploy on it.**

---

## Standing rules — these are not optional

- **Never invent a fact.** Content uses only what Zach or Doug supplied, or already-published copy.
- **(843) 614-9773 is the public number. 843-709-6140 is Zach's own and must never be published** —
  it is the published line for his other company and already causes a NAP conflict.
- **No maintenance or mowing claims.** Residential only. **No hydroseeding.**
- **Prices only as published on the site.** No founding year — none is published anywhere.
- **Doug is "more than thirty years in the trade."** No Lowcountry-specific figure.
- **Free consultation is geography-qualified** — free around Charleston, Mount Pleasant and
  Summerville; a charged, non-refundable proposal trip beyond, credited toward the build.
- **Log anything Zach tells you in `DECISIONS.md`**, quoted and dated, before acting on it.
- **WordPress snippets that WRITE need Zach's explicit go every time** (policy set 2026-09-25).
  Read-only diagnostics do not.

## Context worth having

- Site Health is **95%** against a 92% top-decile benchmark, with **zero errors**. Nothing here is
  urgent; this is tidying, not rescue.
- **Ignore "low text-to-HTML ratio" (73 pages) and "unminified JS/CSS" (74).** Both are artefacts of
  the shell inlining ~58k chars of CSS into every page. Not ranking factors.
- The site ranks for ~1,000 queries but sits at positions 11-50, where **5,934 impressions produced
  zero clicks**. The constraint is authority — reviews and links — **not page content.** Do not
  over-invest here.
- **Already fixed 2026-09-26, do not redo:** 75 footer links reading "Pavilions & Pergolas" pointed
  at the *pavilions* page; split into "Pergolas" → `/pergolas/` and "Pavilions" →
  `/pergolas-pavilions/`. Misleading anchors 75 → 0; links to the real pergola page 128 → 203.
- **Queued, deliberately not done:** migrating the pavilions content off the `/pergolas-pavilions/`
  URL to `/pavilions/` (which currently 404s) with a 301. Correct on the merits, but it is a redirect
  on an indexed page touching `deploy_shell.py`, which has no undo. **Local session, after 30 Sept.**

---

# Round 2 — queued 2026-09-27

Round 1 findings received and reviewed: `findings/2026-09-27-cloud-tasks.md` on branch
`claude/cramers-landscaping-tasks-wctmu4`. **Good work** — diagnosis only, verified on all 74 live
pages, honest about what could not be checked, and Task 2's answer ("no link is dead, change
nothing") was the right call rather than the expected one.

**One thing to fix on your side: PR #1 is titled "Complete service page rewrite from Zach's answers
+ pricing confirmation".** The branch contains two markdown files and 232 insertions with no page
touched. The title describes work that was not done, and on this project a title claiming a
**pricing** change is alarming — prices may only ever be those published on the site. **Retitle it
to something like "Diagnosis for queued cloud tasks — findings only, no page changed."** Titles are
read by people who will not open the diff.

**Your two incidental findings are accepted and queued for the local session** (both need generator
patches, which you cannot reach): the pergola-vs-pavilion meta description carrying wording Zach
explicitly rejected, and the leftover keyword-stuffed paragraph on `/retaining-walls/`. Finding the
first one was the single most valuable thing in the round — it is what Google prints under the title.

---

## Task 6 — Sweep the whole site against the standing facts — HIGHEST VALUE

You found two live defects **by accident** while doing something else. Do it deliberately across all
74 pages. For each item below, grep the sandbox HTML **and** confirm against the live page.

Check for:
1. **Wordings Zach has explicitly rejected.** `PROJECT-NOTES.md` and `DECISIONS.md` record these.
   The pergola "filters light / keeps the rain off" line is one you already found. There will be
   others — *"we do not plant sago palms"*, the West Ashley ceiling motive, "the paving stopping at
   the posts", any "open vs covered" framing.
2. **Vendor-era keyword stuffing** — the `<service> <city> <state>` pattern dropped into a sentence,
   like the `/retaining-walls/` one. Also unsupported superlatives: "premier", "top choice",
   "leading", "Charleston's trusted name".
3. **Unqualified free-consultation claims.** Standard wording: *"Consultation at your home"*, then
   free around Charleston, Mount Pleasant and Summerville; a charge beyond, **non-refundable**, and
   credited toward the build. Any bare "free estimate" or "free consultation" without the geography
   qualifier is a defect.
4. **Maintenance, mowing or lawn-care claims**, and **hydroseeding** — none of these are offered.
5. **Prices not published elsewhere on the site**, and **any founding year** (none is published).
6. **Doug's tenure** stated as anything other than "more than thirty years in the trade" — no
   Lowcountry-specific figure.
7. **`843-709-6140` anywhere.** It must never appear. The public number is (843) 614-9773.

**Deliverable:** one table — page, exact string, which rule it breaks, proposed replacement using
already-published wording. **Do not edit pages.** Flag anything ambiguous rather than guessing; the
rule is never invent a fact.

## Task 7 — Content verdict on the other three pages Google will not index

You did this for the lighting post. Do the same for the three still outstanding, **`/services/`
first** — it is a hub page, and a hub Google declines is the more serious signal:

- `/services/` — last crawled 2026-09-17 (pre-rebuild), still not indexed
- `/blog/pool-pavilion-charleston-sc/` — last crawled 2026-09-03
- `/blog/outdoor-living-space-ideas-charleston/` — last crawled 2026-09-16

**Note the difference from the lighting post:** that one was re-crawled **after** the rebuild and
still declined, so it is a verdict on current content. **These three were last crawled before the
20 September rebuild**, so Google has not yet seen what is there now. **Do not treat their status as
a verdict.** The question to answer is: *if Google re-crawls this page tomorrow, is there a
substantive reason it would decline it?* For `/services/`, the obvious risk is that a hub which only
links onward with little unique content reads as thin.

**Deliverable:** for each, what unique substance the page carries, what it duplicates, and either
"no change needed, wait for re-crawl" or a specific proposal. Same draft-only rule.

## Task 8 — The 64 unaudited `assets/work/` images

64 published images under `assets/work/` appear in **no** `photos.json` record, so the record-based
checks cannot see them. Determine: which live pages reference each, whether any is orphaned
(published but linked from nowhere), and whether any filename, `alt` or caption places a photo in a
town it should not — Kiawah, Sullivan's Island, Folly Beach and Johns Island have **no real job
photos**, and generic shots must say "Charleston area". See `project_photo_town_labels` context in
`DECISIONS.md`: a similar-looking diagnostic once sent a session chasing 24 phantom fixes, so
**confirm against what the page actually renders**, not against filenames alone.

---

## Still not available to you — do not attempt

- **`site-build/`** — all generators, `deploy_shell.py`, `perf_bundle.py`. Local only.
- **Semrush API** — 0 units, and they cannot be bought on this plan. Returns 18 October.
- **Search Console / GA4** — the service account key is not in this repo.
- **Deploying anything.** The repo is the sandbox, not the live site.
