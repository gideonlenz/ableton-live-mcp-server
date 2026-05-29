# Ableton Live MCP - Clip API & CRUD Extension Progress

This document tracks the progress of the Clip API completion and CRUD extension for the Ableton Live MCP server.

**Location**: `C:\mcp\ableton\ableton-live-mcp-server`
**Last Updated**: 2026-05-27

---

## 📊 Summary of CRUD & Clip Endpoints

| Category | Endpoint / Operation | Status | Type | Notes |
|---|---|---|---|---|
| **Clip Slot (CRUD)** | `/live/clip_slot/create_clip` | ✅ Complete | Create | Creates empty MIDI clip in slot |
| **Clip Slot (CRUD)** | `/live/clip_slot/delete_clip` | ✅ Complete | Delete | Deletes clip from slot |
| **Clip Slot (CRUD)** | `/live/clip_slot/duplicate_clip_to` | ✅ Complete | Create/Update | Duplicates clip to another slot |
| **Clip Notes (MIDI)** | `/live/clip/get/notes` | ✅ Complete | Read | Queries notes in clip |
| **Clip Notes (MIDI)** | `/live/clip/add/notes` | ✅ Complete | Create/Update | Adds new MIDI notes to clip |
| **Clip Notes (MIDI)** | `/live/clip/remove/notes` | ✅ Complete | Delete | Removes notes in range |
| **Clip Properties** | `/live/clip/get/color` | ✅ Complete | Read | Refactored from curly-brace |
| **Clip Properties** | `/live/clip/set/color` | ✅ Complete | Update | Refactored from curly-brace |
| **Clip Properties** | `/live/clip/get/color_index` | ✅ Complete | Read | Get color index (0-69) |
| **Clip Properties** | `/live/clip/set/color_index` | ✅ Complete | Update | Set color index (0-69) |
| **Clip Properties** | `/live/clip/get/name` | ✅ Complete | Read | Refactored from curly-brace |
| **Clip Properties** | `/live/clip/set/name` | ✅ Complete | Update | Refactored from curly-brace |
| **Clip Properties** | `/live/clip/get/gain` | ✅ Complete | Read | Get clip gain |
| **Clip Properties** | `/live/clip/set/gain` | ✅ Complete | Update | Set clip gain |
| **Clip Properties** | `/live/clip/get/length` | ✅ Complete | Read | Refactored from curly-brace |
| **Clip Properties** | `/live/clip/get/sample_length` | ✅ Complete | Read | Get clip sample length |
| **Clip Properties** | `/live/clip/get/start_time` | ✅ Complete | Read | Get clip start time |
| **Clip Properties** | `/live/clip/get/pitch_coarse` | ✅ Complete | Read | Get coarse pitch semitones |
| **Clip Properties** | `/live/clip/set/pitch_coarse` | ✅ Complete | Update | Set coarse pitch semitones |
| **Clip Properties** | `/live/clip/get/pitch_fine` | ✅ Complete | Read | Get fine pitch cents |
| **Clip Properties** | `/live/clip/set/pitch_fine` | ✅ Complete | Update | Set fine pitch cents |
| **Clip Properties** | `/live/clip/get/file_path` | ✅ Complete | Read | Get audio file path |
| **Clip Properties** | `/live/clip/get/is_audio_clip` | ✅ Complete | Read | Query if clip is audio |
| **Clip Properties** | `/live/clip/get/is_midi_clip` | ✅ Complete | Read | Query if clip is MIDI |
| **Clip Properties** | `/live/clip/get/is_playing` | ✅ Complete | Read | Query if clip is playing |
| **Clip Properties** | `/live/clip/get/is_overdubbing` | ✅ Complete | Read | Query if clip is overdubbing |
| **Clip Properties** | `/live/clip/get/is_recording` | ✅ Complete | Read | Query if clip is recording |
| **Clip Properties** | `/live/clip/get/will_record_on_start` | ✅ Complete | Read | Query if clip will record on start |
| **Clip Properties** | `/live/clip/get/playing_position` | ✅ Complete | Read | Get current playing position |
| **Clip Properties** | `/live/clip/start_listen/playing_position` | ✅ Complete | Read/Listen | Start playing position observer |
| **Clip Properties** | `/live/clip/stop_listen/playing_position` | ✅ Complete | Read/Listen | Stop playing position observer |
| **Clip Properties** | `/live/clip/get/loop_start` | ✅ Complete | Read | Get loop start beat |
| **Clip Properties** | `/live/clip/set/loop_start` | ✅ Complete | Update | Set loop start beat |
| **Clip Properties** | `/live/clip/get/loop_end` | ✅ Complete | Read | Get loop end beat |
| **Clip Properties** | `/live/clip/set/loop_end` | ✅ Complete | Update | Set loop end beat |
| **Clip Properties** | `/live/clip/get/looping` | ✅ Complete | Read | Refactored from curly-brace |
| **Clip Properties** | `/live/clip/set/looping` | ✅ Complete | Update | Refactored from curly-brace |
| **Clip Properties** | `/live/clip/get/warping` | ✅ Complete | Read | Get if warping is enabled |
| **Clip Properties** | `/live/clip/set/warping` | ✅ Complete | Update | Set if warping is enabled |
| **Clip Properties** | `/live/clip/get/launch_mode` | ✅ Complete | Read | Get launch mode (0-3) |
| **Clip Properties** | `/live/clip/set/launch_mode` | ✅ Complete | Update | Set launch mode (0-3) |
| **Clip Properties** | `/live/clip/get/launch_quantization` | ✅ Complete | Read | Get launch quantization (0-14) |
| **Clip Properties** | `/live/clip/set/launch_quantization` | ✅ Complete | Update | Set launch quantization (0-14) |
| **Clip Properties** | `/live/clip/get/ram_mode` | ✅ Complete | Read | Get RAM mode (0-1) |
| **Clip Properties** | `/live/clip/set/ram_mode` | ✅ Complete | Update | Set RAM mode (0-1) |
| **Clip Properties** | `/live/clip/get/warp_mode` | ✅ Complete | Read | Get warp mode (0-6) |
| **Clip Properties** | `/live/clip/set/warp_mode` | ✅ Complete | Update | Set warp mode (0-6) |
| **Clip Properties** | `/live/clip/get/has_groove` | ✅ Complete | Read | Get if clip has groove |
| **Clip Properties** | `/live/clip/get/legato` | ✅ Complete | Read | Get legato state (0-1) |
| **Clip Properties** | `/live/clip/set/legato` | ✅ Complete | Update | Set legato state (0-1) |
| **Clip Properties** | `/live/clip/get/position` | ✅ Complete | Read | Get current position |
| **Clip Properties** | `/live/clip/set/position` | ✅ Complete | Update | Set current position |
| **Clip Properties** | `/live/clip/get/muted` | ✅ Complete | Read | Get muted state (0-1) |
| **Clip Properties** | `/live/clip/set/muted` | ✅ Complete | Update | Set muted state (0-1) |
| **Clip Properties** | `/live/clip/get/velocity_amount` | ✅ Complete | Read | Get velocity amount (0.0-1.0) |
| **Clip Properties** | `/live/clip/set/velocity_amount` | ✅ Complete | Update | Set velocity amount (0.0-1.0) |
| **Clip Properties** | `/live/clip/get/start_marker` | ✅ Complete | Read | Get start marker beat |
| **Clip Properties** | `/live/clip/set/start_marker` | ✅ Complete | Update | Set start marker beat |
| **Clip Properties** | `/live/clip/get/end_marker` | ✅ Complete | Read | Get end marker beat |
| **Clip Properties** | `/live/clip/set/end_marker` | ✅ Complete | Update | Set end marker beat |
| **Clip Actions** | `/live/clip/fire` | ✅ Complete | Action/Execute | Refactored from curly-brace `/launch` |
| **Clip Actions** | `/live/clip/stop` | ✅ Complete | Action/Execute | Refactored from curly-brace |
| **Clip Actions** | `/live/clip/duplicate_loop` | ✅ Complete | Create/Update | Duplicates clip loop |

---

## 📈 Status Checklists

- [x] Complete Clip Slot CRUD operations (Create/Delete/Duplicate)
- [x] Complete Clip MIDI Notes CRUD operations (Read/Create/Delete)
- [x] Complete Clip Properties operations (Read/Update)
- [x] Complete Clip Actions operations (Execute)
- [x] Refactor and fix all existing broken clip tools
