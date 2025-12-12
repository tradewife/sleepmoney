<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Extract transcript from https://youtu.be/SY8mvbByt30?si=DOkhLLs18aJKBRD0 and convert the step by step instructions into a workflow/harness enabling an AI IDE/CLI to perform the tasks to achieve the same results. This may involve researching alternative “work-arounds”, but let’s endeavour to find the streamlined, cost-effective approach without affecting quality.

This video describes a repeatable 5-step workflow for creating long “sleepy” YouTube videos using mostly free AI tools; below is that process converted into an AI-IDE/CLI friendly harness with streamlined, low-cost defaults while preserving quality.[^1][^2]

***

## High-level pipeline

End-to-end stages your AI IDE/CLI should orchestrate:

1. Topic discovery (low-competition, high-demand “sleepy” niche on YouTube).[^1]
2. Fact collection and validation for that topic.[^1]
3. Script structuring and narrative writing.[^1]
4. Visuals, voiceover, and background music generation.[^1]
5. Video assembly, export, and upload-ready packaging.[^1]

Each stage below is expressed as tasks that an agentic workflow can implement via tools (browser, YouTube API, file ops, HTTP calls to AI models, etc.).

***

## Stage 1: Topic discovery (sleepy-video niche finder)

**Goal:** Find an under-served but proven theme for 2–3 hour sleepy videos (philosophy, psychology, Bible, history, etc.).[^1]

**Default tools (free-first):**

- Web/YouTube search via API (or headless browser).
- General LLM (Gemini/Perplexity/ChatGPT/Claude) for pattern finding across results.[^1]

**CLI/agent tasks:**

1. `discover_base_niches`
    - Input: Broad categories, e.g. `["psychology", "philosophy", "medieval history", "bible", "game lore"]`.[^1]
    - Action:
        - For each category, query YouTube:
`"<category> facts to fall asleep to"`, filter: length ≥ 20 minutes, upload date ≤ 12 months.[^1]
        - Collect: titles, views, upload date, duration.[^1]
    - Output: JSON array of `{category, video_id, title, views, duration, uploaded_at}`.[^1]
2. `identify_winners`
    - Input: Discovery JSON from previous step.[^1]
    - Action (LLM or Python):
        - Score each category by median/mean views of long videos and recent growth (recent uploads with high views).[^1]
    - Output: Ranked list of `base_niche` with metrics and example videos.[^1]
3. `generate_subniche_hypotheses`
    - Input: Top `base_niche` (e.g. “Bible facts to sleep to”).[^1]
    - Action (LLM):
        - Ask LLM: “List 20 specific subtopics within `<base_niche>` that are popular on YouTube generally but rarely appear in sleepy / long-form relaxing videos.”[^1]
    - Output: Candidate subtopics, e.g. “Bible archaeology”, “psychology of learning fast”, etc.[^1]
4. `validate_subniche_gap`
    - For each candidate subtopic:
        - Search YouTube: `"relaxing <subtopic> to fall asleep"`, filter: ≥ 20 minutes, sort by relevance \& view count.[^1]
        - If general videos on `<subtopic>` exist with high views, but almost no long sleepy/relaxing versions, mark as *gap*.[^1]
    - Output: Final choice: `{subniche, evidence_of_demand, evidence_of_low_competition}`.[^1]

**Automation note:** Put a hard cap (e.g. stop after first 2–3 clear gaps) to keep this cheap and fast.[^1]

***

## Stage 2: Fact harvesting and validation

**Goal:** Build a pool of 80–150 short, accurate facts around the chosen subniche.[^1]

**Default tools:**

- Perplexity-style search LLM for fact mining (or your own RAG over web sources).[^1]
- Python/agent for deduplication and citation tracking.[^1]

**CLI/agent tasks:**

1. `batch_fact_generation`
    - Input: `subniche` (e.g. “Bible archaeology for sleepy video”).[^1]
    - Loop N times (e.g. 10 batches × 10 facts):
        - Prompt search-enabled LLM: “Provide 10 *distinct* concise facts about `<subniche>`. For each, output: fact_text, 1–2 credible sources (URLs). Avoid repeating previous facts.”[^1]
    - Aggregate facts across batches.
2. `dedupe_and_score_facts`
    - Action (Python/LLM):
        - Normalize text, cluster by semantic similarity, drop near-duplicates.[^1]
        - Tag: difficulty, emotional tone, and “sleepy” suitability (calm/positive, non-alarming).[^1]
    - Output: Clean JSON: `[{id, fact_text, sources[], tags[]}]`.[^1]
3. `store_facts_document`
    - Generate a `facts_<subniche>.md` or `.docx` with all facts and source links for audit/compliance.[^1]

***

## Stage 3: Script structuring and narrative writing

**Goal:** Turn unordered facts into a flowing 2–3 hour sleepy script with a calm, meditative tone.[^1]

**Cost-efficient defaults:**

- Use one main LLM with strong writing ability (Claude/GPT-4 class) for structuring and script generation.[^1]
- Keep token usage in check by chunking facts and script segments.[^1]

**CLI/agent tasks:**

1. `outline_from_facts`
    - Input: Facts JSON.[^1]
    - Action (LLM):
        - Request a high-level outline: intro, 6–10 themed sections, outro; ordered for maximum relaxation.[^1]
    - Output: `outline_<subniche>.json` with sections and assigned fact IDs.[^1]
2. `segment_fact_reordering`
    - For each section:
        - Ask LLM to reorder assigned facts for logical and emotional flow (from simple/overview to deeper or more contemplative).[^1]
    - Persist section-specific ordered lists of fact IDs.[^1]
3. `generate_script_segments`
    - For each section (10–20 minutes of reading time per segment; assume ~1500–2000 words):
        - Prompt writer LLM with:
            - Section title and ordered facts (fact_text only).
            - Style constraints: slow, soothing, present-tense or gentle narrative, minimal drama, long sentences, no harsh words, optional reflective prompts.[^1]
        - Output: Script segment text.
    - Concatenate segments into a master `script_<subniche>.txt`.
4. `sleepy_style_pass`
    - Optional second LLM pass:
        - Feed script in chunks with instruction: “Smooth and soften language for a relaxing bedtime listen, keep all factual content intact.”[^1]
    - Output: Final script file, plus estimated duration based on reading speed (e.g. 130–150 wpm).[^1]

***

## Stage 4: Assets — visuals, voiceover, music

### 4A. Visual generation (AI images)

**Goal:** Generate 10–40 looping backgrounds that match the theme.[^1]

**Free/cheap options:**

- Leonardo free tier for widescreen, commercially usable images.[^1]
- Alternatives: Stable Diffusion locally, Playground, etc. with commercial-use friendly models.[^1]

**CLI/agent tasks:**

1. `derive_visual_prompts`
    - From outline sections, ask LLM for 1–3 scene prompts per section, e.g.
“soft, dimly-lit ancient library with warm candlelight and scrolls – cinematic, 16:9, no text, calm composition”.[^1]
2. `call_image_generator`
    - For each prompt:
        - Invoke Leonardo or SD API with:
            - Aspect ratio 16:9.
            - Style: photographic / painterly but not busy.
            - 4 variants per prompt.

```
- Store as `images/<subniche>/<section>_<index>.png`.[^1]
```

3. `select_final_images`
    - Optional LLM-vision filter or simple heuristic (reject images with text, faces, artifacts).
    - Output: Ordered list of chosen images and intended on-screen duration (e.g. each 15–30 seconds).[^1]

### 4B. Voiceover generation

**Goal:** Generate a single long audio file matching the script; free-first, but allow premium for scale.[^1]

**Options aligned with the video:**

- 100% free but chunked: Clipchamp TTS (Microsoft).[^1]
- Free trial / cheap: CapCut Pro TTS.[^1]
- High quality \& fast: ElevenLabs with paid plan for commercial license.[^1]

**Streamlined, cost-conscious defaults for automation:**

- For first version: use a free or trial TTS that allows ≥ 10,000 characters per call (e.g. CapCut or an open-source TTS API).[^1]
- For production with monetization: support ElevenLabs path with a config switch.[^1]

**CLI/agent tasks:**

1. `chunk_script_for_tts`
    - Input: `script_<subniche>.txt`, `max_chars` per TTS call.[^1]
    - Action: Split on paragraph boundaries, keeping within limits, tag chunk order.[^1]
    - Output: `tts_chunks.json`.
2. `select_voice_profile`
    - Config or interactive selection:
        - Gender, accent, meditative/relaxing style, pace (slower than default).[^1]
    - If using ElevenLabs:
        - Choose voice from “meditative” or similar category and persist voice_id.[^1]
3. `generate_tts_audio`
    - For each chunk:
        - Call TTS API with text, voice, speed, pitch adjustments for calm tone.[^1]
        - Save `audio/chunk_<n>.wav`.
    - If API supports full-script upload (e.g. ElevenLabs Studio), allow one-shot generation to a single file.[^1]
4. `merge_audio_chunks`
    - If multiple chunks:
        - Concatenate into `audio/voiceover_full.wav` and normalize loudness.[^1]

### 4C. Background music

**Goal:** Long, royalty-free ambient track with no content ID fingerprint.[^1]

**Source pattern:**

- Use a site like Pixabay music, filter for “meditation / ambient” and avoid tracks with digital fingerprint / content ID flags.[^1]

**CLI/agent tasks:**

1. `search_royalty_free_music`
    - Input: Mood keywords (e.g. “ambient meditation 2 hour”), BPM range.[^1]
    - Action:
        - Scrape or API search; only accept tracks explicitly labeled commercial use without attribution and without fingerprint flag.[^1]
    - Output: Chosen track URL and license metadata.
2. `prepare_music_loop`
    - Download track as `music/base_track.wav`.
    - Loop and crossfade to cover full voiceover length plus padding:
        - Generate `music/background_loop.wav` of equal or longer duration than `voiceover_full.wav`.[^1]
    - Set base music gain (e.g. –20 to –30 dB relative to speech).[^1]

***

## Stage 5: Video assembly \& export

**Goal:** Auto-assemble timeline: voiceover + image slideshow + background music, then render to H.264 for YouTube.[^1]

**Tools:**

- Desktop NLE (CapCut, DaVinci Resolve, Premiere) if user-facing.[^1]
- For full CLI automation, use FFmpeg or a programmatic editor (e.g. MoviePy, ffmpeg-python).[^1]

**CLI/agent tasks (FFmpeg-based version):**

1. `plan_slideshow_timeline`
    - Input:
        - `voiceover_full_duration`
        - List of selected images and preferred per-image duration (e.g. 20–30 seconds).[^1]
    - Action:
        - Compute number of slots = ceil(voiceover_duration / per_image_duration).
        - Cycle images if fewer images than slots.[^1]
    - Output: `timeline.json` with array of `{image_path, start_time, duration}`.[^1]
2. `render_slideshow_video`
    - Use FFmpeg filters:
        - Create a video stream from images with transitions (crossfade or simple cuts).
    - Output: `video/slideshow_raw.mp4`.
3. `mix_audio_tracks`
    - Combine `voiceover_full.wav` and `background_loop.wav`:
        - Voice at 0 dB reference, music ducked to –20 dB and sidechained if needed.[^1]
    - Output: `audio/mix_final.wav`.
4. `mux_video_and_audio`
    - Combine `slideshow_raw.mp4` and `mix_final.wav` into final container:
        - Codec: H.264 video, AAC audio.
        - Resolution: 1920×1080.
    - Output: `final/<subniche>_sleep_video.mp4`.
5. `compress_if_needed`
    - If filesize is extremely large, optionally:
        - Slightly reduce bitrate, but keep quality acceptable for YouTube (e.g. 8–12 Mbps for 1080p long-form).[^1]

***

## Optional: Upload \& channel optimization

These steps were implied in the original business explanation (getting monetized quickly) but not deeply detailed, so the harness can include:

1. `generate_title_description_tags`
    - Use LLM:
        - SEO-optimized but calm title.
        - Description including:
            - Topic summary.
            - Timestamps for major sections.
            - Disclosure if AI-generated voice/images used.
        - Tags/keywords list.[^1]
2. `youtube_upload`
    - Use YouTube Data API for:
        - Upload video.
        - Set title, description, tags, playlist, thumbnail.[^1]
3. `thumbnail_generation`
    - Generate one still image via AI (Leonardo/SD) with large, clear text and calm visuals; export as PNG.[^1]

***

## Streamlining \& cost-control switches

To make this IDE/CLI harness adaptable, expose config flags:

- `use_premium_tts` (boolean): if true, route to ElevenLabs; else use free/OSS.[^1]
- `max_fact_batches`, `max_outline_sections`, `script_target_hours`: to cap token usage.[^1]
- `image_count_target`, `per_image_duration_sec`: trade-off between variety and generation cost.[^1]
- `auto_upload` vs `manual_upload`.[^1]

The net result is an automated pipeline that replicates the video’s one-person AI business workflow but optimized for an AI IDE/CLI: minimal manual input (mainly niche preferences and final approval), heavy lifting done by orchestrated agents, and flexible choice between free and premium tools depending on budget and monetization goals.[^1]
<span style="display:none">[^10][^3][^4][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://www.linkedin.com/pulse/4-hour-ai-workflow-builds-income-while-you-sleep-manoj-yadav-rsdof

[^2]: https://www.entrepreneur.com/leadership/want-to-succeed-on-youtube-ask-yourself-this-one-question/346406

[^3]: https://www.youtube.com/watch?v=SY8mvbByt30

[^4]: https://www.youtube.com/watch?v=OkqHjlSoZz4

[^5]: https://viqsolutions.com/transcription-services/

[^6]: https://www.youtube.com/watch?v=Q0rocxV50is

[^7]: https://viqsolutions.com/transcription-services/criminal-justice-transcription/

[^8]: https://www.youtube.com/watch?v=8x3HB62C4OE

[^9]: https://www.youtube.com/watch?v=mvHG-evNuOE

[^10]: https://ytscribe.com

