# Récitalpha daily pipeline (read this first in every scheduled run)

Channel: TikTok @recitalpha6 — faceless animated TRUE stories about money, power, scams, gangs & mafia. US audience.
Goal: reach Creator Rewards (10k followers, 100k views/30 days). Every video must be > 60 s (target 75–95 s).

## Daily output
- 2 new episodes per day. Post times (Africa/Tunis): 16:00 and 23:00.
- Never repeat a story: check `engine/stories_log.md`, append each new episode there.

## Truth rules (non-negotiable)
- Every fact (dates, numbers, names, outcomes) must be confirmed by at least 2 reliable sources found with WebSearch/WebFetch
  (museums, .gov, encyclopedias, major newspapers, history sites). If a fact can't be confirmed, cut it or soften it ("about", "reportedly").
- No legends presented as facts. Prefer people/events from before ~1990, or well-documented later cases.
- Gang/mafia stories: tell the money angle (heists, rackets, tax cases, laundering). No glorifying, no gore.
- Keep a sources list per episode in `engine/stories_log.md`.

## Hook rules (first 3 seconds decide everything)
- Sentence 1 = the most shocking TRUE fact or twist, with a number. e.g. "In 1931, the most feared gangster in America went to prison… for not paying taxes."
- On-screen giant number/text from frame 1. No intros, no "hey guys".
- End every video with a cliffhanger teaser of the NEXT episode + "Follow".

## Build steps (cloud workspace)
Work dir layout (paths are hard-coded, keep them):
- /home/claude/rec/fonts  (BebasNeue-Regular.ttf, Anton-Regular.ttf, PlayfairDisplay[wght].ttf, Oswald[wght].ttf from
  https://raw.githubusercontent.com/google/fonts/main/ofl/<family>/<file>)
- /home/claude/rec/models (kokoro-v1.0.onnx + voices-v1.0.bin from
  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/)
- /home/claude/epNN/ for each episode, with symlinks fonts -> /home/claude/rec/fonts and models -> /home/claude/rec/models,
  plus img/ for archive photos.
1. Setup: `pip install --break-system-packages skia-python kokoro-onnx soundfile numpy pillow`. Download fonts + models.
   Copy project docs into each episode dir: `engine/engine.py` -> engine.py, `engine/gen_audio.py`, `engine/mix_ep.py`.
   Copy `engine/props.py` too (shared photo cards, tags, bills, safes, calendars, pop text, follow pill). Use `engine/render_ep03_capone.py`, `engine/render_ep04_brinks.py` (and ep02) as THE reference for a new episode (photo cards,
   props, scene timing with wt()). Write script.py and render_epNN.py for the new story in the same pattern
   (os.environ["REC_ROOT"] = the episode dir; set E.DRAW, E.RED_SCENES, IMPACTS, CLINKS).
2. Research + script (12 scenes, 1–3 sentences each, ~200–240 words). Numbers spelled out in narration, digits in CAPTION_OVERRIDES.
3. `REC_ROOT=/home/claude/epNN python3 gen_audio.py af_heart 1.05` -> voice.wav + timeline.json (TOTAL must be > 62 s).
4. Archive photos: the cloud workspace cannot reach Wikimedia, so use the PUBLIC-DOMAIN photo stock already in the repo:
   `archive/stock/<topic>/` (each folder has credits.txt: file | Commons title | license | date | author) and `archive/used/epNN_*/`.
   Topics in stock: dillinger, bonnie_clyde, luciano, db_cooper, george_parker (Brooklyn Bridge), kreuger, poyais (Gregor MacGregor),
   lansky, siegel, machine_gun_kelly, dutch_schultz, escobar, lufthansa (JFK airport), prohibition, great_depression, fbi_old.
   Prefer stories that have stock photos. Look at a contact sheet first (some files may be off-topic: skip them), and put the credit
   line on screen (author/source from credits.txt, e.g. "PHOTO: FBI · PUBLIC DOMAIN"). If no photo fits, make the scene fully animated.
   Never use news/TV/film footage or copyrighted images. If Mike's PC happens to be reachable (Desktop Commander tools present),
   you MAY download extra Public-domain/CC0 Commons files there, but never depend on it.
5. Preview with `python3 render_epNN.py --frames=a,b,c` (2 frames per scene in a contact sheet) and fix overlaps or missing glyphs
   (Bebas has no arrows like →). Dry-run every 3rd frame to catch crashes, then full render (~13 min, run in background),
   `python3 mix_ep.py render_epNN`, then mux:
   `ffmpeg -i video_only.mp4 -i mix.wav -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart <name>.mp4`.
   Keep under 95 MB.

## Publishing (TikTok + YouTube Shorts, same video, 2 separate Metricool posts)
- Push the MP4 to GitHub repo Bienvenusaoulomou/recitalpha-videos (attach with add_repo, access "push"; clone --depth 1; fetch before push), folder `videos/`.
  Public URL: https://raw.githubusercontent.com/Bienvenusaoulomou/recitalpha-videos/main/videos/<name>.mp4 (check it returns 200).
- Metricool brand blogId 7611997, timezone Africa/Tunis. Make TWO createScheduledPost calls per episode at the same time
  (separate posts, so a failure on one network never blocks the other):
  1. TikTok: providers [tiktok], autoPublish true, media [URL], videoCoverMilliseconds at the hook frame (~3000–7000),
     tiktokData {privacyOption PUBLIC_TO_EVERYONE, isAigc true, title: short hook}, firstCommentText: next-episode teaser + "Follow so you don't miss it".
  2. YouTube Short: providers [youtube], autoPublish true, media [URL], no cover fields, firstCommentText "",
     youtubeData {title: hook in Title Case + 1 emoji + " #shorts" (max ~90 chars), type "short", privacy "public",
     tags: 5–7 keywords, category "EDUCATION", madeForKids false, isAiGeneratedContent false (stylized animation + real archive photos, nothing realistic-synthetic)}.
     Text: 2–3 sentence teaser + question + "#shorts" + 3–4 hashtags.
  If auto-publishing fails, create the post with draft true and say so.
- TikTok description template:
  Line 1: hook with a number + emoji. Lines 2–3: two-sentence teaser that does NOT give away the ending. Line 4: a question to drive comments.
  Then 4–5 hashtags (story-specific + #truestory #history). No #fyp.

## Report
End each run with a short message: the 2 titles, post times, Metricool planner links (TikTok + YouTube), and any fact that was softened.
