# Renderings & design work: handoff

From the "Cramers pavilion renders" cloud session (session_016AReCdWE7Xr6Bg2QTK7yqU) to "Renderings and design work"
(session_01HRSLvwnrdC3uth8dSeh33g). The client contact for all of this is Zach (Luxurious Renovations / Cramers Landscaping).

> This folder is design/render working material on a side branch of the website repo. **Do not merge `renders-handoff/` into
> the website's main branch.**

## Contents

```
renders-handoff/
  HANDOFF.md                       this file
  sunup-pavilion/                  ACTIVE PROJECT - 116 Sun Up Way pavilion
    build_pavilion.py              builds the whole scene from scratch (the source of truth)
    sunup-pavilion.blend           current build (entablature D, lighter fascia, stain A, 72" black fan)
    fetch_textures.sh              downloads the stand-in sky HDRI (not in git)
    textures/                      ambientCG CC0 maps the materials use
    scripts/                       render + review helpers (see "Render pipeline")
    drawings/                      2D concept drawings (matplotlib) + their scripts
    renders/review/                latest full review set (16 views) + 3 contact sheets
    renders/options/               option boards the client chose from (trim, fascia, stain, corner)
    refs/                          historic / Brent Hull reference images + credits (see refs/REFERENCES.md)
  other-projects/
    vanhove-hood/                  finished: Van Hove range hood (3 finishes) - script + final renders
    cramers-pavilion/              finished: Cramers Landscaping pavilion - setup script v3 + final renders
```

## 1. Active project: 116 Sun Up Way pavilion (Summerville, SC)

The client's own backyard project. It is a hip-roof pavilion with a TV/back wall on the long side and an outdoor kitchen at
one end. It goes in the back corner of the fenced yard where the oak trees are, past the crape myrtles (those are being
removed). White marking-paint lines on the lawn show the footprint, plus the planned plant beds and a walkway from the
fence gate.

### Site facts so far
- **Slab edge to fence:** 3 ft. The other yard measurements are still to come from Zach.
- **Orientation:** the back wall's outside faces north-east, so the TV faces south-west. The house shades it in the
  afternoon, so a full-sun TV is not needed.
- **House:** light aqua Hardie lap and board-and-batten (about sRGB #A0CED6), white trim, dark charcoal architectural
  shingles, white K-style gutters.
- **Yard:** a charcoal-stained wood fence with an open-picket top, young crape myrtles in pine straw, neighbours' white
  two-story houses and tall loblolly pines behind.
- **Photos:** in Google Drive folder "116 sun up way". All are 10-18 MB, which is over the Drive connector's 10 MB
  limit. Zach pasted 5 of them into the chat.

### Plan
| Item | Value |
|---|---|
| Roof | 16 x 20 ft hip, **4:12**, architectural shingles (charcoal), 2 ft overhang all round |
| Posts | 4 posts, **11-1/4" square**, **12 x 16 ft on centre**, 8'-0" slab to bottom of beam |
| Ridge | 4 ft long. Hips at 45 deg land exactly over the post corners |
| Slab | = drip edge (16 x 20). **Salt finish** field, **broom-finish** border band. Saw cuts on the outside faces of the posts, carried to the slab edge, plus centre cross joints. Slopes away from the back wall (to the front) |
| Back wall | Between the back posts, inset from both post faces. 2x6 wall. **Shiplap inside**, **Hardie lap outside**, both house aqua. Hardie 1x6 baseboard inside |
| TV wall | 70" TV + soundbar, flush mount, centred. Charleston-style copper lanterns each side (about 16" body). **One** floating shelf under each, stained to match the ceiling. No bench, no accent panel |
| Kitchen | At the +X (south-east) end. Counter front flush with the inside face of the posts. 30" deep, so its back lands at the drip edge (+3/8"). Run between posts 11'-0 3/4": 12" counter / 24" ice-drink basin / 24" cabinet / 18" counter / **36" Blaze grill** (20 lb LP bottle in the cabinet below) / 18-3/4" counter. **Lime plaster** island, **Hardie 1x6 baseboard**, **black granite, leathered**, stainless doors/drawers, LP vent panels low on both ends |
| Hood | **Required**: Blaze needs 6 ft from countertop to any overhead, and a vent hood under combustible overhead (LTE2 manual). **Lime plaster** hood, straight sides, **tapered front**, about 42" wide over the 36" grill. Rises behind the beam to the soffit; duct out through the overhang to a roof cap. No sink |
| Ceiling | **Beaded 1x6 pine T&G**, **stain A, light honey-neutral** (linear RGB 0.44, 0.27, 0.14 in the model), on the ceiling AND the soffit |
| Hips/ridge | Exposed and painted white. Hips 4-1/2" wide, 3" drop inside. Ridge 5-1/2" wide, 4" drop. **Hip trim continues out under the soffit** into the fascia corner, cut with **45 deg cheek cuts** so the end sits square in the corner. In the soffit the hip drop = 1" (matches the lighter fascia) |
| Fascia | **Lighter** Hardie fascia, 1" below the soffit, with a **1x4 cap on top**. The white **half-round gutter** hangs on the 1x4 |
| Water | Gutters all 4 sides. **Copper cup rain chains** (instead of downspouts) at both back corners and at the front corner past the kitchen. Each lands in a stone basin on a river-rock pad |
| Lighting | **72" fan, matte black**, with a light on the ridge. **LED tape** on top of the beam inside, hidden behind a 3/4" lip on the inside cap, washing the ceiling. 4 soffit cans (2 front, 2 on the open NW end) |
| Furniture | Outdoor teak sofa facing the TV, 2 teak club chairs on the open left side, teak coffee table + 2 side tables, jute-look outdoor rug. Spread toward the open left side; the cook aisle stays clear |

### Posts and beam (trim)
- **Posts:** plain shafts. The client dropped the paneled shafts to save money.
  - The 5/4 HardieTrim box uses (2) 1x12 + (2) 1x10.
  - Core: PT 8x8 or per engineer. A hidden Simpson standoff base sits inside the base trim.
  - Hardie is held **1/4" off the slab** (HardieTrim HZ10).
  - **Base:** one 5/4 x 5-1/2 band. Its **top edge is now rounded** (3/4" roundover) instead of the chamfer.
  - **Capital:** a 4/4 x 3-1/2 neck band, then an abacus of (2) 5/4 layers projecting 1-7/8" with a bevelled top.
  - The capital extends past the beam on every side. The post and beam are always the same width.
  - The client is open to rounding the underside of the abacus (an echinus-like roundover). Still undecided.
- **Beam:** (2) 1-3/4 x 11-7/8 LVL. **Rafters bear directly on the LVL** (client rule).
  - A PT fur-down brings the trimmed face to **18-3/4"**. That is about 1/5 of the column height, a Tuscan-like split.
  - Gravity check by me: 2-ply 11-7/8 works for the 16 ft span at about L/670.
  - The engineer must do the final sizing and the wind uplift.
  - Wrapped in 3/4" Hardie with a **1/4" drip reveal** at the bottom.
- **Entablature "D" (current, client's pick, see `renders/options/D_trim.jpg`):** option B's bottom and spacing with option A's
  top. Dimensions are from the beam bottom (B), outside face. Projections are measured from the post/beam face.
  - **Architrave, 2 steps:** a flush fascia from 0 to 2-3/4", then an upper fascia from 2-3/4 to 5-3/8" at +3/4".
  - **Frieze:** plain and flush, from 5-3/8 to 10-3/4".
  - **Cornice, A style:** a band from 10-3/4 to 14-1/4" at +1-3/4". Above it, a cap that bevels from +1-3/4 to +3" over 1-1/4", then runs vertical to 16-3/4".
  - The cap top tucks just under the sloped soffit.
  - **Inside face:** the same steps. The cornice is raised to the beam top, with a 3/4" lip that hides the LED.
  - Earlier options are kept in `build_pavilion.py` as `ENTS['A'|'B'|'C']`; select one with the env var `PAV_ENT`.
- **Client feedback history:**
  - First version: "the entablature just looks like 3 lines". The steps were then deepened.
  - Then: "entablature looks off". The diagnosis was a lone mid-height fillet plus a too-heavy deep fascia (two stacked white bands).
  - Resolved with D + the lighter fascia.

### Decisions log (client preferences, in order)
1. **Size:** 16x20 roof max (site). Ideas tried: posts 12x16 with 2 ft overhang; posts 14x20 (too big for the site); posts 13x16 with a 1 ft back overhang. **Final: 2 ft overhang all round, posts 12x16.**
2. **Pitch:** 4:12. Below 4:12, shingles need double underlayment (IRC R905).
3. **Classical inspiration:**
   - Mount Vernon front porch: its piers are actually **Tuscan, from Batty Langley plate 51, with paneled shafts**.
   - Doric proportions checked against Ware's *American Vignola*: 8 ft / 11-1/4" = 8.5 D.
   - Hardie flat stock plus a few router profiles. The client runs routers himself.
   - Then **simplified to save money**: stock widths and table-saw bevels.
4. Back wall shiplap inside / Hardie lap outside, close to the slab. HardiePlank HZ10 needs 1" minimum to the slab.
5. Hips 4.5" wide x 3" drop; the ridge slightly larger with more drop. The client normally uses Simpson anchors hidden by trim.
6. Grill: client uses **Blaze**. The hood can't be avoided (see above). Raising the beam to 9 ft fixes only the 6 ft clearance, and Hardie-wrapped wood is still combustible.
7. Stain: **A**. House colour taken from the photos.
8. Gutters: half-round, white. Then **rain chains instead of downspouts** (gutters kept, since the chains need outlets).
9. Fan 52" -> 60" -> **72" black**. Lanterns shrunk about 20%. One shelf per sconce. Outdoor furniture spread left.
10. Fascia: a 1x4 added on top. Deep fascia tried, then **lighter fascia** chosen.

### Open / next
- **Yard model and final renders:**
  - Zach will send yard measurements and the plant-bed / walkway layout.
  - Then build the site: fence, the house corner/porch, beds, walkway, remove the crape myrtles where the pavilion goes, oaks.
  - Re-light it to the real orientation (the open front faces SW).
  - Run finals at 1920x1080 or larger.
- **Books (Kindle) not reachable from the cloud:**
  - McAlester, *A Field Guide to American Houses*
  - Hull, *Millwork*
  - Hull, *Traditional American Rooms*
  - An earlier desktop-app session ("175 Civitas St range hood and fireplace") read them in Kindle Cloud Reader, but only for interior mantels and the hood.
  - Wanted for this project: Hull's classical-system chapter and any exterior porch, entablature or capital/base plates; McAlester's porch-support and cornice pages.
- **Still undecided:** capital underside rounded or square; whether to bring the inside entablature down to just wrap + cap to save money.
- **Engineer:** LVL sizing, uplift ties, post core, hip/ridge framing (the open vaulted hip has outward thrust at the beams).

## 2. Render pipeline

- **Blender:** 4.2.3 LTS, headless. In the old container it lived at `/opt/blender-dl/blender-4.2.3-linux-x64/blender`.
  Install:
  `curl -L -o b.tar.xz https://download.blender.org/release/Blender4.2/blender-4.2.3-linux-x64.tar.xz && tar xf b.tar.xz`
  Python deps for drawings and contact sheets: `pip install matplotlib pillow`.
- **Build:**
  1. `cd renders-handoff/sunup-pavilion && sh fetch_textures.sh`. This gets noon_grass_4k.hdr. The 8k original was 98 MB, too big for git.
  2. `blender -b --factory-startup -P build_pavilion.py` writes `sunup-pavilion.blend` next to the script.
  - Env vars:
    - `PAV_ENT` = A|B|C|D (default D)
    - `PAV_SOFFIT_HIP_DROP` (default 1.0)
    - `PAV_STAIN` = "r,g,b" linear
    - `PAV_OUT` = output .blend path
  - **Units:** inches internally, converted to metres (`IN = 0.0254`).
  - **Coordinates:**
    - Origin at the slab centre, top of the slab z = 0.
    - Posts at x = +-96, y = +-72. **+Y = the back wall (north-east)**, -Y = the open front (south-west), +X = the kitchen end.
  - **Key helpers in the script:**
    - `loft_ring()`: mitred rectangular rings from a (d, z) profile. Used for the beam/entablature, post bands, fascia and gutter.
    - `hip_surface()`: ceiling and roof surfaces with per-face UVs, so the T&G and shingles run parallel to the eaves.
    - `hip_tail()`: the soffit hip with 45 deg cheek cuts.
    - `bar()`: oriented boxes for hips, ridge and fan blades.
- **One view:** `blender -b sunup-pavilion.blend -P scripts/render_view.py -- OUT.png "Pavilion" "<camera name>" W H SPP`.
- **Full review set (16 views):**
  `blender -b sunup-pavilion.blend -P scripts/render_review.py -- OUTDIR 1280 720 64 "<view names...>"`
  - Ortho views are built on the fly: `E1 front elevation (SW)`, `E2 kitchen end elevation (SE)`, `E3 back elevation (NE)`,
    `E4 open end elevation (NW)`, `P1 roof plan`, `P2 floor plan cut at 4 ft`.
  - Perspective cameras:
    - `CAM_01 front 3-4`, `CAM_02 kitchen end`, `CAM_03 interior to TV`, `CAM_04 interior to kitchen`
    - `CAM_05 ceiling + hips`, `CAM_06 hood + island close`, `CAM_07 corner detail - trim + soffit hip`
    - `CAM_08 soffit corner looking up`, `CAM_09 lounge from the kitchen`, `CAM_10 back 3-4 (NE)`
  - At 1280x720 / 64 spp on 4 CPU cores, the full set takes about 25 min.
- **Other helpers:**
  - `close_corner.py` / `detail_cams.py`: trim close-ups.
  - `cam_tmp.py`: ad-hoc camera, `-- OUT eye_x,y,z target_x,y,z lens`.
  - `raycast.py` / `debug_ids.py`: find which object is at a pixel.
  - `ent_sections.py`: 2D true-scale entablature profile drawings.
- **Look settings:**
  - Cycles, OIDN denoise, adaptive sampling, AgX Medium High Contrast.
  - The sky is the Poly Haven `noon_grass` HDRI rotated 200 deg on a flat procedural lawn. This is a **stand-in** until the yard is modelled.
  - The green bounce from the lawn tints white trim in shade, which is expected in the stand-in.
- **Gotchas found:**
  - The wide lenses make the 18-3/4" beam look like a sloped band. That is perspective, not a bug (confirmed by raycast).
  - Vertical segments in `bar()` need the fallback side vector (already fixed).
  - Drive files over 10 MB can't be downloaded with the Drive connector.
  - Cross-container renders: if the container restarts, use the strip-render approach from the Van Hove project (`render in border strips + stitch`) for long finals.

## 3. Reference sources used
- W. R. Ware, *The American Vignola* (archive.org), used for the Doric and Tuscan proportions:
  - **Doric** (in diameters D): column 8 D, base 1/2 D, capital 1/2 D (abacus 1/6 D, echinus 1/6 D, necking 1/6 D),
    entablature 2 D (architrave 1/2 D, frieze 3/4 D, cornice 3/4 D).
  - **Tuscan:** column 7 D, entablature 1-3/4 D (architrave 1/2 D, frieze 1/2 D, cornice 3/4 D).
  - **General rule:** entablature = 1/4 of the column height, sometimes 1/5.
- Brent Hull, "Designing Exterior Columns" (JLC): proportion columns to the building; an intervening beam bridges the
  column-roof mass difference. The beam face lines up with the column neck and the capital projects past it
  (OldHouseGuy porch column alignment). More Hull findings are in `sunup-pavilion/refs/REFERENCES.md`.
- HABS VA-505 (Mount Vernon). Lossing 1851 (paneled square pilasters). The State Dept Diplomatic Rooms note on Langley plate 51.
- **Hardie and code:**
  - HardieTrim HZ10 install (2025): 1/4" off hardscape.
  - HardiePlank HZ10: 1" off the slab.
  - Prime all field-cut edges.
  - Routing is not addressed by Hardie (silica-dust task).
  - IRC R905.1.1 / R905.2.2 (shingle slope and underlayment).
- **Blaze LTE2 manual:** 6 ft countertop-to-overhead minimum. A vent hood is required under combustible overhead, and recommended under non-combustible.
- The client's photos (chat) and the Drive folder "116 sun up way".

## 4. Other projects (finished, for reference)
- **Van Hove range hood** (Laura Van Hove, 175 Civitas St, Mount Pleasant)
  - Three finishes rendered straight-on at 1920x1080 / 256 spp:
    - A: marmorino satin, cloudy
    - B: lime plaster + limewash
    - C: marmorino + new satin brass band with 3/4" polished rivet heads
  - Plus a finish close-up sheet. `other-projects/vanhove-hood/build_scene.py` rebuilds it; its textures were ambientCG Concrete034/Plaster006/Metal042A.
  - The full package (with .blend) was delivered to the client as 5 zips.
- **Cramers Landscaping pavilion:** `blender_setup.py` v3 plus the final renders (CAM_01-07). Delivered earlier.
