# Tasks for the cloud session — queued 2026-09-26

Written by the **Cramers Landscaping company overview** session. You have this repo; it cannot
message you back, so this file is the handover. Read `DECISIONS.md` first — it is the record of
every instruction Zach has given, newest first.

---

## Cloud session reply to Rounds 2 and 3 — 2026-09-27 02:40Z (read this first)

**Paused before starting, because the budget premise in Round 3 is wrong.** This cloud session does
**not** have a separate budget. Anthropic's docs: *"cloud sessions share rate limits with all other
Claude and Claude Code usage within your account"* (code.claude.com/docs/en/claude-code-on-the-web,
Limitations). This session's own rate-limit record shows the **same weekly window as the local
sessions, resetting 30 Sept 14:00Z, at warning status**. That agrees with `DECISIONS.md` #81 and
contradicts #87. Tasks 6-11 would spend the same 91% / 94% pool, against Zach's 95% ceiling and the
"at 90%+, deadline work only" rule, and none of them has a deadline.

**Done anyway, because it was small:** PR #1 retitled to *"Cloud session findings for queued site
tasks (docs only, no page changed)"*, with a description that says not to merge it into `main`.

**Update 02:45Z:** Zach chose "All tasks now" (DECISIONS #88), so Tasks 6-11 are running, and PR #1
is closed. He also reported the **homepage video glitching**: diagnosed in
`findings/2026-09-27-hero-video-glitch.md`. The poster is the t = 1.5 s frame but playback starts at
frame 0, so the picture jumps on every page load. A frame-0 poster is ready to upload; `hero_video.py`
needs the same change.

The pause above no longer applies. With PR #1 closed, its scheduled check-ins were cancelled too.

---

## Rounds 2 and 3 — results, 2026-09-27 03:30Z (cloud session)

All six tasks are done, plus Zach's homepage-video report. **Findings only; no page, generator or
setting was changed.** Everything was checked against a live snapshot taken at 02:43Z, after the
02:34Z batch deploy and the lighting merge.

| Task | File in `findings/` | Headline |
|---|---|---|
| Video | `2026-09-27-hero-video-glitch.md` | Poster is the t = 1.5 s frame, playback starts at frame 0, so the picture jumps on every load. Frame-0 poster ready in `findings/hero-video/`. |
| 6 Facts sweep | `2026-09-27-task6-facts-sweep.md` | Founding year "2016" is live on `/about/`; Zach's crisp-edge correction never reached 4 pages; Sullivan's Island "waterfront backyard" may be the Charleston live-oak job (needs Zach); bare free-consultation claims on 3 blog posts and 7 service pages; fire bowls $2,000 and custom fire pit $2,500 have no recorded source. 843-709-6140 appears nowhere. |
| 7 Unindexed pages | `2026-09-27-task7-unindexed-pages.md` | Wait for re-crawl on all three. `/services/` may stay out, which is fine for a navigation page. |
| 8 Images | `2026-09-27-task8-images.md` | No wrong-town labels. 118 of 339 base images unused (42.6 MB); 149 duplicate groups. One "pool and lawn" alt on an artificial-turf photo on `/sullivans-island-sc/`. |
| 9 Internal links | `2026-09-27-task9-internal-links.md` | Mulch and grading pages are missing from both sitewide menus. Retired lighting post is still in `post-sitemap.xml` and still published. |
| 10 Structured data | `2026-09-27-task10-structured-data.md` | `WebSite.name` is the bare domain on all 74 pages; LocalBusiness address has no postalCode 29485. Two FAQ-schema mismatches. |
| 11 Blog plan | `2026-09-27-task11-blog-plan.md` | Draft for Zach. Top 3: pergola permits (needs his town answers), fire pit vs fireplace, irrigation running cost. |

### Handback, in order (local session; Zach's go for any WordPress write)

0. **Deploy the restructured `/services/`** — Zach's go is given (`DECISIONS.md` #99). Port the
   `<!--process-->` block from the sandbox `services.html` into the generator that owns the page,
   then deploy and re-crawl. Steps and a source for every sentence: `findings/2026-09-27-services-restructure.md`.
1. **Hero video poster** — upload the frame-0 poster, change `hero_video.py` to cut the poster at
   frame 0, update `og:image`/JSON-LD references, purge Cloudflare. Seen on every homepage visit.
2. **Questions for Zach:** is "opened the business in 2016" right (then the "no founding year" rule
   changes) or should it come off `/about/` and `/summerville-sc/`? Is the Sullivan's Island
   "waterfront backyard" a Sullivan's job? Where do fire bowls $2,000 and custom fire pit $2,500 come
   from?
3. **Crisp-edge sentence** on `/patios-pavers/`, `/hardscape-installation/` and two posts: align to
   the `754a653` correction. Grep the generators.
4. **Bare free-consultation claims**: the 3 blog posts first (their FAQ schema repeats them).
5. **Menus**: add `/mulching-bed-maintenance/` and `/landscape-grading-services-charleston-sc/` to
   the header and footer service lists.
6. **Retired lighting post**: unpublish it so it leaves `post-sitemap.xml`; set its Redirection rule
   to ignore query parameters.
7. **Schema**: `WebSite.name` to "Cramers Landscaping"; add postalCode 29485; regenerate the cost
   post's FAQ schema.
8. Lower priority: the turf CTA superlative, the "pool and lawn" alt, and the unused and duplicate
   images.

---

## Status — 2026-09-27 (cloud session)

Results are in `findings/2026-09-27-cloud-tasks.md`. No page was edited. Every finding was verified
on the 74 live pages once network access opened.

| Task | Status |
|---|---|
| 1. Duplicate title/H1 | **Done, confirmed live.** `/contact-us/` and the pergola-vs-pavilion post, with proposed titles |
| 2. Broken external link | **Done.** No link is dead for visitors. The flagged one is almost certainly a Charleston Water rate page (404 to Semrush's crawler only) or Instagram (rate-limits crawlers). Change nothing |
| 3. Non-descriptive anchors | **Done, confirmed live.** The 22 "read more" links on `/blog/` |
| 4. Lighting consolidation | **Proposal written.** Awaiting Zach |
| 5. CSS comments | **Not done.** Needs `site-build/` |

Also found, both confirmed live: the pergola-vs-pavilion post's meta description still says "a
pergola filters light; a pavilion keeps the rain off", the wording `PROJECT-NOTES.md` calls wrong; and
`/retaining-walls/` still ends with old vendor copy ("retaining walls Charleston SC"). Details in the
findings.

### Handback — what the local session still has to do

The cloud session cannot reach `site-build/` and cannot publish, so everything below is yours. Each
page change goes through the generator, then a grep of both the generators and the rendered HTML,
per the rule below. Writes to WordPress need Zach's explicit go.

1. **Fix the pergola-vs-pavilion description** — HIGH, live now. The meta, og and twitter
   descriptions of `/blog/pergola-pavilion-installation-charleston-sc/` and its `/blog/` card
   excerpt say "a pergola filters light; a pavilion keeps the rain off". Replacement text is in the
   findings, finding 1. Grep the generators for "filters light".
2. **Delete the vendor paragraph on `/retaining-walls/`** — MEDIUM, live now. The one ending "...our
   retaining walls Charleston SC can transform your outdoor space." Findings, finding 2.
3. **Replace the 22 "read more" links on `/blog/`** — Task 3. Recommended: drop the `cl-more` link from
   each card, since the image and title already link to the post.
4. **Retitle `/contact-us/` and the pergola-vs-pavilion post** — Task 1. Proposed titles are in the
   findings.
5. **Put the lighting consolidation to Zach** — Task 4. Proposal only; nothing moves without his go.
6. **Strip the developer comments from the CSS bundles** — Task 5, with the next `perf_bundle.py`
   run.
7. **Align the gazebo wording** on `/outdoor-structures/` ("peaked" to "domed"), then re-run
   `build_knowledge.py` — LOW. Findings, finding 3.
8. **Optional:** confirm Task 2's exact URL in the Semrush Site Audit UI (campaign 31306158). No
   change is expected; every candidate works for people. The Semrush connector had no API units left.

**Getting these files onto Site-revamp.** They are on
`claude/cramers-landscaping-tasks-wctmu4`, open as PR #1 against `main`. That branch is Site-revamp
plus docs-only commits, so it fast-forwards cleanly:

```
git fetch origin && git checkout Site-revamp && git merge --ff-only origin/claude/cramers-landscaping-tasks-wctmu4 && git push origin Site-revamp
```

Publishing `main` afterwards the usual way (`--ff-only` from Site-revamp) marks PR #1 merged. Do not
use GitHub's merge button with squash or rebase: both rewrite the commits, and the next
fast-forward publish would fail.

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

---

# Round 3 — queued 2026-09-27

Round 1 merged into Site-revamp at `632d937`, docs only. **Good work** — and Task 2's "no link is
dead, change nothing" was the right answer rather than the expected one.

**Context you need: the local session is stopped until Monday.** Weekly Claude usage is at **91%
all-models / 94% Fable** against Zach's **95% ceiling**, resetting **30 Sept 14:00Z**. The eight
generator-side items you handed back are queued but **nothing local will happen before then**. You
have separate budget, so **you are the only one working on this until Monday.** Queue findings in
`findings/`; do not expect a local fix to land in between.

**Still outstanding from Round 2 — start here.** Tasks **6, 7 and 8** were appended to this file
after your branch was cut, so you may not have seen them. They are above. In priority order:
**Task 6** (sitewide sweep against the standing facts), **Task 7** (content verdicts on `/services/`
and the two unindexed blogs), **Task 8** (the 64 `assets/work/` images).

**Task 6 is the highest-value thing available to you.** You found two live defects *by accident* in
Round 1 — the rejected pergola wording in a meta description, and the keyword-stuffed
`/retaining-walls/` paragraph. Doing that deliberately across all 74 pages is likely to find more,
and those are the defects that actually reach customers.

**Still true, do not attempt:** `site-build/` (generators, `deploy_shell.py`, `perf_bundle.py`,
`build_knowledge.py`), the Semrush API (0 units until 18 October), Search Console and GA4 (service
account key is not in this repo), and deploying anything.

---

## Task 9 — Internal linking and orphan audit

Semrush scores Internal Linking **93%** but does not say what the 7% is. Round 1 showed why this
matters: 75 footer links reading "Pavilions & Pergolas" pointed at the *pavilions* page, which was
over a third of all pergola anchor text on the site pointing at the wrong URL. **That was invisible
until someone counted.**

Across all 74 pages, from the sandbox HTML and confirmed against the live pages, report:
1. **Orphans** — pages in the sitemap that no other page links to.
2. **Click depth** from the home page for every page. Flag anything deeper than 3.
3. **Inbound internal link counts per page**, ranked. Call out any **money page** (the service hubs,
   the 12 town pages, `/contact-us/`) that is unusually starved.
4. **Anchor-text profile for each money page** — the distinct anchor strings pointing at it and how
   many of each. **This is where the pergola defect showed up.** Flag any page whose most common
   inbound anchor does not describe it.
5. Internal links that **301 rather than resolving directly** — a hop wastes a little equity and
   they are cheap to correct at source.

**Deliverable:** the tables, plus a short list of the changes worth making, ranked. **No edits** —
these all live in generators.

## Task 10 — JSON-LD / structured data audit

Semrush reports Markup 100%, which is not the same as correct. Two known incidents: a **duplicate
`BreadcrumbList` on 73 pages** (caught and fixed), and an **old `HomeAndConstructionBusiness` block
with "Cramers landscaping" lower-cased** still sitting in a WordPress option (inert — stripped from
rendered pages — but it shows this drifts).

For all 74 pages: extract every JSON-LD block, and report **duplicate `@type`s on one page**;
**inconsistent NAP** across blocks (name, phone, address, URL) against the version of record —
**Cramers Landscaping · (843) 614-9773 · 9153 Markleys Grove Blvd, Summerville, SC 29485 ·
https://cramerslandscaping.com**; **any appearance of `843-709-6140`**, which must never be
published; broken or self-inconsistent `BreadcrumbList` trails; `FAQPage` entries whose questions or
answers do not match the visible page text; and any `priceRange`, `aggregateRating` or `review`
markup, **which must not be present unless it reflects something genuinely published**.

**Deliverable:** one table of defects, with the correct value for each. **No edits.**

## Task 11 — Blog plan by audience (DRAFT for Zach, do not write posts)

Zach, 2026-09-25: *"creating different content that serves different needs. So some blogs are going
to be more for homeowners and designs some are going to be more proffesional some statistics based
etc."* Logged as a standing direction, not started.

Using only the 22 existing posts and what is already published: **classify each existing post** by
audience (homeowner/design, trade/professional, data-led) and note which register dominates; then
**propose a shortlist of new post ideas per register**, each with a one-line rationale tied to a real
gap — a service with no supporting post, a town with real jobs and no story, a question the chat
logs or the FAQs show people asking.

**Hard constraint, and it is the reason this is draft-only: a statistics-led post is the highest
risk of invented figures on this whole site.** Every number must carry a named, checkable source, or
come from Zach. **Do not draft any post body.** A list of ideas with rationales is the deliverable;
Zach picks, then supplies the facts.

---

**Housekeeping:** PR #1 is still titled *"Complete service page rewrite from Zach's answers +
pricing confirmation"*, which the branch does not contain. **Please retitle it.**

**Do not touch `main`.** It is 154 commits behind Site-revamp and deliberately holds the pre-revamp
site; Pages serves Site-revamp. Fast-forwarding it would publish the whole revamp. **That is Zach's
decision and he has not made it.**
