# Task 6: facts sweep of all 74 live pages (2026-09-27, cloud session)

**This is a diagnosis only. No page, CSS or generator was changed.**

**Source.** The live snapshot of all 74 sitemap URLs, fetched 2026-09-27. `/thank-you/` was fetched separately and is clean. Every page was parsed into:

- visible text, with header and footer handled separately
- `<title>`, meta, og and twitter descriptions
- every JSON-LD string, including the FAQ answers
- `alt`, `title`, `figcaption`, `aria-label` and placeholders

The same extraction was run on the sandbox HTML.

**Sandbox against live.** Every finding below is identical in the sandbox. Apart from WordPress form and metadata markup, the sandbox differs from live in one place: it is behind on the lighting consolidation, which is now live. `/landscape-lighting/` has a new "Beyond Paths and Trees" section, and `/blog/` no longer has the lighting card. The new text breaks no rule.

**How the probes were checked.** Each search pattern was first shown to find a known positive:

- The public number (843) 614-9773 was found on 74 of 74 pages.
- The town + "SC" pattern matches the deleted `/retaining-walls/` sentence.
- Zach's approved "not open vs covered" line was found.

**Regression check.** Every sentence that any commit removed from the sandbox HTML was checked against the live text. None of Zach's corrections has come back, apart from the item in row 3, which was never removed in the first place.

Severity runs from customer-facing false claims down to tidying. "Needs Zach" means no published wording or recorded answer settles the point.

## Findings

| # | Page (live) | Exact string (excerpt) | Rule broken | Where | Proposed replacement (published wording) |
|---|---|---|---|---|---|
| 1 | `/sullivans-island-sc/` | H3 "A waterfront backyard": "This waterfront property was a whole-yard project… A pavilion and a brick herringbone patio… The backyard lawn is artificial turf… Out front the lawn is zoysia." | **1: wrong-town job.** Same class as the Johns Island fix (823f086), probably the Charleston job; see note A | body, og:image | **Needs Zach to confirm.** If it is the Charleston job, use the Johns Island pattern: call it a Charleston job and link it, reusing "This Charleston job covered the whole property, from the front walk down to the water" from `/project-charleston-live-oak-landscape/` |
| 2 | `/about/` (twice), `/summerville-sc/` | "Doug Cramer opened the business **in 2016** after a lifetime in landscaping." / "**In 2016** he opened Cramers Landscaping…" / "Before starting Cramers Landscaping **in 2016**, he helped develop Nexton…" | **5: founding year.** The standing rule and the ABC/GBP pack (DECISIONS #72) say none is published, but it is. The About text is already in the repo's first commit (49a16ed). The Summerville line came in with fa8701c, "Rewrite… from Zach's answers", so 2016 may well be Zach's own figure and the rule may be what is wrong | body | **Needs Zach.** Either confirm 2016 and correct the rule and the ABC pack, or delete the year: "Doug Cramer opened the business after a lifetime in landscaping." / "He opened Cramers Landscaping and turned his focus to…" / "Before starting Cramers Landscaping, he helped develop Nexton…" |
| 2b | `/`, `/contact-us/` | `"founder": [Doug Cramer, Zach Cramer]` | Contradicts `/about/`: "Doug Cramer opened the business", "Doug owns the company". Added by 0851717 (site audit), not by Zach | JSON-LD | Founder: Doug Cramer only, per `/about/`. Also for Task 10 |
| 3 | `/patios-pavers/` (Summerville story), `/hardscape-installation/`, `/blog/hardscaping-in-charleston-the-ultimate-design-material-guide/`, `/blog/outdoor-living-space-ideas-charleston/` | "Mortar over a slab is what let us get a perfect install **with crisp edges**" / "…which is what let us get **crisp edges** and a perfectly flat install" | **1: wording Zach corrected.** 754a653 (Zach, 09-20): "Mortar over a concrete base does not give a paver a crisp edge – it lets a paver that already has one sit dead flat." That commit says the Summerville story was fixed; it was not, and three later pages copied the line. `/patios-pavers/` now contradicts its own FAQ | body | Use the `/patios-pavers/` FAQ wording: "…mortar set over a concrete slab. That does not give the paver a crisp edge – it means a paver that already has one can be laid dead flat, every piece level with the next." |
| 4 | `/blog/outdoor-living-design-installation-charleston-sc/`, `/blog/why-cramers-landscaping-is-charlestons-top-landscaping-company/`, `/blog/drainage-solutions-grading-charleston-sc/` | "The consultation at your home is free, you get drawings, and 3D renderings are available at additional cost." (FAQ, and the body of the How We Work post) / "…The consultation is free." (drainage FAQ) | **3(c): bare.** There is no caveat anywhere on these pages. "You get drawings" beside "3D at additional cost" also implies drawings are always included, which Zach's design-fee answer (ce9b9a4) removed from the landscaping FAQ | body, FAQ JSON-LD | The `/landscape-installation/` FAQ answer: "The consultation at your home is free around Charleston, Mount Pleasant and Summerville. For Kiawah, Seabrook, Wadmalaw and Awendaw, or anywhere else more than an hour from Charleston or Summerville, there is a charge for the proposal trip. It comes off the price if you go ahead with the build, and it is not refundable if you do not. A job that does not need a design, or where a quick drawing will do, is not charged for one. A larger project with a full drawn design carries a design fee… 3D renderings are available as an option at additional cost." For the drainage post, use the first three sentences |
| 5 | `/artificial-turf-installation/` (CTA) | "Cramers Landscaping, **your trusted choice for Charleston artificial turf installation**." + "…or anywhere in Charleston County, our team is ready to elevate your outdoor space." | **2: vendor keyword stuffing and superlative.** Same class as the `/retaining-walls/` paragraph deleted today | body | Delete both sentences. The section already has "Tell us where the turf would go…" and the full caveat |
| 6 | `/landscape-drainage-services-charleston-sc/`, `/outdoor-shower-installation-charleston-sc/`, `/landscape-lighting/`, `/charleston-sod-installation/`, `/landscape-installation/`, `/patios-pavers/`, `/retaining-walls/` | Step "**Free consultation at the property.**" (drainage) / "We look at the spot. **Free consultation at your home.**" (shower) / "Every quote follows a **free consultation** at your home" (lighting costs) / call-to-action headings "Request (a) **Free** Drainage / Sod Installation / Landscape / Patio / Retaining Wall Consultation", with no caveat in the section | **3(c): bare within the section.** Each page carries the caveat elsewhere. d510276 said bare "Free" in headings would be dropped; these survived | body, H2 | Steps: "Consultation at your home." plus "It's free around Charleston, Mount Pleasant and Summerville. For Kiawah, Seabrook, Wadmalaw and Awendaw…", as on `/patios-pavers/`. Lighting: delete "free". Headings: drop "Free", as in "Request a Pool Deck Consultation" |
| 7 | `/charleston-sod-installation/` (CTA) | "If your lawn needs a fresh start, Cramers Landscaping is here to help. We provide: Full sod installation · **Partial sod repairs** · Soil and grading improvements · **Irrigation adjustments** … Let Cramers Landscaping create a healthy, beautiful lawn…" | **2: vendor-era CTA copy. 4 (ambiguous):** "irrigation adjustments" is a service claim with no source from Zach | body | "Call or text Doug at (843) 614-9773, or fill in the form below." plus the caveat. The service list **needs Zach** |
| 8 | `/irrigation-system-installation/` | "We design, install **and service** systems…" / "Cramers Landscaping installs **and services** irrigation systems across the greater Charleston region…" | **4 (ambiguous).** "Service" reads as an ongoing service; a95feb9 removed "ongoing irrigation maintenance". `/summerville-sc/` does publish "irrigation repairs" | body | **Needs Zach.** Either "design and install" (delete "and service"), or "design, install and repair" per `/summerville-sc/` ("…drainage fixes and irrigation repairs") |
| 9 | `/concrete-pool-decks/`, `/north-charleston-sc/` | "Pavers, travertine and natural stone start from about **$18** a square foot" / meta: "travertine and pavers from $18" | **5: possible conflict.** $18 is Zach's patio starting point (pavers on sand). Stone mortar-set on a slab is published at "$30 or more" on 3 pages (Zach, per 0b10bf0) | meta, body, FAQ JSON-LD | **Needs Zach** |
| 10 | `/blog/outdoor-living-spaces-mount-pleasant-sc/` | H2 "**Commercial Work:** A Wellness Center Entrance" / "**Commercial Work:** A Deck Under a Live Oak" | Standing rule "Residential only"; 10467f2 stripped commercial claims. The jobs themselves came from Zach (2eecc00) | body | **Needs Zach.** The smallest change is to drop the "Commercial Work:" prefix |
| 11 | `/fire-pits/` | "Custom fire bowls on pedestals **$2,000 and up**" | **5:** price on one page only; no source in PROJECT-NOTES or DECISIONS | body, FAQ JSON-LD | **Needs Zach:** confirm and record it, or remove it |
| 12 | 10 pages (`/fire-pits/` meta, `/hardscape-installation/`, 3 town pages, 4 posts, `/fireplaces/`) | custom fire pit "**from $2,500**" | **5:** consistent across the site but unsourced. PROJECT-NOTES has only the "$1,000 kit"; 754a653 recorded custom as "up to $3,000+" | meta, body | **Needs Zach:** confirm, then record it in PROJECT-NOTES |
| 13 | 6 pages; `/mulching-bed-maintenance/` meta | "**$105 a yard**" / meta: "Mulch **and pine straw** beds… at $105 a yard installed" | **5:** the unit is still unconfirmed (PROJECT-NOTES:793 "Zach wrote 'square yard'… CONFIRM"), and the meta applies the price to pine straw too | meta, body | **Needs Zach** |
| 14 | `/mulching-bed-maintenance/` | Step in "How We Do Beds": "**Refresh on schedule:** mulch annually, pine straw two to three times a year." + "Book Your Mulch and Bed **Service** Today" | **4 (ambiguous):** reads as a recurring service. a95feb9: the mulch page "describes installation, not year-round bed care" | body | The page's own meta wording as advice: "Mulch once a year, pine straw two to three times." Delete the "Book…" line |
| 15 | `/mulching-bed-maintenance/`, `/irrigation-system-installation/`, `/patios-pavers/`, `/about/`, `/contact-us/` | "No matter where you're located in the Lowcountry, we bring prompt, reliable service and a commitment to quality." / "Ready for a Smarter Watering Solution?… Contact us today…" / "…highlight our expertise, craftsmanship, and attention to detail." / About "Our Mission" ("the best possible landscaping experience") and "Our Values" / "proudly serves… Charleston County and beyond" | **2: vendor-era filler** (mild) | body | Delete the mulch sentence and the patios carousel line. Irrigation CTA: "Call or text Doug at (843) 614-9773, or request a consultation." plus the caveat. About and contact boilerplate: Zach's call |
| 16 | `/about/`, `/contact-us/` | Service-area labels "Folly Beach Coastal **& Rental** Landscapes", "Kiawah Island **Estate** Landscaping", "Isle of Palms Salt-Air Landscaping"… | **2: vendor "town + service" labels.** "Rental" brings back the rental-property audience a95feb9 removed | body | Plain "<Town>, SC", as the same list already does for "Daniel Island, SC" and "James Island, SC" |
| 17 | `/blog/` | "Explore the Cramers Landscaping blog for **expert** tips…" | **2:** vendor template (mild) | meta, og, JSON-LD | Delete "expert" |
| 17b | `/blog/why-cramers-landscaping-is-charlestons-top-landscaping-company/` | The URL slug itself | **2:** superlative in the URL; the title and H1 were already rewritten | URL | Zach's call. Changing it needs a 301 |
| 18 | `/hardscape-installation/`, `/landscape-grading-services-charleston-sc/`, `/landscape-lighting/`, `/outdoor-shower-installation-charleston-sc/` | Call-to-action heading "Request (a) **Free** … Consultation" | **3(a):** the caveat is in the same section; only the heading is bare | H2 | Drop "Free" for consistency |
| 19 | 11 project pages; `/charleston-sc/`, `/james-island-sc/` and `/summerville-sc/` (FAQ, and the CTA on Summerville) | "Tell us about your Charleston-area / James Island-area / Mount Pleasant-area / Summerville-area / West Ashley-area yard… **free consultation** at your home." / "…and the consultation is free." | **3(b): qualified only by the town** (ambiguous, Zach's call). d510276 judged these accurate | body; the town FAQs are also in JSON-LD | No change, unless Zach wants the caveat everywhere |
| 20 | `/outdoor-structures/`, the How We Work post | "the seams between trades are where projects go wrong" | **1-adjacent:** a drafted line Zach replaced on the ideas post (02b3192, where it was the fountain reason). Here it is used in another context | body | Zach's call |

**Note A (row 1).**

- The story matches `/project-charleston-live-oak-landscape/` feature for feature: waterfront, herringbone brick patio, pavilion, turf out back, zoysia out front, lighting.
- On 2026-09-21 Zach said Sullivan's Island has no photos.
- 99ca32a records that job's photo as Charleston.
- 823f086 lists Sullivan's Island among the towns "with no job of their own".
- The photos in the section are captioned "Charleston area".

`town_page_facts.md` is in `site-build/` and could not be read from here, so this needs Zach.

## Rule 3: every free-consultation claim, judged by section

**(a) Qualified by the caveat.** 32 passages on 25 pages; 4 of the 32 are FAQ JSON-LD copies. These are the canonical sentence, "…free around Charleston, Mount Pleasant and Summerville. For Kiawah, Seabrook, Wadmalaw and Awendaw… not refundable…". The trip-charge wording says the same thing in all 34 places it appears: non-refundable, and it comes off the price. Three pages word it slightly differently.

**(a), but the heading is bare.** 4 headings; see row 18.

**(b) Qualified only by the town.** 15 passages on 14 pages, plus 3 FAQ JSON-LD copies; see row 19. Ambiguous, Zach's call.

**(c) Bare within the section, with the caveat elsewhere on the page.** 7 pages and 8 instances; see row 6.

**(c) Bare, with no caveat anywhere on the page.** 3 blog posts, 4 passages, all mirrored in FAQ JSON-LD; see row 4.

**Also clear:**

- No "free" in any title or meta description.
- No "free estimate", "free quote", "no obligation" or "complimentary".

## Rule 5: price inventory (live pages)

Every price below is consistent everywhere it appears. The exceptions are flagged in rows 9 and 11-13.

| Price | Pages | Status |
|---|---|---|
| Pergola $10,000–$30,000 | 17 | verified |
| Pavilion $30,000–$90,000+ | 19 | verified |
| Pavilion "$80,000 and up" (West Ashley level) | 5 | verified |
| Outdoor kitchen $8,000–$20,000+ | 16 | verified |
| Fireplace kit ~$8,000, custom $20,000+ | 5 | verified |
| Fire pit kit ~$1,000 | 8 | verified |
| Custom fire pit from $2,500 | 10 | **unsourced** (row 12) |
| Fire bowls on pedestals from $2,000 | **1** | **single page, unsourced** (row 11) |
| Patios from ~$18/sq ft | 20 | verified. Pool-deck use for travertine is row 9 |
| Stone on slab $30+/sq ft | 3 | from Zach per 0b10bf0; not in PROJECT-NOTES |
| Poured concrete ~$12/sq ft | 16 | verified |
| Retaining wall (CMU and stucco) from ~$50/sq ft | 4 | verified |
| Turf from $13/sq ft | 15 | verified |
| Sod $750 a pallet installed | 9 | verified |
| Irrigation $1,000/zone plus $1,500 backflow and timer | 6 | verified |
| Irrigation "typical system about $6,500" | **1** | arithmetic of published figures (5 × $1,000 + $1,500); acceptable |
| Lighting ~$200 a light plus transformer | 14 | verified |
| Mulch $105 a yard | 6 | unit unconfirmed (row 13) |
| Fountain kit $1,000, custom up to $30,000 | 5 | verified |
| Shower $6,000–$15,000 | 8 | verified. No stale $8,000 remains |
| Planting: beds $1,000–$2,000, front yard $5,000–$10,000, full $20,000+ | 8 | verified. PROJECT-NOTES' list of 7 pages is stale: Kiawah and Sullivan's no longer carry it; four posts do |
| Glulam beams $10,000 in materials | 4 | verified |
| Cost-post worked example ($7,200 / $1,200 / $525 / $20,925) | 1 | derived and labelled "an illustration… not a quote" |
| Cited third-party figures: Cost vs Value $18,263 and $25,096; North Charleston tree fee $217.50/inch; Charleston Water rates | 1–2 each | sourced, not Cramers prices |

**Founding year:** "2016" is on 2 pages; see row 2. No other founding claim appears anywhere: no "since 19xx/20xx", "founded", "established" or `foundingDate`. The only "since 1924" is the state flower, and every "established" is about lawns or yards.

## Fixes worth making, ranked

1. **Row 1: the Sullivan's Island story.** One question to Zach. If it is the Charleston job, it is the Johns Island defect again, with one customer's yard advertised in two towns.
2. **Row 2: the 2016 founding year**, plus the JSON-LD founder field. Either the page or the standing rule and ABC pack is wrong, and GBP and ABC have an opening-date field that should match.
3. **Row 3: the crisp-edges line.** This is Zach's own correction, 7 days unapplied. It contradicts the FAQ on the same page.
4. **Row 4: three blog FAQs with a bare "free"** and an implied free design. These are in FAQ JSON-LD, the text Google can quote.
5. **Row 5: the turf keyword and superlative sentence.** It is the same fix as `/retaining-walls/`.
6. **Row 6, then row 18:** drop "Free" from the call-to-action headings and step labels on 11 service pages. This is generator-owned (the service_page / CTA builders), so grep the generators for "Free" in `<h2>` and `<strong>`.
7. **Rows 7, 8 and 14:** the maintenance-flavoured wording (sod CTA list, irrigation "service", mulch "refresh on schedule"). Each is one question to Zach.
8. **Rows 9-13:** record the unsourced prices ($2,500, $2,000, $30+, the mulch unit) in PROJECT-NOTES once Zach confirms them, and settle the pool-deck travertine figure.
9. **Rows 15-17 and 20:** vendor-era tidying. Low priority, one pass.

## Checked and clean

- **Rule 7, 843-709-6140.** It appears in no form (dashed, dotted, bracketed or `tel:`) on any of the 74 live pages or `/thank-you/`. It is also absent from all 78 sandbox HTML files, `chat-widget.js`, `sitemap.xml` and every other repo file except the rule text in `CLOUD-TASKS.md` and `DECISIONS.md`. Git history shows it was last in page HTML in a concrete-page CTA ("Call 843-709-6140 today…"), removed in 6806c2b (09-22). The only other phone-like strings are the form placeholder `(843) 555-1234` and a Facebook ID.
- **Rule 1, Zach's known corrections, all clean live:**
  - The sago palm line.
  - The West Ashley ceiling: "beadboard" everywhere it is described, in body, alt, captions and FAQ JSON-LD. The cost-saving motive is back by Zach's #20 ("the beadboard ceiling was a cost decision"), so it is approved. The `-plywood-` filename is deliberate (e3ff1cd).
  - "The paving stopping at the posts" and the related drafted lines.
  - Open vs covered, "cannot have a roof", "defined by gable/hip/gambrel", and the gazebo "peaked" (now "domed").
  - Pre-emergent, fertilizer, fungicide and pesticide claims. The only first-person chemical line is Zach's approved "spray and kill the old grass and the weeds"; the rest is homeowner advice.
  - Johns Island prose now credits the James Island garden correctly.
  - "Sullivans Island" without the apostrophe: 0 in text, meta or JSON-LD. There are 141 correct forms; only URLs lack the apostrophe.
  - Retaining walls failing "mainly from drainage": gone.
  - The Kiawah oak threshold is 16 in.
  - GFCI 210.8 is described as rewritten.
  - Outdoor showers: no permit.
  - The trip charge is non-refundable and "comes off the price" in all 34 places.
  - 3D renderings are always "at additional cost".
  - The pergola meta and the `/retaining-walls/` vendor paragraph from Round 1 are both fixed live.
- **Rule 2:** no "<service> <town> SC", no "near me/you", and none of "premier", "top choice", "leading", "#1", "award" or "trusted name". The live homepage testimonials carry no Cramer family reviewers.
- **Rule 4:** no hydroseeding, mowing service, lawn-care service or maintenance plan. Every "maintenance" mention is advice or an explicit "we are not a maintenance company". `/charleston-sc/` "has us back to prune and to clean her fountains" is framed the same way; Zach's call if fountain cleaning is too much.
- **Rule 6:** the same line appears on 16 pages: "Doug has worked in landscaping his whole life, with more than 30 years of experience". There is no Lowcountry figure anywhere. "His whole life" is Zach's own wording from 09-22 (6806c2b). The homepage eyebrow "30+ Years of Experience" is not attributed to Doug, so it reads as company tenure next to "opened in 2016". That is worth a look if row 2 changes.
- **Warranty and credentials:** all say 1-year workmanship and plant warranty, licensed residential builder (Zach) and insured. The footer rating "5.0 from 18 reviews" matches 57141fa.

## Not verified, and sandbox-only notes

- **`site-build/`** could not be reached, so neither the generators nor `town_page_facts.md` were grepped. Rows 1, 3 and 6 need a generator grep before any fix, per the standing rule. Grep the claim, not just the string.
- **The live chat widget** (`chat.cramerslandscaping.com`) and `knowledge.md` were not in scope. The repo copy of `chat-widget.js` is clean.
- **Two photos for Task 8 to confirm.**
  - The North Charleston "swing set around the fire" story. PROJECT-NOTES (B16) still records that Zach did not recognise that job.
  - 23 alt texts on 13 pages read "… by Cramers Landscaping, Charleston area", which breaks the alt convention in PROJECT-NOTES.
- **Sandbox only, not live:** `_draft-pay-invoice.html` has a bare "Request a free consultation" twice and the old footer "Charleston's premier landscaping company…". Fix both before it is ever published.

---

**Verified by the parent cloud session, 2026-09-27 03:30Z, against the live snapshot and git history.**
- Founding year: live `/about/` reads *"Doug Cramer opened the business in 2016 after a lifetime in
  landscaping."* Confirmed. The live LocalBusiness JSON-LD also lists both Doug and Zach as `founder`.
- Crisp edge: Zach's correction is commit `754a653` (2026-09-20, "Corrections from Zach"): *"the
  mortar-set explanation was wrong. Mortar over a concrete base does not give a paver a crisp edge."*
  It reached the `/patios-pavers/` FAQ only. The pre-correction sentence is still live on
  `/patios-pavers/` itself, `/hardscape-installation/`, and the hardscaping-materials and
  outdoor-living-ideas posts. Its source is `PROJECT-NOTES.md` (Summerville marble patio), which
  still carried the uncorrected wording; a correction note was added there in this commit.
- Sullivan's Island: the live page's "A waterfront backyard" paragraph is as quoted. Its source is in
  `site-build/`, which the cloud cannot read, so it stays "needs Zach".
