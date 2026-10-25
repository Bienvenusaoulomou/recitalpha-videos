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

## Story choice (first)
- Prefer LITTLE-KNOWN true stories (see "Story choice rule" in stories_log.md). Famous stories are retold by hundreds of accounts.

## Retention lessons (YouTube Studio, first 4 Shorts, 2026-10-25)
- EP01 Ponzi (1:29): 73.5% average watched (1:05 avg). Best by far. Every scene revealed a new NUMBER that escalated
  ($100 -> $200, 50% in 45 days, $10M, 160 million vs 27,000 coupons, -$20M). Simple visual payoff in the first 5 s ("PAID").
- EP02 Eiffel (1:33): 35.6% (0:33). EP03 Capone (1:18): 44.7% (0:34). EP04 Brink's (1:32): 35.1% (0:32).
  => Viewers leave at ~0:32-0:34, i.e. scenes 4-5, where those episodes slowed down with setup/background.
Rules from now on:
1. Target 65-80 s total (still over 62 s). Cut biography/background scenes; start the action by 0:10.
2. Every scene must reveal something new: a number, a twist or a reversal. No "setup only" scenes.
3. Put a re-hook at ~0:25-0:30 ("But that wasn't the crazy part...", "Then it got worse.") with a big on-screen line.
4. Prefer escalating numbers like EP01 (counters, bars, before/after).
5. Re-hook scene: add a scene with id "rehook" (2 short sentences) and use props.make_rehook(...). See script_ep05_lufthansa.py / script_ep06_poyais.py (v2 cuts).

## YouTube Studio advice (2026-10-25): "viewed vs swiped away" was only 41-45% (goal 70-80%)
Apply to EVERY new episode:
1. Frame 0 = the hook. Hook text and main visual at FULL opacity at t=0 (no fade-in), voice starts at once (gen_audio LEAD=0.08).
   First spoken line = the most absurd true fact in under 2 seconds.
2. Something new on screen every 2-3 seconds (new number, stamp, photo zoom, keyword pop). No static scene longer than 3 s.
3. TWO CUTS PER EPISODE (same research, same scene functions):
   - TikTok cut: 62-75 s (TikTok Creator Rewards needs > 60 s). Ends with next-episode teaser + Follow.
   - YouTube Shorts cut: 35-50 s. Keep hook + the 4-5 strongest number/twist scenes + re-hook. No spoken "Follow".
     End with a SEAMLESS LOOP: the last sentence must flow straight back into the first sentence
     (e.g. last: "...and that is how" -> first: "Six masked men walked out of JFK with five million dollars.").
     Put the next-episode teaser in the YouTube description instead.
   How: epNN/ (TikTok) and epNN/yt/ (YouTube) each with its own script.py (yt SCENES = subset/shortened, same scene ids so wt() words exist),
   own timeline.json/voice.wav. In render_epNN.py use os.environ.setdefault("REC_ROOT", "/home/claude/epNN") and
   sys.path.insert(0, os.environ["REC_ROOT"]) so the same file renders both cuts: REC_ROOT=/home/claude/epNN/yt python3 render_epNN.py.
   Copy img/, fonts, models links into yt/. Name files Recitalpha_EPNN_<slug>.mp4 and Recitalpha_EPNN_<slug>_yt.mp4.
4. YouTube post uses the _yt file; TikTok post uses the long file.

## Motion design FX v2 (2026-10-25, engine.py) — "be the best in the niche"
- engine.FX = True (default): whip-pan transitions with motion blur + gold light sweep between scenes, punch-zoom + shake + flash on
  every impact (call E.set_hits(IMPACTS) in the render module), moving light leak, rising gold embers.
- B-roll: E.BROLL[scene_id] = E.load_broll(path, start, dur, alpha=0.7-0.8, credit=...) plays real footage behind a scene,
  sepia-graded with a dark gradient so text stays readable. Library: archive/broll/ (see credits.txt). Only Public domain / CC0 clips.
  Memory: keep total b-roll under ~25 s per render (cgroup OOM kills renders above ~2 GB).
- Reference wrappers: ep05/ep06 render_fx.py (engine/render_ep05_fx_wrapper.py, render_ep06_fx_wrapper.py) incl. YouTube loop-end scene.

## Hook rules (first 3 seconds decide everything)
- Never open with "In 19XX, ..." or a name. Open with the absurd fact or a question, e.g. "This woman got banks to lend her millions... with one fake signature."
- Frame 1 must already show the hook text big on screen (no fade-in from black).
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
   Helpers (copy to /home/claude/tools/): `python3 preview.py /home/claude/epNN render_epNN.py` writes contact.jpg (frame 0 + 2 frames
   per scene); `python3 dryrun.py render_epNN` (run inside the episode dir) draws every 3rd frame. Two episodes can render in parallel
   in the background (~20 min on 2 cores). Note: `archive/stock/lufthansa/` is an off-topic 1976 Ford contact sheet; don't use it.

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
