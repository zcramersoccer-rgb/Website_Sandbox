# Tasks for the cloud session — queued 2026-09-26

Written by the **Cramers Landscaping company overview** session. You have this repo; it cannot
message you back, so this file is the handover. Read `DECISIONS.md` first — it is the record of
every instruction Zach has given, newest first.

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
