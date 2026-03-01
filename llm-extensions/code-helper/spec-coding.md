# Try spec-kit: plan and task
really complex for a mid project



# Implementation Tasks: Auto-2D-Media Studio

**Feature**: Auto-2D-Media Studio  
**Branch**: `001-auto-2d-studio`  
**Date**: 2026-03-01  
**Status**: Phase 1 Design - Ready for Implementation

---

## Overview

This document breaks down the Auto-2D-Media Studio implementation into independent, testable tasks organized by user story. Each task is specific enough for an LLM or developer to complete without additional context.

**Architecture**: Python FastAPI backend + Vue 3 frontend + Plugin system  
**Key Technologies**: 
- Backend: FastAPI, Pydantic, Direct SDK (Deepseek/Qwen/GLM/MiniMax)
- Frontend: Vue 3, Pinia, @vueuse/core
- TTS: GPT-SoVITS (port 9872) or VITS (port 23456)
- Rendering: PixiJS for sprite animation

**MVP Scope**: User Stories 1 + 2 (Load Project + Auto-Parse Script)  
**Full Scope**: All 5 user stories with playback and export

---

## Phase 1: Setup & Infrastructure

### 1.1 Project Structure & Dependencies

- [ ] T001 Create project folder structure with backend/, frontend/, plugins/, tests/, docs/ directories
- [ ] T002 [P] Create backend/pyproject.toml with FastAPI, Pydantic, openai, requests, pytest, Ruff
- [ ] T003 [P] Create frontend/package.json with Vue 3, Pinia, Vite, @vueuse/core, PixiJS, Vitest, ESLint
- [ ] T004 Create backend/.env.example with LLM config (Deepseek primary, Qwen fallback), TTS endpoints
- [ ] T005 Create frontend/.env.example with Backend API URL (http://localhost:8000)
- [ ] T006 Create .gitignore for Python (__pycache__, .venv, *.pyc) and Node (node_modules/, dist/, .env)

### 1.2 Backend Core Setup

- [ ] T007 [P] Create backend/src/main.py with FastAPI app initialization, CORS setup, error handlers
- [ ] T008 [P] Create backend/src/config.py with environment variable loading (LLM, TTS, logging)
- [ ] T009 [P] Create backend/src/utils/logger.py for ACTION_LOG.md minimalist logging
- [ ] T010 [P] Create backend/src/utils/file_safe.py with smart backup policy (.orig, .bak1, .bak2)
- [ ] T011 Create backend/tests/conftest.py with pytest fixtures for test projects, test scripts, temp folders

### 1.3 Frontend Core Setup

- [ ] T012 [P] Create frontend/src/main.ts with Vue 3 app initialization, router, Pinia stores
- [ ] T013 [P] Create frontend/src/App.vue with root layout (sidebar, main editor, preview panel)
- [ ] T014 Create frontend/vite.config.ts with dev server config, path aliases, PixiJS setup
- [ ] T015 Create frontend/src/types/models.ts with TypeScript interfaces mirroring backend Pydantic models

---

## Phase 2: Foundational (Blocking Prerequisites for All User Stories)

### 2.1 Data Models & Schemas

- [ ] T016 Create backend/src/models/project.py with Pydantic models: Project, ProjectState, AssetMetadata, Character, Asset
- [ ] T017 Create backend/src/models/timeline.py with models: TimelineRow, Timeline, Scene, Emotion, Action enums
- [ ] T018 Create backend/src/models/parser.py with ParseResult, SceneList, DialogueLine models
- [ ] T019 [P] Create backend/src/models/tts_queue.py with TTSQueueItem, TTSStatus, TTSRequest models

### 2.2 LLM Parser Service (Direct SDK + Caching)

- [ ] T020 Create backend/src/services/parser.py with ScriptParser class (~50 lines):
  - Constructor with api_key, model, cache_dir, provider (Deepseek default)
  - parse() method with script hash caching (SHA256)
  - Fallback chain: Deepseek → Qwen → GLM → Regex parser
  - Token counting and cost calculation (pricing table for all 10 models)
- [ ] T021 Add ScriptParser._build_prompt() with few-shot examples for emotion/action extraction
- [ ] T022 Add ScriptParser._parse_response() to extract JSON scenes from LLM output
- [ ] T023 [P] Add ScriptParser._calculate_cost() with pricing for Deepseek, Qwen, GLM, MiniMax, OpenAI
- [ ] T024 Add ScriptParser._try_fallback() to switch providers on API error

### 2.3 File Management Service

- [ ] T025 Create backend/src/services/project_manager.py with ProjectManager class:
  - load_project(folder_path) → Project + ProjectState
  - save_project(project) → writes project.json, config.json with file_safe backup
  - get_project_assets(folder_path) → lists images/characters/, images/backgrounds/, voice_models/
  - scan_project_folder(path) → auto-detect available assets
- [ ] T026 Add ProjectManager.initialize_project(folder_path, name) to create new project structure
- [ ] T027 Add ProjectManager.validate_project(project) to check required files and folder structure

### 2.4 TTS Service

- [ ] T028 Create backend/src/services/tts_service.py with TTSService class:
  - queue_tts(timeline_row) → async TTS request to GPT-SoVITS or VITS
  - get_queue_status() → returns list of pending TTS items and progress
  - generate_audio(character, text, emotion) → calls external TTS API, saves to audio/ folder
  - Support GPT-SoVITS endpoint (9872) and VITS (23456) with configurable switching
- [ ] T029 Add TTSService.health_check() to verify TTS endpoint availability on startup

### 2.5 API Routes (Basic CRUD)

- [ ] T030 [P] Create backend/src/api/routes.py with FastAPI routes:
  - POST /api/v1/project/load → load project from folder path
  - GET /api/v1/project/{project_id} → return project state
  - POST /api/v1/project/{project_id}/save → save project state
- [ ] T031 Create backend/src/api/deps.py with dependency injection for services (ProjectManager, ScriptParser, TTSService)

### 2.6 Frontend Pinia Stores

- [ ] T032 [P] Create frontend/src/stores/projectStore.ts with Pinia store:
  - State: folderPath, projectName, characters, assets, metadata
  - Actions: loadProject(path), setProjectName(name), addAsset(asset)
  - Getters: hasProject, projectCharacters, projectAssets
- [ ] T033 [P] Create frontend/src/stores/timelineStore.ts with Pinia store + VueUse history:
  - State: rows (TimelineRow[]), selectedRowId
  - History: useHistory() with 50-state capacity for undo/redo
  - Actions: addRow(row), updateRow(id, updates), deleteRow(id), undo(), redo()
  - Getters: selectedRow, rowCount, canUndo, canRedo
- [ ] T034 Create frontend/src/stores/uiStore.ts with Pinia store:
  - State: isLoading, error, playbackState, selectedTab
  - Actions: setLoading(bool), setError(msg), setPlaybackState(state)

---

## Phase 3: User Story 1 - Load & Manage Project Folder (P1)

### 3.1 Backend: Project Loading

- [ ] T035 [US1] Implement ProjectManager.load_project() to:
  - Read script.txt from folder
  - Detect and list character images (images/characters/{name}/*.png)
  - Detect background images (images/backgrounds/*.png)
  - Load project.json if exists, else initialize empty ProjectState
  - Return Project object with all metadata
- [ ] T036 [US1] Implement ProjectManager.save_project() to:
  - Write project.json to .a2d-studio/ with file_safe backup
  - Create .a2d-studio/cache/ for script parsing cache
  - Log action to ACTION_LOG.md: [timestamp] | Project Save | {project_id} | {size}

### 3.2 Backend: API for Project Load/Save

- [ ] T037 [US1] Implement POST /api/v1/project/load endpoint:
  - Accept folder_path parameter
  - Call ProjectManager.load_project()
  - Return Project JSON with all assets and metadata
  - Error handling: folder not found, invalid structure
- [ ] T038 [US1] Implement GET /api/v1/project/{project_id} endpoint:
  - Return current project state from memory
  - Return 404 if project not loaded
- [ ] T039 [US1] Implement POST /api/v1/project/{project_id}/save endpoint:
  - Accept project state JSON
  - Call ProjectManager.save_project()
  - Return 200 OK with save timestamp

### 3.3 Frontend: Project Loader Component

- [ ] T040 [US1] Create frontend/src/components/ProjectLoader.vue:
  - Folder picker button (using file system API)
  - Display selected folder path
  - Button to "Load Project"
  - Display loaded project name and asset counts (characters, backgrounds)
- [ ] T041 [US1] Create frontend/src/pages/Home.vue:
  - Project loader component
  - List of recent projects (from localStorage)
  - Button to open recent project or pick new folder

### 3.4 Frontend: Session Persistence

- [ ] T042 [US1] Implement projectStore.loadProject() to:
  - Call POST /api/v1/project/load with folder_path
  - Save projectState to localStorage (for recovery)
  - Dispatch uiStore.setLoading(false)
  - Navigate to Editor page
- [ ] T043 [US1] Implement auto-save in projectStore:
  - On any mutation (addRow, updateRow, deleteRow), call POST /api/v1/project/{id}/save
  - Debounce saves to 2 seconds (avoid excessive API calls)
  - Log save status to console

### 3.5 Tests for User Story 1

- [ ] T044 [US1] Test backend: test_project_manager_load_valid_folder
  - Create temp folder with script.txt and images/
  - Load project, verify Project object created with correct assets
- [ ] T045 [US1] Test backend: test_project_manager_save_and_restore
  - Create project, save with file_safe backup, verify .orig/.bak1 files exist
  - Modify project, save again, verify .bak1 rotated to .bak2
- [ ] T046 [US1] Test backend: test_api_project_load_endpoint
  - POST /api/v1/project/load with valid folder, verify 200 OK and Project JSON returned
  - POST with invalid folder, verify 404 error
- [ ] T047 [US1] Test frontend: test_projectStore_load_and_restore
  - Load project via store, verify folderPath and projectName set
  - Close app, reload from localStorage, verify state restored
- [ ] T048 [US1] Test frontend: test_ProjectLoader_component_rendering
  - Render ProjectLoader component, verify folder picker and load button visible
  - Click load, verify project state updates

---

## Phase 4: User Story 2 - Auto-Parse Script & Generate Timeline (P1)

### 4.1 Backend: Script Parsing (LLM-Powered)

- [ ] T049 [US2] Implement ScriptParser.parse() end-to-end:
  - Accept script.txt content and character_list
  - Check cache by SHA256 hash (no API call if cached)
  - Call Deepseek LLM with few-shot prompt (fallback chain: Qwen → GLM → Regex)
  - Extract scenes, dialogue lines, character assignments, emotions
  - Calculate cost and log to ACTION_LOG.md
  - Return ParseResult with scenes, tokens_used, cost
- [ ] T050 [US2] Create ScriptParser._build_prompt() with:
  - System prompt: "Analyze visual novel scripts. Extract scenes, dialogue, emotions, actions."
  - Few-shot examples: show 2-3 correct scene/dialogue/emotion extractions
  - User input: script content with character list
- [ ] T051 [US2] Implement fallback parser (regex-based):
  - Parse simple format: [CHARACTER] / {EMOTION} / dialogue text
  - Return scenes with detected characters and emotions (fallback only)
  - Used when LLM unavailable (network error, API timeout)

### 4.2 Backend: TTS Generation

- [ ] T052 [US2] Implement TTSService.generate_audio():
  - Accept character, dialogue_text, emotion
  - Build TTS request (model ID, voice clone if applicable)
  - Call external TTS API (GPT-SoVITS or VITS)
  - Save WAV file to project/audio/ with naming: scene_{scene_id}_line_{line_id}.wav
  - Return audio file path
- [ ] T053 [US2] Implement TTSService.queue_tts() for async processing:
  - Create TTSQueueItem with dialogue line metadata
  - Add to async queue (asyncio.Queue)
  - Worker processes queue items in parallel (up to 5 concurrent TTS calls)
  - Broadcast progress via WebSocket (optional for MVP)
- [ ] T054 [US2] Implement TTSService health_check():
  - Test connectivity to TTS endpoint on startup
  - Log availability to ACTION_LOG.md
  - Warn user if TTS unavailable, offer "generate audio later" option

### 4.3 Backend: Timeline Generation API

- [ ] T055 [US2] Implement POST /api/v1/timeline/parse endpoint:
  - Accept project_id and script_content
  - Call ScriptParser.parse()
  - Queue TTS generation for all dialogue lines
  - Return Timeline JSON with all rows, TTS status
- [ ] T056 [US2] Implement GET /api/v1/tts/status endpoint:
  - Return current TTS queue status (total items, completed, pending, progress %)
  - Allow UI to show progress bar
- [ ] T057 [US2] Implement POST /api/v1/timeline/rows endpoint:
  - Accept list of TimelineRow updates (from parsing)
  - Persist to project.json
  - Return 200 OK with updated timeline

### 4.4 Frontend: Timeline Editor Table

- [ ] T058 [US2] Create frontend/src/components/TimelineEditor.vue:
  - Table with columns: Scene, Character, Dialogue, Emotion, Action, Audio File
  - Display all TimelineRow objects from timelineStore
  - Read-only for now (editing in User Story 3)
- [ ] T059 [US2] Create frontend/src/pages/Editor.vue:
  - Layout: sidebar (project info), main (timeline table), preview panel
  - Button to "Generate Timeline" → calls POST /api/v1/timeline/parse
  - Progress bar for TTS generation (polls GET /api/v1/tts/status every 1 sec)

### 4.5 Frontend: Timeline State Management

- [ ] T060 [US2] Implement timelineStore.generateTimeline() action:
  - Call POST /api/v1/timeline/parse with project_id and script
  - Poll GET /api/v1/tts/status to show progress
  - On completion, update timelineStore.rows with all rows
  - Save to project.json via POST /api/v1/project/{id}/save
- [ ] T061 [US2] Implement timelineStore.rows as reactive array:
  - Bind to TimelineEditor table rows
  - Update when parsing completes

### 4.6 Tests for User Story 2

- [ ] T062 [US2] Test backend: test_parser_deepseek_integration
  - Set LLM_API_KEY for Deepseek in .env
  - Parse 2-scene script with 5 dialogue lines
  - Verify scenes extracted, characters assigned, emotions detected
  - Verify token cost calculated and logged
- [ ] T063 [US2] Test backend: test_parser_cache_hit
  - Parse same script twice, verify cache hit on second call (zero cost)
- [ ] T064 [US2] Test backend: test_parser_fallback_to_regex
  - Set LLM_API_KEY to invalid value
  - Parse script, verify fallback to regex parser (less accurate but functional)
- [ ] T065 [US2] Test backend: test_tts_service_generate_audio
  - Set TTS_ENDPOINT to live GPT-SoVITS or VITS
  - Generate audio for sample dialogue, verify WAV file created
- [ ] T066 [US2] Test backend: test_api_timeline_parse_endpoint
  - POST /api/v1/timeline/parse with valid project_id and script
  - Verify 200 OK and Timeline JSON with rows returned
  - Verify audio files created in project/audio/
- [ ] T067 [US2] Test frontend: test_Editor_page_renders
  - Navigate to Editor page, verify sidebar, timeline table, preview panel visible
- [ ] T068 [US2] Test frontend: test_generate_timeline_button
  - Click "Generate Timeline" button
  - Verify progress bar shows
  - Verify timeline table populated on completion

---

## Phase 5: User Story 3 - Director's Edit Interface (P2)

### 5.1 Backend: Row Update API

- [ ] T069 [US3] Implement POST /api/v1/timeline/rows/{row_id} endpoint:
  - Accept TimelineRow with updated character, dialogue, emotion, action
  - Update in memory and persist to project.json
  - Return 200 OK with updated row
- [ ] T070 [US3] Implement POST /api/v1/timeline/rows/{row_id}/regenerate-audio endpoint:
  - Accept updated dialogue text
  - Call TTSService.generate_audio() with new text
  - Save new WAV file, replace path in timeline row
  - Return updated row with new audio file path

### 5.2 Frontend: Inline Editing in Timeline Table

- [ ] T071 [US3] Update TimelineEditor.vue to support inline editing:
  - Make Dialogue column text input editable (contenteditable or input field)
  - Make Emotion column a dropdown (select from standard emotion enum)
  - Make Action column a dropdown (select from action enum: slide, jump, wave, nod, shake, fade, none)
  - Make Character column a dropdown (select from project.characters)
- [ ] T072 [US3] Add "Regenerate Audio" button per row:
  - On click, show loading spinner
  - Call POST /api/v1/timeline/rows/{id}/regenerate-audio
  - Replace audio file in project/audio/
  - Update row.audioPath in timeline
- [ ] T073 [US3] Implement auto-save for edited rows:
  - On blur/change of any cell, call POST /api/v1/timeline/rows/{id}
  - Debounce to 1 second
  - Show save status (checkmark or spinner)

### 5.3 Frontend: Undo/Redo for Timeline Edits

- [ ] T074 [US3] Implement timelineStore.updateRow() with history tracking:
  - Update row in timelineStore.rows
  - VueUse useHistory() auto-tracks this mutation
  - User can Ctrl+Z to undo or Ctrl+Y to redo
- [ ] T075 [US3] Add Undo/Redo buttons to Editor UI:
  - Display "Undo" and "Redo" buttons (enabled based on canUndo, canRedo)
  - Show keyboard shortcut hints (Ctrl+Z, Ctrl+Y)

### 5.4 Tests for User Story 3

- [ ] T076 [US3] Test backend: test_update_timeline_row
  - Update row dialogue text, emotion, action
  - Verify POST returns updated row, changes persisted in project.json
- [ ] T077 [US3] Test backend: test_regenerate_audio_for_row
  - Edit dialogue text, call regenerate endpoint
  - Verify new audio file created, old file replaced
- [ ] T078 [US3] Test frontend: test_TimelineEditor_inline_edit_dialogue
  - Edit dialogue text cell, blur, verify POST called
  - Verify save status shown, change persisted to store
- [ ] T079 [US3] Test frontend: test_emotion_dropdown_select
  - Click emotion cell, select new emotion, verify POST called and row updated
- [ ] T080 [US3] Test frontend: test_undo_redo_timeline_edits
  - Edit row (change dialogue), press Ctrl+Z, verify change undone
  - Press Ctrl+Y, verify change redone

---

## Phase 6: User Story 4 - Playback / Story Replay (P2)

### 6.1 Backend: Playback Instructions API

- [ ] T081 [US4] Implement GET /api/v1/playback/{project_id} endpoint:
  - Return playback instructions JSON with:
    - Timeline rows in order
    - Background image path for each scene
    - Character sprite paths (default emotion)
    - Audio file paths
    - Animation timing (duration per action)
  - Example: { "scenes": [{ "background": "path", "actions": [...] }] }

### 6.2 Frontend: Playback Engine

- [ ] T082 [US4] Create frontend/src/services/playbackEngine.ts:
  - Class PlaybackEngine to orchestrate scene playback
  - Methods: play(), pause(), resume(), seekToScene(index), skipScene()
  - State: currentScene, currentLineIndex, isPlaying, timestamp
- [ ] T083 [US4] Implement PlaybackEngine.play():
  - Load playback instructions from backend
  - Display background image
  - For each timeline row:
    - Show character sprite with current emotion
    - Play audio file
    - Trigger animation (slide-in, jump, etc.)
    - Wait for audio to finish before next line

### 6.3 Frontend: Scene Preview Component (PixiJS)

- [ ] T084 [US4] Create frontend/src/components/ScenePreview.vue:
  - PixiJS canvas for rendering sprites
  - Display background image (fullscreen or container-fit)
  - Render character sprites with PixiJS (support multiple characters per scene)
  - Trigger animations via PixiJS transitions (slide-in, jump, fade)
- [ ] T085 [US4] Implement sprite animations in PixiJS:
  - slide-in: Move sprite from left/right edge to center (duration: 500ms)
  - jump: Move sprite up/down with easing (duration: 300ms)
  - fade: Opacity transition (duration: 300ms)
  - wave: Sprite wave animation (duration: 500ms, custom tween)

### 6.4 Frontend: Playback Controls

- [ ] T086 [US4] Create frontend/src/components/PlaybackControls.vue:
  - Play button (triangular play icon)
  - Pause button (two vertical bars)
  - Resume button (when paused)
  - Progress bar showing current position / total duration
  - Scene selector dropdown (jump to scene X)
  - Speed control slider (0.5x, 1x, 1.5x, 2x)
- [ ] T087 [US4] Bind controls to PlaybackEngine:
  - onClick Play → playbackEngine.play()
  - onClick Pause → playbackEngine.pause()
  - onClick Resume → playbackEngine.resume()
  - onChange SceneSelector → playbackEngine.seekToScene(index)
  - onChange SpeedSlider → playbackEngine.setSpeed(rate)

### 6.5 Frontend: Audio Sync

- [ ] T088 [US4] Implement audio playback in PlaybackEngine:
  - Use HTML5 Audio API to play WAV files
  - Sync sprite animations to audio playback (start animation when audio starts)
  - Wait for audio to finish before advancing to next line
  - Handle audio errors (file missing, corrupted) gracefully

### 6.6 Tests for User Story 4

- [ ] T089 [US4] Test backend: test_playback_instructions_api
  - GET /api/v1/playback/{project_id}, verify JSON structure
  - Verify all background paths, sprite paths, audio paths present
- [ ] T090 [US4] Test frontend: test_ScenePreview_renders_background
  - Load scene with background, verify background image displayed in PixiJS canvas
- [ ] T091 [US4] Test frontend: test_sprite_animation_slide_in
  - Trigger slide-in animation, verify sprite moves from edge to center over 500ms
- [ ] T092 [US4] Test frontend: test_playback_audio_sync
  - Start playback, verify audio plays when dialogue line reached
  - Verify sprite animation starts at same time as audio
- [ ] T093 [US4] Test frontend: test_pause_resume_playback
  - Play scene, pause, verify audio paused and sprite frozen
  - Resume, verify audio continues from paused timestamp, animation resumes

---

## Phase 7: User Story 5 - Export Timeline & Generate Output (P3)

### 7.1 Backend: Export API

- [ ] T094 [US5] Implement POST /api/v1/timeline/export endpoint:
  - Accept project_id and export_format (json, renpy, webgal)
  - Serialize timeline to structured format
  - Write to project/export/ folder
  - Return file path of exported file
- [ ] T095 [US5] Implement JSON export:
  - Serialize Timeline to JSON with all metadata (scenes, rows, paths, costs)
  - Include formatting and indentation for readability
- [ ] T096 [US5] Implement Ren'Py export plugin:
  - Use plugin system to load exporter_renpy.py
  - Convert timeline to Ren'Py DSL (define characters, scenes, dialogue)
  - Write .rpy file

### 7.2 Frontend: Export UI

- [ ] T097 [US5] Create frontend/src/components/ExportDialog.vue:
  - Dialog box with export format selector (JSON, Ren'Py)
  - Export button
  - Show exported file path on success
- [ ] T098 [US5] Add Export button to Editor page:
  - Trigger ExportDialog when clicked
  - Call POST /api/v1/timeline/export with selected format
  - Show success message with file location

### 7.3 Tests for User Story 5

- [ ] T099 [US5] Test backend: test_export_timeline_to_json
  - Create complete timeline, export to JSON
  - Verify JSON file created with all metadata
  - Re-import JSON, verify no data loss
- [ ] T100 [US5] Test backend: test_export_timeline_to_renpy
  - Export timeline to Ren'Py DSL
  - Verify .rpy file created with character definitions and scenes
- [ ] T101 [US5] Test frontend: test_ExportDialog_renders
  - Click Export button, verify dialog shown with format options
- [ ] T102 [US5] Test frontend: test_export_workflow_end_to_end
  - Complete timeline editing, click Export, select JSON, verify file downloaded/saved

---

## Phase 8: Polish & Cross-Cutting Concerns

### 8.1 Error Handling & Validation

- [ ] T103 Implement comprehensive error handling in backend:
  - Custom exception classes (ProjectNotFound, InvalidScript, TTSError, LLMError)
  - Global error handler returning 400/404/500 with error message
  - Validate project structure before loading
  - Validate API request payloads with Pydantic
- [ ] T104 Implement error handling in frontend:
  - Try/catch for all API calls
  - User-friendly error messages in ErrorDialog component
  - Fallback UI when API unavailable
- [ ] T105 Add input validation:
  - Script validation (check script.txt exists, not empty)
  - Character validation (ensure used characters defined)
  - Emotion validation (restrict to standard emotion set)
  - Action validation (restrict to valid action enums)

### 8.2 Logging & Monitoring

- [ ] T106 Implement ACTION_LOG.md minimalist logging:
  - Log format: [timestamp] | [action] | [target] | [result]
  - Log all API calls, file operations, LLM calls, TTS generation
  - Log costs: token usage, TTS duration, total project cost
- [ ] T107 Add performance logging:
  - Log script parsing time, TTS generation time per line
  - Alert if any operation exceeds performance targets
- [ ] T108 Add user action logging:
  - Log timeline edits, undo/redo, playback start/stop, export

### 8.3 Testing Coverage

- [ ] T109 Achieve 80% statement coverage for core modules:
  - backend/src/models/ (100%)
  - backend/src/services/ (80%+)
  - backend/src/api/ (80%+)
  - frontend/src/stores/ (80%+)
- [ ] T110 Write integration tests:
  - Full workflow: load → parse → edit → playback → export
  - Cross-module interactions (ProjectManager + ScriptParser + TTSService)
- [ ] T111 Write contract tests:
  - Backend API contract (request/response JSON validation)
  - Frontend→Backend API compatibility

### 8.4 Documentation

- [ ] T112 Create docs/ARCHITECTURE.md:
  - High-level design overview
  - Component diagram (Backend, Frontend, Plugins, FileSystem)
  - Data flow (script → parsing → TTS → timeline → playback)
  - Plugin system design
- [ ] T113 Create docs/API.md:
  - All endpoint documentation (method, path, request, response)
  - Example requests/responses for each endpoint
  - Error codes and meanings
- [ ] T114 Create docs/DEVELOPMENT.md:
  - Dev environment setup (conda, uv, pnpm, TTS endpoint)
  - Running tests (pytest, Vitest)
  - Code style conventions (from SD-WebUI-Forge: 4-space, snake_case, PascalCase)
  - Debugging tips
- [ ] T115 Create docs/PLUGIN_GUIDE.md:
  - How to write custom TTS plugin
  - How to write custom exporter plugin
  - Plugin lifecycle and hooks (pre_parse, post_parse, pre_tts, post_tts, pre_export, post_export)

### 8.5 Code Quality

- [ ] T116 [P] Set up Ruff for Python linting:
  - Create backend/pyproject.toml with Ruff config
  - Fix all lint errors in backend/src/
  - Run in CI (GitHub Actions)
- [ ] T117 [P] Set up ESLint for frontend linting:
  - Create frontend/.eslintrc.js with alloy + prettier config
  - Fix all lint errors in frontend/src/
  - Run in CI
- [ ] T118 Add type checking:
  - Ensure all Python functions have type hints (Pydantic models, return types)
  - Ensure all TypeScript is strict mode (tsconfig.json)
  - Run mypy or pyright for Python static analysis
- [ ] T119 Code review checklist:
  - All functions documented (docstrings)
  - No hardcoded values (use config.py / .env)
  - No console.log or print statements (use logger)
  - No TODO comments without issue reference

### 8.6 Performance Optimization

- [ ] T120 Optimize script parsing:
  - Cache parsed scenes by script hash (already implemented in ScriptParser)
  - Only reparse if script.txt changed (compare hash)
- [ ] T121 Optimize TTS generation:
  - Queue TTS requests (asyncio.Queue) with parallel processing (5 concurrent)
  - Don't regenerate audio for unchanged lines
- [ ] T122 Optimize UI rendering:
  - Virtualize timeline table if >100 rows (render only visible rows)
  - Lazy-load background images in ScenePreview
  - Debounce timeline edits to 1 second
- [ ] T123 Optimize bundle size:
  - Tree-shake unused PixiJS features
  - Minify CSS/JS in production build
  - Target: frontend bundle <500 KB gzipped

### 8.7 Deployment & Setup

- [ ] T124 Create docker-compose.yml (optional for MVP):
  - FastAPI backend service
  - TTS service (GPT-SoVITS or VITS) - optional
- [ ] T125 Create quickstart.md:
  - Step-by-step setup: conda, uv, pnpm, .env config
  - Running backend: python backend/src/main.py
  - Running frontend: pnpm dev
  - Opening project folder workflow
  - First-run troubleshooting (TTS endpoint unreachable, etc.)
- [ ] T126 Create GitHub Actions CI workflow:
  - Run pytest with coverage report
  - Run Vitest
  - Run Ruff and ESLint
  - Report coverage (target 80%+)

---

## Dependencies & Sequencing

### Critical Path for MVP (User Stories 1 + 2)

```
Phase 1 (Setup)
  ↓
Phase 2 (Foundational)
  ├── Data Models (T016-T019)
  ├── LLM Parser (T020-T024)
  ├── File Manager (T025-T027)
  └── API Routes (T030-T031)
  ↓
Phase 3 (User Story 1: Load Project)
  ├── Backend: T035-T039
  ├── Frontend: T040-T043
  └── Tests: T044-T048
  ↓
Phase 4 (User Story 2: Auto-Parse & TTS)
  ├── Backend: T049-T057
  ├── Frontend: T058-T061
  └── Tests: T062-T068
```

### Full Path (All 5 User Stories)

```
[MVP Critical Path above]
  ↓
Phase 5 (User Story 3: Edit Interface)
  ├── Backend: T069-T070
  ├── Frontend: T071-T075
  └── Tests: T076-T080
  ↓
Phase 6 (User Story 4: Playback)
  ├── Backend: T081
  ├── Frontend (PixiJS): T082-T088
  └── Tests: T089-T093
  ↓
Phase 7 (User Story 5: Export)
  ├── Backend: T094-T096
  ├── Frontend: T097-T098
  └── Tests: T099-T102
  ↓
Phase 8 (Polish)
  ├── Error Handling (T103-T105)
  ├── Logging (T106-T108)
  ├── Testing Coverage (T109-T111)
  ├── Documentation (T112-T115)
  ├── Code Quality (T116-T119)
  ├── Performance (T120-T123)
  └── Deployment (T124-T126)
```

### Parallel Opportunities per User Story

**Phase 3 (User Story 1 Parallelization)**:
- T035-T036 (Backend project loading)
- T040-T041 (Frontend components)
- T044-T048 (Tests)
- Can work in parallel: Backend and Frontend teams independently

**Phase 4 (User Story 2 Parallelization)**:
- T049-T051 (Backend parsing) — blocks T052-T054 (TTS)
- T058-T059 (Frontend UI) — can start once API routes defined (T055)
- T062-T068 (Tests) — can run in parallel with implementation

**Phase 5-6 Parallelization**:
- User Story 3 and 4 are independent — two teams can work in parallel
- User Story 3 backend (T069-T070) blocks User Story 3 frontend (T071-T075)
- User Story 4 backend (T081) blocks User Story 4 frontend (T082-T088)

---

## Success Metrics

### For User Story 1 (Load Project)
- ✅ Project folder loaded in <2 seconds
- ✅ Project state persisted in project.json
- ✅ Session restored after app restart
- ✅ 100% test coverage for ProjectManager

### For User Story 2 (Auto-Parse & TTS)
- ✅ 3-scene script parsed in <5 minutes (including TTS)
- ✅ All dialogue lines assigned character, emotion, action
- ✅ TTS audio generated for all lines
- ✅ Cost tracked and displayed (Deepseek: <$0.01 for typical script)
- ✅ Parse result cached (2nd parse of same script <1 second)

### For User Story 3 (Edit Interface)
- ✅ Edit row + regenerate audio in <30 seconds
- ✅ Undo/redo works for all edits
- ✅ 80% test coverage for editing logic

### For User Story 4 (Playback)
- ✅ Playback load <3 seconds
- ✅ Audio/sprite sync <200ms
- ✅ Animations smooth (60 FPS)

### For User Story 5 (Export)
- ✅ Export to JSON <1 second
- ✅ Re-import without data loss
- ✅ Export to Ren'Py format functional

### Overall
- ✅ 80% statement coverage across all modules
- ✅ All acceptance scenarios in spec.md passing
- ✅ No lint errors (Ruff + ESLint)
- ✅ All tasks completed with documented code

---

## Notes for Implementation

- **LLM Default**: Use Deepseek (tested in LingChat) with Qwen/GLM/Regex fallback
- **TTS Default**: GPT-SoVITS at http://127.0.0.1:9872, fallback to VITS
- **File Format**: JSON for project state (human-readable, editable)
- **Backup Policy**: .orig (pristine), .bak1 (previous), .bak2 (oldest) — no file deletion
- **Logging**: Minimalist ACTION_LOG.md format only
- **Error Handling**: User-friendly messages, never expose internal errors
- **Performance Targets**: Per spec.md success criteria (SC-001 through SC-010)
- **Testing**: Red-Green-Refactor per Constitution Principle II (Test-First)
- **Code Style**: From SD-WebUI-Forge (4-space indent, snake_case functions, PascalCase classes)

---

**Next Steps**: Begin with Phase 1 setup tasks (T001-T015) in parallel. Once foundational services ready (Phase 2: T016-T043), start Phase 3 and 4 independently or in parallel by team.

**Estimated Effort**:
- MVP (Stories 1+2 + tests): ~3-4 weeks (2-3 developers)
- Full 5 stories: ~6-8 weeks (2-3 developers)
- Polish + deployment: ~1-2 weeks

