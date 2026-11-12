# ArtMath — portable project instructions

## Start every task

- Work in the GitHub repository and the selected Codex Cloud environment. Never assume this chat's old desktop files, installed tools, or Drive connection are available.
- Read README.md, docs/ARTMATH_SPEC_TH.md, and docs/MOBILE_WORKFLOW_TH.md. For episode work, read the user's current private HANDOFF before changing episode assets.
- Record the current branch and commit. Follow the user's latest brief; treat old project notes as historical evidence, not proof that current inputs passed QA.
- Respond in Thai unless the user requests another language. State verified results and blockers plainly.

## Environment and commands

Run commands from the repository root. Use Python 3.11 or 3.12 through `.venv/bin/python`.

- Prepare: `bash scripts/setup_cloud.sh`
- Check readiness: `bash scripts/setup_cloud.sh --check`
- Synthetic end-to-end check: `bash scripts/setup_cloud.sh --smoke-test`
- Tests after code changes: `.venv/bin/python -m unittest discover -s tests -v`
- Inspect footage: `.venv/bin/python tools/story_editor.py catalog <media> --out <catalog>`
- Validate an episode: `.venv/bin/python tools/dm_project.py validate <episode_dir>`
- Render: `.venv/bin/python tools/dm_project.py render <episode_dir>`
- Replace a known output only when requested: use `render <episode_dir> --overwrite`; never delete the old output first.

Use paths relative to this repository/episode. Do not depend on shell activation carrying into another command. Setup must not retrieve private media.

## Episode workflow

1. Verify actual file access, input versions, and footage evidence before writing the final shot list. Do not infer events from filenames.
2. Finalize narration before caption timing. Trim silence at most once before timing; keep `trim_voice_silences` false.
3. Follow the checked-in schema. The renderer requires 1080x1920 at 30 fps, a 1080x1264 cover panel, valid source ranges, consistent frames/speed, and timed captions.
4. Run validate before rendering. Fix all errors; evaluate warnings using the brief. `--force` does not bypass errors.
5. Inspect the exported MP4 with FFprobe and view the subtitles/crop. Listen when audio review is required. Do not claim a check was done unless it was actually performed.
6. Keep code changes separate from episode assets. Use synthetic fixtures for code tests.

### Story, footage reuse, and audio gates

- Build the story before choosing cut frequency: hook, who/where/goal, cause and consequence, escalation, then a supported payoff or cliffhanger. Document the visible action and narration supported by each chosen source interval. Introduce a new character with enough face/context footage to identify them before relying on reaction or detail shots.
- Inspect source intervals in chronological order and explain any intentional change in narrative order. A shot-length warning is not an instruction to cut every 2.2 seconds. Hold until the relevant action or reaction is understandable; do not force speed changes to fill a target duration.
- Reject reuse of the same resolved source file with overlap greater than 0.15 seconds. Crop, zoom, speed changes, cached shots, `allow_reuse`, and `--force` do not exempt a shot. Fix the shot plan before rendering. This timestamp gate does not detect identical pictures stored at different timestamps or in copied files; review those visually.
- Listen to narration and music separately before mixing. Use clean narration and instrumental music; stop and repair or replace a contaminated input when unwanted dialogue is embedded in it. Ducking is not voice isolation. Do not treat the presence of an audio stream as proof of clean audio.
- The ordinary mix uses BGM -29 LUFS / -6 dBTP before ducking with threshold 0.015, ratio 5, attack 5 ms, release 300 ms. `approved_audio` remains an already-mixed input and bypasses this mixer. Listen to the exported result before claiming audio QA passed.

## Storage and handoff

- Code, generic instructions, and empty templates belong in Git. Keep footage, voices, episode scripts/timelines, filled HANDOFF files, credentials, and signed URLs outside Git even if this repository is private.
- Use `.local/episodes/<episode-id>/` as temporary working storage. A new task may not recover these files; it must restore inputs from the user's durable storage.
- Drive integration is not built into this repository. Check the task's tools/permissions; if unavailable, report the missing input or export capability instead of inventing a link.
- End episode work with a filled private copy of templates/HANDOFF_TH.md: current commit, inputs, completed work, actual QA, durable output locations, blockers, and one next action.
- Verify uploaded/exported files can be read back before reporting them saved. If export is pending, mark `awaiting_export` and list files still needing persistence.
- Review staged files before committing; Markdown and JSON can contain private data too. Do not import the full original Drive folder into Git.

## Delivery

For software changes, provide the branch/PR, tests, and limitations. For episode work, provide actual artifact links and private HANDOFF. Do not publish videos, clone voices, or merge PRs unless covered by the user's request. No background work or ongoing synchronization is implied by these instructions.

