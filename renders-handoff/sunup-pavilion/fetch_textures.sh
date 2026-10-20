#!/bin/sh
# Stand-in sky for the review renders (Poly Haven CC0). The 8k original (98 MB) was too big for git; 4k is fine.
cd "$(dirname "$0")/textures" && curl -fL -A "Mozilla/5.0" -o noon_grass_4k.hdr https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/4k/noon_grass_4k.hdr
