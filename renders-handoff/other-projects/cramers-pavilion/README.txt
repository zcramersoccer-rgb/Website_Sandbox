CRAMERS LANDSCAPING PAVILION - BLENDER PACKAGE  (matches drawing set REV 14)  - scene setup v3

FILES
  cramers_pavilion.blend      Ready-to-render scene built by blender_setup.py v3 (Blender 4.2 LTS). Open and press F12.
  cramers_pavilion.glb        Main model. Real-world size in meters, Z-up in Blender, materials named.
  blender_setup.py            v3 scene setup (materials, grass, sky + sun, interior lights, 6 cameras, Cycles).
  blender_setup_v2_original.py  The previous setup script, kept for reference.
  textures/noon_grass_8k.hdr  Poly Haven CC0 sky (open field with a tree line). The .blend points here (relative path).
  textures/typhoon_bordeaux_tile.jpg  Countertop texture made from the owner's photo of the actual slab.
  renders/sauna_bath_plan_before_after.png  Top-down cutaway of the sauna + bath layout changes.
  renders/final/              Final renders, 2400 x 1350, 256 samples, denoised.
  renders/v1_original/        What the v2 script produced (1200 x 675, 64 samples) - for before/after comparison.
  cramers_pavilion_obj/       Same model as OBJ/MTL (pre-rotated for Blender's default OBJ import, meters).
  preview_*.png               Depth-correct test renders of this exact model (geometry check, flat colors).

QUICK START
  Open cramers_pavilion.blend. The timeline holds one shot per frame:
     frame 1 CAM_01_Cover   2 CAM_02_Bar_Stool_View   3 CAM_03_Front_Right
     frame 4 CAM_04_Sauna_Doorway   5 CAM_05_Sauna_Back_Bench   6 CAM_06_Back_Right
  Go to a frame and press F12, or Render > Render Animation for all six. Each frame has its own sun direction,
  backdrop turn and exposure (keyed), so switch shots by changing frame rather than "Set Active Camera".
  Cycles, 256 samples, adaptive, OpenImageDenoise, 2400 x 1350, AgX Medium High Contrast. Uses the GPU if it finds one.

REBUILD FROM SCRATCH
  Blender > Scripting > Open > blender_setup.py > Run Script   (or: blender -b -P blender_setup.py)
  Settings at the top of the script:
    SUN_AZIMUTH / SUN_ELEVATION   main sun direction (default front-left, 45 deg high)
    CAM_SUN / CAM_BG_TURN / CAM_EXPOSURE   per-shot overrides
    USE_GRASS      3D lawn on/off (off renders faster)
    CEDAR_PHOTO    path to a photo of your cedar boards  -> used for the board color (grain still follows each board)
    GRANITE_PHOTO  path to a photo of your countertop slab -> replaces the procedural Typhoon Bordeaux
    RENDER_ALL     True = render all six shots into /renders when the script finishes
  The script downloads the HDRI from Poly Haven if textures/ doesn't have it; without internet it falls back to
  Blender's procedural sky.

MODEL LAYOUT
  Front of the pavilion faces -Y (Blender Front view, Numpad 1, looks at the open front).
  Bar on the left (-X side), bath/sauna block on the right (+X). Origin = back-left post grid corner.
  Objects are grouped: Pavilion, Roof, Enclosure, Enclosure_Siding, Sauna_Interior, Bath_Fixtures,
  Doors, Fan, Outdoor_Shower, Site - each split by material (e.g. Pavilion__charred_cedar).
  Wood meshes carry two attributes the shaders use: 'grain' (board-local coordinates, x along the grain) and
  'board' (per-board random / position across the board). The script writes them; they have no UVs.

WHAT v3 FIXED (details in the CHANGES block at the end of blender_setup.py)
  - Cedar grain ran as the same wavy stripes across every wall; bench tops and beam undersides had none; boards
    were invisible. Now every board has its own grain direction, tone, rings and seams.
  - Shou sugi ban looked like a pebble wall; granite looked like pink marble; concrete was a stained old floor;
    the lawn was patchy dead grass ending in mid-air.
  - Two suns (HDRI sun + an extra sun lamp at a different angle) -> one.
  - Fan light lit the blades white and cast blade shadows over the ceiling; sauna light blew out the ceiling and
    showed as a glowing ball through the door glass; the sauna bucket stand-in rendered as a stick in a box.

OWNER REVIEW CHANGES
  - Cedar matched to the West Ashley pool cabana (honey/amber sealed WRC, small knots, light rough-sawn texture).
  - Post bases: board-wrapped upper block on a wider plinth that stands on corner feet (incl. the wall-engaged posts).
  - Bar baseboard black; countertop from the photo of the Typhoon Bordeaux slab.
  - Sauna: lower bench pulled back 46 cm for a ~68 cm walkway past the heater; three recessed ceiling lights.
  - Bathroom: water heater and cedar shelves swapped.
  - Sloped beam over the TV wall: grain follows the slope. Ceiling = beaded T&G, TV wall = flat T&G,
    bath/sauna exterior = lap siding with real 1/2 in butt shadow lines.

SIMPLIFIED ON PURPOSE (concept model, not shop drawings)
  - Siding, wall boards and T&G ceiling are individual flat boards (no tongue/bead profile - seams are shaded).
  - Furniture, stools, decor and landscaping beds are not included.
  - Fan, fixtures and plumbing are simple stand-ins; heater stones are low-poly.
  - Hidden framing (rafters, studs, footings) is not modeled - see S0-S2 for structure.
