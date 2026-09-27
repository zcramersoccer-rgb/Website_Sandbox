# Homepage hero video "glitching" — diagnosis, 2026-09-27 (cloud session)

Zach reported the homepage video glitching. **Nothing on the site was changed.** The fix needs a
WordPress media upload and a generator edit, which only the local session can do, with Zach's go.

## The cause: the poster is not the video's first frame

The video shows the poster while it loads, then plays from its first frame. They are different
moments of a moving camera shot, so on every page load the picture **jumps sideways the instant
playback starts, then glides back** to where the poster was.

| Compared (grayscale, 320x180, mean absolute difference on 0-255) | Value |
|---|---|
| Live poster `hero-poster-3.webp` vs video frame 0 (what plays first) | **65.23** |
| Live poster vs video frame 45, t = 1.50 s | **0.66** (best match of all 1,104 frames) |
| Typical change between consecutive frames | 2.81 |

So the poster is the **t = 1.5 s** frame. That dates from the old cut, which faded in from black, so
1.5 s was its first clear frame. The v9 cut replaced the fade with a crossfade loop, making frame 0 a
full picture, but the poster was never moved to frame 0. See `poster-vs-first-frames.jpg`: the
cabana sits in a clearly different place at 0.00 s than on the poster, and returns to it by 1.50 s.

## What was checked and is fine

- **Live files = repo files.** `hero-1080-2.mp4`, `hero-720-2.mp4` and `hero-poster-3.webp` on
  WordPress are byte-identical to `assets/video/` (MD5 `0290bd0e…`, `62a83fea…`, `bb451422…`).
- **Encode:** H.264 High, constant 30 fps, 1,104 frames, 36.8 s, no irregular frame timing, 0 decode
  errors, bt709 SDR tagging (the old HLG problem is not back), keyframe every 2 s, start time 0.
- **Motion:** no single-frame pops, no freezes, no brightness flashes, and no uneven pattern from
  the interpolated in-between frames. A full-resolution crop at the fastest camera move shows sharp
  posts and fence slats with no warping.
- **Loop seam:** last frame to first frame changes by 6.38, in line with the crossfade's own
  frame-to-frame change (about 8 in the first 2 s). Seamless, as #17 intended.
- **Delivery:** Cloudflare HIT, `Accept-Ranges: bytes`, and Range requests return 206 with a correct
  `Content-Range`, which iPhone Safari needs.
- **Script:** picks the 720 or 1080 file once at load (by `max-width: 900px`), sets muted and
  autoplay, plays on `canplay`, resumes on tab return. No source swapping on resize.

## The fix (local session, Zach's go needed for the WordPress write)

1. **Replace the poster with frame 0.** Ready-made: `findings/hero-video/hero-poster-frame0.webp`,
   1920x1080, 175 KB (the current one is 170 KB), cut from the live 1080 file. It matches frame 0 at
   0.4 on the table's scale. Upload it and point the homepage at it. If the file is instead replaced
   in place at the same URL, **purge Cloudflare for that URL**: it is cached with a one-year
   `max-age` and currently a HIT.
2. **Fix the generator so it cannot come back.** `hero_video.py` still cuts the poster at t = 1.5 s.
   Change that to frame 0, or the next video run restores the jump. Per `DECISIONS.md`, "a page is
   not a fix": grep the generators for the poster timestamp.
3. **Also update** anything else that references `hero-poster-3.webp`: the homepage JSON-LD
   `image` / `primaryImageOfPage` and `og:image` use it too.

**Alternative, no new image:** in the homepage's inline video script, set `vid.currentTime = 1.5`
before the first `play()`. Playback then starts on the poster's frame. The poster swap is simpler
and also fixes the social-share image, so it is the recommendation.
