# Script to add complete Clip API and Clip Slot CRUD extensions to mcp_ableton_server.py
# Correcting broken REST-like paths to standard AbletonOSC paths.

import re

# Read current server content
with open('mcp_ableton_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. We will find the start of CLIP CONTROL TOOLS and end of it.
# Start marker
start_marker = "# ============= CLIP CONTROL TOOLS ============="
# The next section starts with # ============= CLIP SLOT CONTROL TOOLS =============
end_marker = "# ============= CLIP SLOT CONTROL TOOLS ============="

start_index = content.find(start_marker)
end_index = content.find(end_marker)

if start_index == -1 or end_index == -1:
    print("Error: Could not find markers in mcp_ableton_server.py")
    exit(1)

# Complete refactored & new clip tools block
new_clip_tools = '''# ============= CLIP CONTROL TOOLS =============

# --- Core Clip Actions ---

@mcp.tool()
async def clip_launch(track_index: int, clip_index: int) -> str:
    """Launch (fire) a specific clip.
    
    Args:
        track_index: 0-based track index
        clip_index: 0-based clip slot index
    """
    params = {"address": "/live/clip/fire", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} launched"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def clip_stop(track_index: int, clip_index: int) -> str:
    """Stop a specific clip.
    
    Args:
        track_index: 0-based track index
        clip_index: 0-based clip slot index
    """
    params = {"address": "/live/clip/stop", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} stopped"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def duplicate_loop(track_index: int, clip_index: int) -> str:
    """Duplicates the clip's loop.
    
    Args:
        track_index: 0-based track index
        clip_index: 0-based clip slot index
    """
    params = {"address": "/live/clip/duplicate_loop", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} loop duplicated"
    return f"Error: {response.get('message', 'Unknown error')}"


# --- Clip Notes (MIDI) CRUD Operations ---

@mcp.tool()
async def get_clip_notes(track_index: int, clip_index: int, 
                     pitch_start: Optional[int] = None, pitch_span: Optional[int] = None, 
                     time_start: Optional[float] = None, time_span: Optional[float] = None) -> str:
    """Query the MIDI notes inside a clip.
    
    Returns a JSON string list of note dictionaries containing pitch, start_time, duration, velocity, mute.
    """
    args = [int(track_index), int(clip_index)]
    if all(v is not None for v in [pitch_start, pitch_span, time_start, time_span]):
        args.extend([int(pitch_start), int(pitch_span), float(time_start), float(time_span)])
        
    params = {"address": "/live/clip/get/notes", "args": args}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            raw_notes = result['data'][2:] # First 2 elements are track_index, clip_index
            notes = []
            for i in range(0, len(raw_notes), 5):
                if i + 4 < len(raw_notes):
                    notes.append({
                        "pitch": int(raw_notes[i]),
                        "start_time": float(raw_notes[i+1]),
                        "duration": float(raw_notes[i+2]),
                        "velocity": int(raw_notes[i+3]),
                        "mute": bool(raw_notes[i+4])
                    })
            import json
            return json.dumps(notes, indent=2)
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def add_clip_notes(track_index: int, clip_index: int, notes_json: str) -> str:
    """Add new MIDI notes to a clip.
    
    Args:
        notes_json: A JSON string list of note objects, e.g.
                    '[{"pitch": 60, "start_time": 0.0, "duration": 1.0, "velocity": 100, "mute": false}]'
    """
    import json
    try:
        notes_list = json.loads(notes_json)
    except Exception as e:
        return f"Error: Invalid JSON format: {e}"
        
    flat_args = []
    for note in notes_list:
        flat_args.extend([
            int(note.get("pitch", 60)),
            float(note.get("start_time", 0.0)),
            float(note.get("duration", 1.0)),
            int(note.get("velocity", 100)),
            int(note.get("mute", 0))
        ])
        
    params = {
        "address": "/live/clip/add/notes",
        "args": [int(track_index), int(clip_index)] + flat_args
    }
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Added {len(notes_list)} MIDI notes to clip {clip_index} on track {track_index}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def remove_clip_notes(track_index: int, clip_index: int, 
                        pitch_start: Optional[int] = None, pitch_span: Optional[int] = None, 
                        time_start: Optional[float] = None, time_span: Optional[float] = None) -> str:
    """Remove MIDI notes from a clip in a range of pitches and times.
    If no ranges specified, all notes are removed.
    """
    args = [int(track_index), int(clip_index)]
    if all(v is not None for v in [pitch_start, pitch_span, time_start, time_span]):
        args.extend([int(pitch_start), int(pitch_span), float(time_start), float(time_span)])
        
    params = {"address": "/live/clip/remove/notes", "args": args}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Removed notes from clip {clip_index} on track {track_index}"
    return f"Error: {response.get('message', 'Unknown error')}"


# --- Clip Property Read/Write Endpoints ---

@mcp.tool()
async def get_clip_name(track_index: int, clip_index: int) -> str:
    """Get the name of a specific clip."""
    params = {"address": "/live/clip/get/name", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return str(result['data'][2])
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def set_clip_name(track_index: int, clip_index: int, name: str) -> str:
    """Set the name of a specific clip."""
    params = {"address": "/live/clip/set/name", "args": [int(track_index), int(clip_index), str(name)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} name set to '{name}'"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_color(track_index: int, clip_index: int) -> str:
    """Get the color of a specific clip as a hex string."""
    params = {"address": "/live/clip/get/color", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return str(result['data'][2])
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def set_clip_color(track_index: int, clip_index: int, color: str) -> str:
    """Set the color of a specific clip as a hex string."""
    params = {"address": "/live/clip/set/color", "args": [int(track_index), int(clip_index), str(color)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} color set to '{color}'"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_color_index(track_index: int, clip_index: int) -> int:
    """Get the color index of a specific clip (0-69)."""
    params = {"address": "/live/clip/get/color_index", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return int(result['data'][2])
    raise ValueError(f"Error getting clip color index: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_color_index(track_index: int, clip_index: int, color_index: int) -> str:
    """Set the color index of a specific clip (0-69)."""
    params = {"address": "/live/clip/set/color_index", "args": [int(track_index), int(clip_index), int(color_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} color index set to {color_index}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_gain(track_index: int, clip_index: int) -> float:
    """Get the gain of a specific clip."""
    params = {"address": "/live/clip/get/gain", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return float(result['data'][2])
    raise ValueError(f"Error getting clip gain: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_gain(track_index: int, clip_index: int, gain: float) -> str:
    """Set the gain of a specific clip."""
    params = {"address": "/live/clip/set/gain", "args": [int(track_index), int(clip_index), float(gain)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} gain set to {gain}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_length(track_index: int, clip_index: int) -> float:
    """Get the length of a specific clip in beats."""
    params = {"address": "/live/clip/get/length", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return float(result['data'][2])
    raise ValueError(f"Error getting clip length: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def get_clip_sample_length(track_index: int, clip_index: int) -> float:
    """Get the sample length of a specific audio clip in beats."""
    params = {"address": "/live/clip/get/sample_length", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return float(result['data'][2])
    raise ValueError(f"Error getting clip sample length: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def get_clip_start_time(track_index: int, clip_index: int) -> float:
    """Get the start time of a specific clip in beats."""
    params = {"address": "/live/clip/get/start_time", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return float(result['data'][2])
    raise ValueError(f"Error getting clip start time: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def get_clip_pitch_coarse(track_index: int, clip_index: int) -> int:
    """Get the coarse pitch re-pitch of a clip in semitones."""
    params = {"address": "/live/clip/get/pitch_coarse", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return int(result['data'][2])
    raise ValueError(f"Error getting clip pitch coarse: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_pitch_coarse(track_index: int, clip_index: int, semitones: int) -> str:
    """Set the coarse pitch re-pitch of a clip in semitones."""
    params = {"address": "/live/clip/set/pitch_coarse", "args": [int(track_index), int(clip_index), int(semitones)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} coarse pitch set to {semitones} semitones"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_pitch_fine(track_index: int, clip_index: int) -> int:
    """Get the fine pitch re-pitch of a clip in cents."""
    params = {"address": "/live/clip/get/pitch_fine", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return int(result['data'][2])
    raise ValueError(f"Error getting clip pitch fine: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_pitch_fine(track_index: int, clip_index: int, cents: int) -> str:
    """Set the fine pitch re-pitch of a clip in cents."""
    params = {"address": "/live/clip/set/pitch_fine", "args": [int(track_index), int(clip_index), int(cents)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} fine pitch set to {cents} cents"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_file_path(track_index: int, clip_index: int) -> str:
    """Get the file path of a specific audio clip."""
    params = {"address": "/live/clip/get/file_path", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return str(result['data'][2])
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_is_audio_clip(track_index: int, clip_index: int) -> bool:
    """Query whether a clip is an audio clip."""
    params = {"address": "/live/clip/get/is_audio_clip", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return bool(result['data'][2])
    raise ValueError(f"Error checking if clip is audio: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def get_clip_is_midi_clip(track_index: int, clip_index: int) -> bool:
    """Query whether a clip is a MIDI clip."""
    params = {"address": "/live/clip/get/is_midi_clip", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return bool(result['data'][2])
    raise ValueError(f"Error checking if clip is MIDI: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def get_clip_is_playing(track_index: int, clip_index: int) -> bool:
    """Query whether a clip is currently playing."""
    params = {"address": "/live/clip/get/is_playing", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return bool(result['data'][2])
    raise ValueError(f"Error checking if clip is playing: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def get_clip_playing(track_index: int, clip_index: int) -> bool:
    """Query whether a clip is currently playing (Legacy name alias)."""
    return await get_clip_is_playing(track_index, clip_index)


@mcp.tool()
async def get_clip_is_overdubbing(track_index: int, clip_index: int) -> bool:
    """Query whether a clip is currently overdubbing."""
    params = {"address": "/live/clip/get/is_overdubbing", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return bool(result['data'][2])
    raise ValueError(f"Error checking if clip is overdubbing: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def get_clip_is_recording(track_index: int, clip_index: int) -> bool:
    """Query whether a clip is currently recording."""
    params = {"address": "/live/clip/get/is_recording", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return bool(result['data'][2])
    raise ValueError(f"Error checking if clip is recording: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def get_clip_will_record_on_start(track_index: int, clip_index: int) -> bool:
    """Query whether a clip will record on start."""
    params = {"address": "/live/clip/get/will_record_on_start", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return bool(result['data'][2])
    raise ValueError(f"Error checking if clip will record on start: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def get_clip_playing_position(track_index: int, clip_index: int) -> float:
    """Get the current playing position of the clip in beats."""
    params = {"address": "/live/clip/get/playing_position", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return float(result['data'][2])
    raise ValueError(f"Error getting clip playing position: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def start_listen_clip_playing_position(track_index: int, clip_index: int) -> str:
    """Start listening for the clip's playing position updates."""
    params = {"address": "/live/clip/start_listen/playing_position", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Started listening to playing position updates for clip {clip_index} on track {track_index}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def stop_listen_clip_playing_position(track_index: int, clip_index: int) -> str:
    """Stop listening for the clip's playing position updates."""
    params = {"address": "/live/clip/stop_listen/playing_position", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Stopped listening to playing position updates for clip {clip_index} on track {track_index}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_loop_start(track_index: int, clip_index: int) -> float:
    """Get the loop start beat of a specific clip."""
    params = {"address": "/live/clip/get/loop_start", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return float(result['data'][2])
    raise ValueError(f"Error getting clip loop start: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_loop_start(track_index: int, clip_index: int, loop_start: float) -> str:
    """Set the loop start beat of a specific clip."""
    params = {"address": "/live/clip/set/loop_start", "args": [int(track_index), int(clip_index), float(loop_start)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} loop start set to {loop_start}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_loop_end(track_index: int, clip_index: int) -> float:
    """Get the loop end beat of a specific clip."""
    params = {"address": "/live/clip/get/loop_end", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return float(result['data'][2])
    raise ValueError(f"Error getting clip loop end: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_loop_end(track_index: int, clip_index: int, loop_end: float) -> str:
    """Set the loop end beat of a specific clip."""
    params = {"address": "/live/clip/set/loop_end", "args": [int(track_index), int(clip_index), float(loop_end)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} loop end set to {loop_end}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_looping(track_index: int, clip_index: int) -> bool:
    """Get whether a specific clip is looping."""
    params = {"address": "/live/clip/get/looping", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return bool(result['data'][2])
    raise ValueError(f"Error getting clip looping state: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_looping(track_index: int, clip_index: int, looping: bool) -> str:
    """Set whether a specific clip should loop."""
    params = {"address": "/live/clip/set/looping", "args": [int(track_index), int(clip_index), int(looping)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} looping {'enabled' if looping else 'disabled'}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_warping(track_index: int, clip_index: int) -> bool:
    """Get whether warping is enabled for a specific audio clip."""
    params = {"address": "/live/clip/get/warping", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return bool(result['data'][2])
    raise ValueError(f"Error getting clip warping state: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_warping(track_index: int, clip_index: int, warping: bool) -> str:
    """Set whether warping is enabled for a specific audio clip."""
    params = {"address": "/live/clip/set/warping", "args": [int(track_index), int(clip_index), int(warping)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} warping {'enabled' if warping else 'disabled'}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_launch_mode(track_index: int, clip_index: int) -> int:
    """Get the launch mode of a clip (0=Trigger, 1=Gate, 2=Toggle, 3=Repeat)."""
    params = {"address": "/live/clip/get/launch_mode", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return int(result['data'][2])
    raise ValueError(f"Error getting clip launch mode: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_launch_mode(track_index: int, clip_index: int, launch_mode: int) -> str:
    """Set the launch mode of a clip (0=Trigger, 1=Gate, 2=Toggle, 3=Repeat)."""
    params = {"address": "/live/clip/set/launch_mode", "args": [int(track_index), int(clip_index), int(launch_mode)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} launch mode set to {launch_mode}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_launch_quantization(track_index: int, clip_index: int) -> int:
    """Get launch Quantization Value (0=Global, 1=None, 2=8Bars, 3=4Bars, 4=2Bars, 5=1Bar, etc.)."""
    params = {"address": "/live/clip/get/launch_quantization", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return int(result['data'][2])
    raise ValueError(f"Error getting clip launch quantization: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_launch_quantization(track_index: int, clip_index: int, quantization: int) -> str:
    """Set launch Quantization Value (0=Global, 1=None, 2=8Bars, 3=4Bars, 4=2Bars, 5=1Bar, etc.)."""
    params = {"address": "/live/clip/set/launch_quantization", "args": [int(track_index), int(clip_index), int(quantization)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} launch quantization set to {quantization}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_ram_mode(track_index: int, clip_index: int) -> int:
    """Get RAM mode of clip (0=False, 1=True)."""
    params = {"address": "/live/clip/get/ram_mode", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return int(result['data'][2])
    raise ValueError(f"Error getting clip RAM mode: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_ram_mode(track_index: int, clip_index: int, ram_mode: int) -> str:
    """Set RAM mode of clip (0=False, 1=True)."""
    params = {"address": "/live/clip/set/ram_mode", "args": [int(track_index), int(clip_index), int(ram_mode)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} RAM mode set to {ram_mode}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_warp_mode(track_index: int, clip_index: int) -> int:
    """Get Warp Mode of audio clip (0=Beats, 1=Tones, 2=Texture, 3=Re-Pitch, 4=Complex, 6=Pro)."""
    params = {"address": "/live/clip/get/warp_mode", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return int(result['data'][2])
    raise ValueError(f"Error getting clip warp mode: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_warp_mode(track_index: int, clip_index: int, warp_mode: int) -> str:
    """Set Warp Mode of audio clip (0=Beats, 1=Tones, 2=Texture, 3=Re-Pitch, 4=Complex, 6=Pro)."""
    params = {"address": "/live/clip/set/warp_mode", "args": [int(track_index), int(clip_index), int(warp_mode)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} warp mode set to {warp_mode}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_has_groove(track_index: int, clip_index: int) -> bool:
    """Get whether a specific clip has a groove active."""
    params = {"address": "/live/clip/get/has_groove", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return bool(result['data'][2])
    raise ValueError(f"Error checking if clip has groove: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def get_clip_legato(track_index: int, clip_index: int) -> bool:
    """Get Legato state of a specific clip."""
    params = {"address": "/live/clip/get/legato", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return bool(result['data'][2])
    raise ValueError(f"Error getting clip legato state: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_legato(track_index: int, clip_index: int, legato: bool) -> str:
    """Set Legato state of a specific clip."""
    params = {"address": "/live/clip/set/legato", "args": [int(track_index), int(clip_index), int(legato)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} legato set to {legato}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_position(track_index: int, clip_index: int) -> float:
    """Get position of clip in beats (LoopStart)."""
    params = {"address": "/live/clip/get/position", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return float(result['data'][2])
    raise ValueError(f"Error getting clip position: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_position(track_index: int, clip_index: int, position: float) -> str:
    """Set position of clip in beats (LoopStart)."""
    params = {"address": "/live/clip/set/position", "args": [int(track_index), int(clip_index), float(position)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} position set to {position}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_muted(track_index: int, clip_index: int) -> bool:
    """Get muted state of clip."""
    params = {"address": "/live/clip/get/muted", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return bool(result['data'][2])
    raise ValueError(f"Error getting clip muted state: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_muted(track_index: int, clip_index: int, muted: bool) -> str:
    """Set muted state of clip."""
    params = {"address": "/live/clip/set/muted", "args": [int(track_index), int(clip_index), int(muted)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} muted state set to {muted}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_velocity_amount(track_index: int, clip_index: int) -> float:
    """Get velocity amount (0.0-1.0) of clip."""
    params = {"address": "/live/clip/get/velocity_amount", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return float(result['data'][2])
    raise ValueError(f"Error getting clip velocity amount: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_velocity_amount(track_index: int, clip_index: int, velocity_amount: float) -> str:
    """Set velocity amount (0.0-1.0) of clip."""
    params = {"address": "/live/clip/set/velocity_amount", "args": [int(track_index), int(clip_index), float(velocity_amount)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} velocity amount set to {velocity_amount}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_start_marker(track_index: int, clip_index: int) -> float:
    """Get start marker beat of clip."""
    params = {"address": "/live/clip/get/start_marker", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return float(result['data'][2])
    raise ValueError(f"Error getting clip start marker: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_start_marker(track_index: int, clip_index: int, start_marker: float) -> str:
    """Set start marker beat of clip."""
    params = {"address": "/live/clip/set/start_marker", "args": [int(track_index), int(clip_index), float(start_marker)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} start marker set to {start_marker}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_end_marker(track_index: int, clip_index: int) -> float:
    """Get end marker beat of clip."""
    params = {"address": "/live/clip/get/end_marker", "args": [int(track_index), int(clip_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return float(result['data'][2])
    raise ValueError(f"Error getting clip end marker: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_end_marker(track_index: int, clip_index: int, end_marker: float) -> str:
    """Set end marker beat of clip."""
    params = {"address": "/live/clip/set/end_marker", "args": [int(track_index), int(clip_index), float(end_marker)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} end marker set to {end_marker}"
    return f"Error: {response.get('message', 'Unknown error')}"
'''

# Replace the CLIP CONTROL TOOLS block
new_content = content[:start_index] + new_clip_tools + content[end_index:]

# 2. Now let's inject Clip Slot CRUD operations into CLIP SLOT CONTROL TOOLS section
# Clip Slot section starts with: # ============= CLIP SLOT CONTROL TOOLS =============
# Device section starts with: # ============= DEVICE CONTROL TOOLS =============
slot_start_marker = "# ============= CLIP SLOT CONTROL TOOLS ============="
device_start_marker = "# ============= DEVICE CONTROL TOOLS ============="

slot_start_index = new_content.find(slot_start_marker)
device_start_index = new_content.find(device_start_marker)

if slot_start_index == -1 or device_start_index == -1:
    print("Error: Could not find clip slot or device markers in content")
    exit(1)

# Refactored Clip Slot section with additional CRUD tools: create_clip, delete_clip, duplicate_clip_to
new_slot_tools = '''# ============= CLIP SLOT CONTROL TOOLS =============

# --- Clip Slot CRUD Operations ---

@mcp.tool()
async def create_clip(track_index: int, slot_index: int, length: float) -> str:
    """Create an empty MIDI clip of a specific length in beats in a clip slot.
    
    Args:
        track_index: 0-based track index
        slot_index: 0-based clip slot index
        length: Length in floating-point beats (e.g. 4.0 for a 1-bar loop)
    """
    params = {
        "address": "/live/clip_slot/create_clip",
        "args": [int(track_index), int(slot_index), float(length)]
    }
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Created MIDI clip of length {length} beats in slot {slot_index} on track {track_index}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def delete_clip(track_index: int, slot_index: int) -> str:
    """Delete the clip from a clip slot.
    
    Args:
        track_index: 0-based track index
        slot_index: 0-based clip slot index
    """
    params = {
        "address": "/live/clip_slot/delete_clip",
        "args": [int(track_index), int(slot_index)]
    }
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Deleted clip in slot {slot_index} on track {track_index}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def duplicate_clip_to(track_index: int, slot_index: int, target_track_index: int, target_slot_index: int) -> str:
    """Duplicate the clip in this slot to a target clip slot.
    
    Args:
        track_index: 0-based source track index
        slot_index: 0-based source clip slot index
        target_track_index: 0-based target track index
        target_slot_index: 0-based target clip slot index
    """
    params = {
        "address": "/live/clip_slot/duplicate_clip_to",
        "args": [int(track_index), int(slot_index), int(target_track_index), int(target_slot_index)]
    }
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Duplicated clip from track {track_index} slot {slot_index} to track {target_track_index} slot {target_slot_index}"
    return f"Error: {response.get('message', 'Unknown error')}"


# --- Clip Slot Property Read/Write Endpoints ---

@mcp.tool()
async def get_clip_slot_name(track_index: int, slot_index: int) -> str:
    """Get the name of a specific clip slot."""
    params = {"address": "/live/clip_slot/get/name", "args": [int(track_index), int(slot_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return str(result['data'][2])
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def set_clip_slot_name(track_index: int, slot_index: int, name: str) -> str:
    """Set the name of a specific clip slot."""
    params = {"address": "/live/clip_slot/set/name", "args": [int(track_index), int(slot_index), str(name)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip slot {slot_index} on track {track_index} name set to '{name}'"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_slot_color(track_index: int, slot_index: int) -> str:
    """Get the color of a specific clip slot as hex string."""
    params = {"address": "/live/clip_slot/get/color", "args": [int(track_index), int(slot_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return str(result['data'][2])
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def set_clip_slot_color(track_index: int, slot_index: int, color: str) -> str:
    """Set the color of a specific clip slot as hex string."""
    params = {"address": "/live/clip_slot/set/color", "args": [int(track_index), int(slot_index), str(color)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip slot {slot_index} on track {track_index} color set to '{color}'"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_slot_has_clip(track_index: int, slot_index: int) -> bool:
    """Get whether a clip slot contains a clip."""
    params = {"address": "/live/clip_slot/get/has_clip", "args": [int(track_index), int(slot_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return bool(result['data'][2])
    raise ValueError(f"Error getting clip slot has_clip: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def get_clip_slot_state(track_index: int, slot_index: int) -> str:
    """Get the state of a specific clip slot."""
    params = {"address": "/live/clip_slot/get/state", "args": [int(track_index), int(slot_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result and len(result['data']) > 2:
            return str(result['data'][2])
    return f"Error: {response.get('message', 'Unknown error')}"
'''

final_content = new_content[:slot_start_index] + new_slot_tools + new_content[device_start_index:]

# Write back
with open('mcp_ableton_server.py', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("mcp_ableton_server.py updated successfully!")
