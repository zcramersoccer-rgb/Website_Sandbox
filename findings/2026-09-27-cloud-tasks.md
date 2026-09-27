# Findings for CLOUD-TASKS.md — 2026-09-27 (cloud session)

Diagnosis only. **Nothing on any page was changed.** `site-build/` is not reachable from the
cloud container, so every fix below has to land through the generators in the local session, per
the rule at the top of `CLOUD-TASKS.md`.

**Two limits on this session, both from the container's network policy:**

- `cramerslandscaping.com` is blocked, so the live site could not be read. Everything below is
  measured on the sandbox HTML in this repo (Site-revamp at `425074c`). **Grep the live page before
  applying any fix.** The sandbox and live can drift.
- Every external host is blocked too, including WebFetch. Task 2 could not be finished. It has a
  ranked shortlist and a one-line command to run locally.

---

## Task 1 — Pages where the title and H1 are identical — DONE

Semrush compares the full `<title>` against the H1. Exactly two pages match in full. Seven more
match once the ` | Cramers` suffix is removed, one of them the unpublished pay-invoice draft. Their
full strings differ, so Semrush does not count them.

| URL | Title = H1 | Proposed title |
|---|---|---|
| `/contact-us/` | Contact Cramers Landscaping in Charleston, SC | **Contact Us \| Call or Text Doug at (843) 614-9773 \| Cramers** (58 chars) |
| `/blog/pergola-pavilion-installation-charleston-sc/` | Pergola vs. Pavilion: Which One Is Right for Your Backyard? | **Pergola vs. Pavilion: Cost and Permits in Charleston, SC** (56 chars) |

Every claim in the proposals is already published. "Call or text Doug at (843) 614-9773" is on
the service pages. The pergola post has "Pergola and Pavilion Costs in Charleston" and "Permitting
in Charleston" sections. The second title keeps the KD-1 phrase "pergola vs pavilion" at the front.
Keep both H1s as they are.

## Task 2 — The one broken external link — NOT FINISHED (network blocked)

The sandbox has **34 unique external links**. None could be requested from here: the proxy logged
`connect_rejected` for every host, and WebFetch returned `EGRESS_BLOCKED`.

Skip the three social profiles in the footer. The Ahrefs note in `DECISIONS.md` already records
LinkedIn (999) and Facebook (400) as bot-blocking, not broken. Clemson returns 403 to crawlers for
the same reason.

**Suspects, most likely first**, from web-search evidence only:

1. `https://plantscience.psu.edu/research/centers/ssrc/documents/temperature.pdf/@@download/file/temperature.pdf`
   on 2 pages. Search engines index this document at the **shorter** URL
   `.../ssrc/documents/temperature.pdf`, without the `/@@download/file/...` suffix. If this link is
   the 404, point both links at the short URL.
2. `https://buildingscience.com/documents/bareports/ba-1015-bulk-water-control-methods-for-foundations/view`
   on 1 page. Still indexed. The PDF also lives at
   `https://buildingscience.com/sites/default/files/migrate/pdf/BA-1015_Bulk_Water_Control.pdf`, and
   PNNL mirrors it at `https://basc.pnnl.gov/library/bulk-water-control-methods-foundations-ba-1015`.
3. `https://llr.sc.gov/bcc/BCAdoption.aspx` on 1 page. It has no `www.`, unlike the other LLR
   links on the site.

Run this from any machine with open internet. It prints only the failures:

```
python3 - <<'PY'
import re,glob,html,urllib.request
urls={html.unescape(u) for f in glob.glob('*.html') for u in re.findall(r'href="(https?://[^"]+)"',open(f,encoding='utf-8').read()) if 'cramerslandscaping.com' not in u}
for u in sorted(urls):
    try: c=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).status
    except urllib.error.HTTPError as e: c=e.code
    except Exception as e: c=type(e).__name__
    if c!=200: print(c,u)
PY
```

## Task 3 — Non-descriptive anchor text — DONE

**Best match for Semrush's 22: the 22 "read more" links on `/blog/`.** Each post card has a
`<a class="cl-more" ... aria-label="Read more: <post title>">read more</a>`. The `aria-label` is
good for screen readers, but Semrush and Google read the visible text, which is just "read more".
The count matches exactly: 22 posts, 22 links, one per post.

No other reading fits the count. The only other generic anchors are footnote numerals (`1`, `2` to
`#src-n`) and "Source" on external citations. Together those appear on **14** blog posts, not 22.

**Proposed fix, in the generator that writes the blog index.** Pick one:

- **(a) Recommended: remove the `cl-more` link.** Each card already links the image and the
  `<h2>` title to the same URL, so the third link adds nothing. It also cuts 22 duplicate links from
  the page.
- **(b) Keep it and make the text descriptive.** Use the existing `aria-label` minus "Read more: ",
  for example "Read: Does an Outdoor Living Space Add Value to Your Home?", and drop the
  `aria-label`, since it would now repeat the text.

All 22 destinations are in the table below. The replacement text is the post's own H2 on the card.

| Destination | Replacement text |
|---|---|
| does-an-outdoor-living-space-add-value-to-your-home | Does an Outdoor Living Space Add Value to Your Home? |
| outdoor-living-space-cost-charleston | What Outdoor Living Costs in Charleston |
| how-to-design-an-outdoor-living-space-charleston | How to Design an Outdoor Living Space in Charleston |
| outdoor-living-space-ideas-charleston | Outdoor Living Ideas, and What Each One Cost |
| outdoor-living-spaces-mount-pleasant-sc | Outdoor Living in Mount Pleasant, SC |
| drainage-solutions-grading-charleston-sc | Fixing a Wet Yard in Charleston |
| tree-shrub-care-pruning-trimming-charleston-sc | Keeping a Landscape the Shape It Was Designed to Be |
| pergola-pavilion-installation-charleston-sc | Pergola vs. Pavilion: Which One Is Right for Your Backyard? |
| backyard-design-ideas-charleston-sc | Backyard Design Ideas for Charleston, by What You Want It to Do |
| outdoor-living-design-installation-charleston-sc | Design and Build Under One Roof |
| pool-pavilion-charleston-sc | Building a Pavilion at a Pool: What Changes |
| charleston-sod-installation-the-ultimate-guide-to-a-perfect-lawn | Laying Sod in Charleston, and Making It Last |
| does-artificial-grass-save-money-charleston | Does Artificial Grass Save Money in Charleston? |
| artificial-turf-vs-natural-grass-the-charleston-homeowners-ultimate-guide | Artificial Turf or Real Grass? We Install Both |
| transform-your-charleston-property-with-professional-landscape-lighting-the-ultimate-guide | How a Landscape Lighting System Should Be Designed |
| hardscaping-in-charleston-the-ultimate-design-material-guide | Choosing Hardscape Materials in Charleston |
| designing-your-dream-outdoor-kitchen-in-charleston-a-complete-planning-guide | Planning an Outdoor Kitchen: The Decisions, In Order |
| pool-deck-resurfacing-in-charleston-a-complete-guide-to-materials-methods-and-maintenance | Cool Deck, Microcement, Tile, or Replace It? |
| creating-the-perfect-outdoor-kitchen-for-charleston-homes | Building an Outdoor Kitchen That Works in Charleston |
| top-10-landscape-lighting-ideas-to-transform-your-outdoor-space | Eleven Landscape Lighting Ideas We Actually Install |
| low-maintenance-yard-charleston-sc | A Low Maintenance Yard Is a Design Decision |
| why-cramers-landscaping-is-charlestons-top-landscaping-company | How We Work: Design, Build and What Happens After |

**Lower priority, only if Semrush still flags anchors after the fix above:** the citation links
read "Source". They could carry the publisher name instead, such as "Tree Care Industry
Association: ANSI A300 Part 1". The footnote numerals are in-page `#src-n` jumps and are normal
citation practice. Leave them.

## Task 4 — Lighting post consolidation — PROPOSAL ONLY, Zach decides

**Not approved. Nothing was deleted or redirected.**

The post `/blog/top-10-landscape-lighting-ideas-to-transform-your-outdoor-space/` has 11 ideas.
Compared against `/landscape-lighting/`:

| # | Blog idea | Already on the service page? |
|---|---|---|
| 1 | Uplight one good tree | **Yes**, almost word for word: "Paths, Steps and Trees Come First" has the Japanese maple with two fixtures and the live oak visible from street, porch and house |
| 2 | Hang pendants in a live oak | **No, additive.** The service page does not mention pendants or use that photo |
| 3 | Light the steps | **Yes**, in "What We Light, In What Order" |
| 4 | Path lights along the walk | **Partly.** Paths-first is there. The spacing point is not: "evenly spaced pools of light read as designed, random ones read as a runway" |
| 5 | Wash the front of the house | **Partly.** "Accent lighting on ... the house itself" is there. Grazing to show brick, stucco and siding texture is not |
| 6 | Down lighting from a canopy | **Yes**: "soft moonlight across the lawn" |
| 7 | Tape lighting above the beams | **Yes**, in the structures paragraph and a FAQ answer |
| 8 | Wall sconces at eye level | **Partly.** Sconces are named. The reason is not: "ceiling lights alone make an outdoor room feel like a parking garage" |
| 9 | Bistro lights over the patio | **Partly.** They are named. "Run them on their own circuit, not an extension cord" is not |
| 10 | Light a water feature from within | **No, additive.** Not on the lighting page or on `/fountain-water/` |
| 11 | Timer, ideally with an app | **Mostly.** Transformer, timer and app are there. "We recommend a timer over a photocell" is not |

Four ideas are fully covered (1, 3, 6, 7) and one mostly (11). Two are genuinely new (2 and 10).
Four add one useful sentence each (4, 5, 8, 9). Two of the post's four FAQ answers repeat the service
page's FAQ: what to light first, and the $200-a-light cost.

**Proposed merge.** Add one section to `/landscape-lighting/` after "Paths, Steps and Trees Come
First". Every sentence below is already-published copy from the post, lightly condensed. Nothing is
new.

> **Beyond Paths and Trees**
> **Pendants in a live oak.** Uplit from below and hung with pendant lights from its limbs, the
> tree itself becomes the light over the lawn. *(photo: `charleston-waterfront-live-oak-uplighting-hanging-light-globes`)*
> **Grazing the house.** Light run up a facade shows the texture of brick, stucco or siding and
> gives the house presence from the street without lighting the windows.
> **Path spacing.** Spacing matters more than fixture choice. Evenly spaced pools of light read as
> designed; random ones read as a runway.
> **Covered spaces.** Sconces at eye level give an outdoor room human scale; ceiling lights alone
> make it feel like a parking garage. Bistro lights belong on their own circuit, not an extension cord.
> **Water features.** A fountain lit from inside reads at night as movement rather than a dark
> shape. It is a small addition while the feature is being built and an awkward retrofit afterwards.

Add to "Fixtures, Wiring and Control": *"We recommend a timer over a photocell."*

**Photos to bring across.** Seven of the post's 12 photos are not on the service page. The best
candidates are the waterfront live oak with pendants (item 2), the stepping-stone path with the lit
house corner (item 5), and the Spanish moss oak in West Ashley. Zach has asked not to lean on the
West Ashley cabana, and the service page already shows it, so leave out the cabana ceiling and
string-light shots.

**Redirect, if approved:** 301 `/blog/top-10-landscape-lighting-ideas-to-transform-your-outdoor-space/`
to `/landscape-lighting/`, as one hop. Then remove the post from `/blog/`, the sitemap, the
"Worth Reading Before You Start" block on `/landscape-lighting/`, and any "Related Reading" that
links to it. The anchor-text fix in Task 3 then covers 21 cards, not 22.

**Reason to hold off.** The binding constraint is authority, per `DECISIONS.md`. Consolidating
removes a page Google already declined rather than adding value. It is tidy, not urgent.

## Task 5 — Developer comments in the CSS bundles — NOT DONE

It needs `site-build/perf_bundle.py`, which is not in this repository. It is already marked
"ride along with the next bundle change".

---

## Found along the way — worth fixing, not in the task list

### 1. The pergola-vs-pavilion post's description uses the wording Zach rejected — HIGH

`PROJECT-NOTES.md` says: the old copy "a pergola filters light and keeps the space open; a pavilion
has a solid roof and keeps the rain off" — **"That is wrong"**. It also says "Do not write that the
split is open vs covered."

The sandbox still carries it in two places:

- `/blog/pergola-pavilion-installation-charleston-sc/`: the `meta description`, `og:description` and
  `twitter:description` all read *"Pergola or pavilion? A pergola filters light; a pavilion keeps the
  rain off. Compare them, see what each costs in Charleston, and which needs a permit."*
- `/blog/`: the card excerpt for that post has the same sentence.

The meta description is what Google shows under the title, so this is the first line most
searchers read about the post. **Check the live page first.** If it is there, proposed replacement
(155 chars, uses Zach's final wording):

> Pergola or pavilion? The difference is scale, roof options and enclosure, not open vs covered.
> See what each costs in Charleston, and which needs a permit.

Grep the generators for "filters light" too. Per `DECISIONS.md`, generators are what put fixed
wording back.

### 2. Leftover vendor keyword copy on `/retaining-walls/` — MEDIUM

The call-to-action section ends with:

> Call **(843) 614-9773** to schedule your free consultation and discover how our retaining walls
> Charleston SC can transform your outdoor space.

"retaining walls Charleston SC" is the old keyword-stuffed pattern the rewrite removed everywhere
else. This paragraph also has no geography or trip-charge qualifier. Check live first, since
`free_claim_audit.py` may already have handled it there. If it is still live, delete the paragraph.
The paragraph above it already says Doug and Zach will walk the site and quote.
