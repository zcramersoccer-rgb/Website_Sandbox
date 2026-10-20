# python3 contact_sheets.py RENDERDIR [OUTDIR]
# Converts the review PNGs to JPG and builds the three contact sheets (elevations/plans, exterior, interior).
import sys, os
from PIL import Image, ImageDraw, ImageFont
src = sys.argv[1]; out = sys.argv[2] if len(sys.argv) > 2 else src
SHEETS = {
 'Sheet1_elevations_plans': ['E1 front elevation (SW)', 'E2 kitchen end elevation (SE)', 'E3 back elevation (NE)',
                             'E4 open end elevation (NW)', 'P1 roof plan', 'P2 floor plan cut at 4 ft'],
 'Sheet2_exterior': ['CAM_01 front 3-4', 'CAM_02 kitchen end', 'CAM_07 corner detail - trim + soffit hip',
                     'CAM_08 soffit corner looking up', 'CAM_10 back 3-4 (NE)'],
 'Sheet3_interior': ['CAM_03 interior to TV', 'CAM_04 interior to kitchen', 'CAM_05 ceiling + hips',
                     'CAM_06 hood + island close', 'CAM_09 lounge from the kitchen'],
}
try: font = ImageFont.truetype('DejaVuSans.ttf', 22)
except OSError: font = ImageFont.load_default()
TW, TH, CAP, PAD = 960, 540, 34, 16
for sheet, names in SHEETS.items():
    rows = (len(names) + 1) // 2
    im = Image.new('RGB', (PAD + 2*(TW + PAD), PAD + rows*(TH + CAP + PAD)), (244, 241, 234))
    d = ImageDraw.Draw(im)
    for i, n in enumerate(names):
        p = os.path.join(src, n + '.png')
        if not os.path.exists(p): continue
        r = Image.open(p).convert('RGB')
        r.save(os.path.join(out, n + '.jpg'), quality=90)
        x, y = PAD + (i % 2)*(TW + PAD), PAD + (i // 2)*(TH + CAP + PAD)
        d.text((x, y + 4), n, fill=(30, 30, 30), font=font)
        im.paste(r.resize((TW, TH), Image.LANCZOS), (x, y + CAP))
    im.save(os.path.join(out, sheet + '.jpg'), quality=88)
    print('SHEET', sheet)
