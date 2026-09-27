# /services/ restructured around the process — ready to port and deploy (2026-09-27)

> **Revision 2, same day.** Zach: *"service page still doesnt have enough unique content"* (`DECISIONS.md` #100).
> Three new sections were added: **What Happens Before What**, **Comparing Quotes**, and a six-question
> **FAQ** with matching FAQPage JSON-LD. Main content 544 → **1,667 words**; phrasing found on no other
> page 483 → **1,582** eight-word sequences (**95%** of the page). The sentences the first version had copied whole
> from other pages (the trip-charge paragraph, design fee, warranty, start times, stages) were **reworded, same
> facts**, which is Zach's "repeated block content" point.
>
> **Where each block goes (the local session found the owners):** the reworded `<!--process-->` block into
> `site-build/process_section.py`, which already emits it for `/services/` only; the new `<!--sequence-->`,
> `<!--quotes-->` and `<!--faq-->` blocks into whichever generator emits the rest of the `/services/` body
> (`grep -rln "Custom Outdoor Spaces, Designed and Built by One Family" site-build/`), **never into a generator
> that fans out to other pages**; and the FAQPage JSON-LD into the `/services/` head.

**Zach's go to build AND deploy:** `DECISIONS.md` #99 (*"Restructure /services/ around the process
can you do this and then have the other session push it live"*). Built in the sandbox `services.html`
by the cloud session; **the local session ports it into the generator and deploys.** Nothing is live.

## What changed

- **The process is now the page's spine.** "How a Project Works" moved from near the bottom to
  directly after the introduction, and grew from a short list into six numbered steps: consultation
  at your home, a rough budget, design, HOA review and permits, build, and after the build. Each step
  says what happens, how long it takes, and links to the services and real projects that belong there.
- **It stays the service directory.** The three groups (Landscaping, Hardscaping, Outdoor Structures)
  and every service link below them are byte-for-byte unchanged, so no service page loses a link.
- **It does not compete with the "How We Work" post.** Each step is two to five sentences; the intro
  links the post ("The full story is in How We Work...") for the long version.
- **One styling tweak:** the intro section's background class went from `cl-sec mint` to `cl-sec`,
  so tinted and plain sections still alternate with the process section moved up. No new CSS: every
  class used (`cl-sec`, `cl-wrap`, `cl-center`, `cl-steps`, `mint`, `g`) already exists in the bundle.
- Title, H1, meta description, canonical, robots, breadcrumbs, hero, header, footer and form: unchanged.

| | Before | After |
|---|---|---|
| Main content words | 550 | 789 |
| Section order | intro, directory, projects, process, CTA | intro, **process**, directory, projects, CTA |
| New in-content links | — | 13, to: sod, irrigation, plants, outdoor kitchens, pergolas, pavilions, outdoor structures, outdoor showers, contact, the cost post, the How We Work post, Game Day Backyard, Fireside Retreat |

## Where the block is

In the sandbox `services.html`, the new section is delimited by `<!--process-->` and `<!--/process-->`
(lines 48-59). The old process block (formerly lines 100-111) is removed. The only other change is
the class on line 38. `git diff 56eafd7 -- services.html` shows all of it.

## Every sentence and its source

| Step | Sentence | Source |
|---|---|---|
| Intro | Every project runs the same way, wherever you live, and the people who design it are the people who build it. | old `/services/` process intro |
| Intro | The full story is in How We Work: Design, Build and What Happens After. | link to that post, by its title |
| 1 | Doug or Zach comes out in person, usually within a week of your call, to walk the property with you and ask how you want to use the space. | old `/services/` ("comes out in person"; "On-site consultation, usually within a week of your call. We ask how you want to use the space") |
| 1 | The consultation is free around Charleston, Mount Pleasant and Summerville. For Kiawah, Seabrook, Wadmalaw and Awendaw, or anywhere else more than an hour from Charleston or Summerville, there's a charge for the proposal trip. It comes off the price if you go ahead with the build, and it is not refundable if you do not. | verbatim sitewide consultation wording (`/plants/`, `/about/`, service-page CTAs) |
| 2 | Most people want a rough budget first, because they do not know what these things cost. | `PROJECT-NOTES.md`, Zach's cross-cutting answers: "a rough budget, because they do not know what things cost" |
| 2 | It usually comes within a week of the consultation. There's no point designing something you can't afford. | old `/services/` |
| 2 | What Outdoor Living Costs in Charleston has real Charleston prices from our own projects, with what moves each number. | that post's own meta description |
| 3 | Drawings matched to your home's architecture, for the planting and for any structure, with optional 3D renderings for an additional cost. | old `/services/` design step; "planting plans" (`/services/` directory, `/about/`) |
| 3 | This takes 1 to 4 weeks depending on size. A larger project with a full drawn design carries a design fee, and what it comes to depends on the job. Small, simple jobs skip this step, pay nothing for design, and get a quote and plan right after the consultation. | old `/services/` (design-fee sentence also verbatim on `/summerville-sc/`) |
| 4 | Local reviews, like an HOA or a town board, fit in before the permit, and we can prepare and submit those applications for you. | old `/services/` |
| 4 | Structures like pergolas and pavilions need a permit, which takes about 4 to 6 weeks; an outdoor shower does not. | old `/services/`; no permit for showers: `/outdoor-shower-installation-charleston-sc/` and `DECISIONS.md` (09-22) |
| 4 | Our Game Day Backyard in Nexton went through HOA review before we built it. | `/project-summerville-putting-green-pergola-kitchen/`: "The home is in Nexton ... so the design went through HOA review before we built it." |
| 5 | You'll get an exact quote once the design is set. | old `/services/` ("Final quote once the design is set.") |
| 5 | Structures usually begin within 1 to 2 months of signing, and simple sod jobs we try to fit in within a few weeks at most. | `/pergolas-pavilions/` and `/outdoor-structures/` (first half, verbatim); `/charleston-sod-installation/` (second half); `PROJECT-NOTES.md` A5 |
| 5 | A pergola, or a simple kitchen and pergola, takes 1 to 3 weeks to build, and a pavilion 6 to 8 weeks. | old `/services/`; `PROJECT-NOTES.md` confirmed timelines |
| 5 | Our own team handles the gas, electrical and plumbing. | `/services/` directory: "Gas, electrical, plumbing and permits are handled by our own team" |
| 6 | We carry a 1-year workmanship and plant warranty. The plant warranty does not apply without an automatic watering system or to losses from weather. | How We Work post (both clauses verbatim) |
| 6 | Most yards happen in stages, which is sensible: our Fireside Retreat in Summerville was built that way, with the gas and water lines for later stages pre-run. | `/landscape-installation/` ("Most yards happen in stages, which is sensible."); `/project-summerville-stone-fireplace-pool-deck/` ("came together in stages"; "we ran the gas and water lines for everything that would come later") |

Nothing was left out for lack of a source. No title, H1 or meta change is proposed.

## Port and deploy (local session)

1. **Find the owner.** Which generator emits `/services/` could not be determined from the repo. Run
   `grep -rln "How a Project Works" site-build/`; that string is in the current live body.
2. **Port the block into that generator** (or into `deploy_shell.py` if the markup is static there),
   replacing the old process block and moving it after the intro. Do not paste into WordPress by hand:
   a generator run would revert it.
3. **Grep afterwards**, generators and rendered HTML, for the old step text ("Final quote once the
   design is set", "Permits and build.") to confirm nothing re-emits the old block.
4. **Deploy**, then check the live `/services/` main text matches the sandbox `services.html`.
5. **Queue `/services/` for a re-crawl request** in the daily-tasks session. It is one of the pages
   Google has not indexed since the rebuild (Task 7).

## Verification (cloud session)

- Well-formed: zero unclosed or mismatched tags; exactly one H1; header, hero, breadcrumbs, service
  directory, footer and form unchanged (the diff touches only line 38 and the process block).
- All 13 new links resolve to live pages (the two blog links map to `/blog/<slug>/`). The retired
  lighting post is not linked.
- No "near me", no year, no 843-709-6140, no "premier" or "trusted"; the one "free" is the
  geography-qualified consultation sentence.
- Rendered at 1440px and 390px: no horizontal overflow, no broken images, step cards lay out in two
  columns on desktop and one on mobile. Full-page shots: `findings/services-restructure/`.


## Revision 2 — the new sections and their sources

Placed after the service directory (sequence, quotes) and after the projects (FAQ), so the tinted and
plain bands still alternate. Same classes as the rest of the site (`cl-steps`, `cl-faq`); no new CSS.
The sentences are new wording; the **facts** are all published or verified, as below.

| Section | Claim | Source |
|---|---|---|
| Before What, intro | The order of trades matters because some things get expensive to change once built over. | `/landscape-installation/`: "The order matters, though, because a few things get very expensive once there is a patio sitting on top of them." |
| Before What, intro | Every project is built with our own crews; nothing gets blamed on another trade. | Homepage LocalBusiness description ("design and build every project with their own crews"); `/landscape-installation/` ("so nothing gets blamed on another trade") |
| The ground | Grading and drainage come before planting; poor grading leaves a lawn lumpy; regrade if it slopes to the house; drainage can save mature planting. | `/landscape-installation/` ("Grading, drainage and irrigation go in before planting"); `PROJECT-NOTES.md` sod answers ("poor grading gives a lumpy yard"); `/landscape-drainage-services-charleston-sc/` |
| What runs underneath | Conduit, gas and water go in before hardscape; cheap on the day, costly under a finished patio. | `/landscape-installation/`, "Plan for What You Cannot Dig Up Later" (linked for the full list) |
| Wiring during the build | Run lighting while a structure or patio goes in; structures are lit as part of building them. | `/landscape-lighting/` (both points, published) |
| Room for the next stage | Lines for a later kitchen, fireplace or sink run while framing is open; Fireside Retreat built that way. | `/project-summerville-stone-fireplace-pool-deck/`; `PROJECT-NOTES.md` details list ("Planning ahead for a later kitchen project") |
| Water, then plants | Irrigation before planting; sod on ground sprayed off, dug out and regraded. | `/landscape-installation/`; `/charleston-sod-installation/` |
| Quotes, intro | A lower quote usually prices something different. | How We Work post, "When Another Quote Comes In Cheaper". The clause "most of the difference is in work you cannot see" is framing that summarises the list below it, not a new fact. |
| Quotes | Concrete: 2x4 forms are 3.5 in; slab should be at least 4 in. | `/concrete-services/` |
| Quotes | Retaining walls: rebar; unfilled block is weaker and caps bond poorly. | `/retaining-walls/`; `PROJECT-NOTES.md` RW4 |
| Quotes | Patios and pool decks: compaction; settling and roots; uncompacted pool backfill. | `/patios-pavers/`; `/concrete-pool-decks/` |
| Quotes | Pergolas: roof, ceiling, trim and electrical separate $10,000 from $30,000. | `/pergolas/`; `PROJECT-NOTES.md` price drivers (confirmed) |
| Quotes | Irrigation: zones from water pressure and volume; most systems they fix were poorly designed. | `/irrigation-system-installation/`; `PROJECT-NOTES.md` Part E |
| Quotes | Lighting: every system needs a transformer and timer. | `/landscape-lighting/` |
| Quotes | Sod: $750 a pallet installed; prep not included. | `/charleston-sod-installation/` |
| FAQ 1 | Timeline by stage. | This page's process steps; `/pergolas-pavilions/` (start within 1 to 2 months, "depending on how busy we are and whether permitting or HOA approval is still running") |
| FAQ 2 | Small jobs skip design; plant beds $1,000 to $2,000; sod within a few weeks. | This page's design step; planting prices confirmed by Zach 2026-09-24 (`PROJECT-NOTES.md`, published on `/landscape-installation/`); `/charleston-sod-installation/`; Zach still wants smaller jobs (`DECISIONS.md`, Google Ads 09-24) |
| FAQ 3 | Most yards are staged; rather stage over a couple of years than rush; first stage planned with the last in mind. | `/landscape-installation/`; How We Work post; `/project-summerville-stone-fireplace-pool-deck/` |
| FAQ 4 | Applications prepared; HOA before permit; almost all structures need one (4-6 weeks), some towns like Isle of Palms exempt small ones; showers need none; walls need one at 6 ft from the lowest point. | This page; `PROJECT-NOTES.md` (Zach: permits, Isle of Palms example, RW3); showers: `DECISIONS.md` 09-22 |
| FAQ 5 | No mowing or lawn maintenance; no hydroseeding. | Standing rules in `CLOUD-TASKS.md`; Zach 2026-09-24, *"we dont hydroseed"*. **Zach's call:** this publishes a "no". Drop the question if he prefers not to say it. |
| FAQ 6 | Pergola $10,000-$30,000; pavilion $30,000-$90,000+; patios about $18/sq ft. | `/pergolas/`, `/pergolas-pavilions/`, `/patios-pavers/` (all confirmed prices) |

**Verification, revision 2:** zero unclosed or mismatched tags; one H1; every link on the page exists
on the live site; none of "near me", a year, 843-709-6140, "premier", "trusted", "best" or an
unqualified "free" in the new sections; FAQ JSON-LD matches all six visible answers after normalising;
no horizontal overflow at 1440px or 390px. Full-page shots in `findings/services-restructure/` were
re-taken.

**Rewording pass (revision 2b):** nine sentences reworded so they no longer repeat other pages word for
word. Facts unchanged. The consultation sentence keeps every element of the rule: free around
Charleston, Mount Pleasant and Summerville; charged beyond, naming Kiawah, Seabrook, Wadmalaw, Awendaw and
anywhere over an hour out; credited toward the build; not refunded otherwise. FAQ JSON-LD rebuilt from the
visible answers; zero mismatches, markup balanced, one H1.
