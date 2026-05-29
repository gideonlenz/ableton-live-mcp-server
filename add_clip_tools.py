# Script to add clip control tools to mcp_ableton_server.py

# Read the file
with open('mcp_ableton_server.py', 'r') as f:
    content = f.read()

# Find the insertion point (after SCENE CONTROL TOOLS section, before # ----- TOOLS WITH RESPONSE -----)
# We'll add it after the last scene tool and before the comment
insertion_marker = "# ----- TOOLS WITH RESPONSE -----"
insertion_point = content.find(insertion_marker)

# Clip control tools to add
clip_tools = '''
# ============= CLIP CONTROL TOOLS =============

@mcp.tool()
async def clip_launch(track_index: int, clip_index: int) -> str:
    """Launch a specific clip."""
    params = {"address": f"/live/clip/{track_index}/{clip_index}/launch", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} launched"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def clip_stop(track_index: int, clip_index: int) -> str:
    """Stop a specific clip."""
    params = {"address": f"/live/clip/{track_index}/{clip_index}/stop", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} stopped"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_name(track_index: int, clip_index: int) -> str:
    """Get the name of a specific clip."""
    params = {"address": f"/live/clip/{track_index}/{clip_index}/get/name", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return str(result['data'][0]) if result['data'] else ""
        return str(result.get('status', ''))
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def set_clip_name(track_index: int, clip_index: int, name: str) -> str:
    """Set the name of a specific clip."""
    params = {"address": f"/live/clip/{track_index}/{clip_index}/set/name", "args": [str(name)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} name set to '{name}'"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_color(track_index: int, clip_index: int) -> str:
    """Get the color of a specific clip as hex string."""
    params = {"address": f"/live/clip/{track_index}/{clip_index}/get/color", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return str(result['data'][0]) if result['data'] else ""
        return str(result.get('status', ''))
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def set_clip_color(track_index: int, clip_index: int, color: str) -> str:
    """Set the color of a specific clip as hex string."""
    params = {"address": f"/live/clip/{track_index}/{clip_index}/set/color", "args": [str(color)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} color set to '{color}'"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_looping(track_index: int, clip_index: int) -> bool:
    """Get whether a clip is looping."""
    params = {"address": f"/live/clip/{track_index}/{clip_index}/get/looping", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return bool(result['data'][0]) if result['data'] else False
        return bool(result.get('status', False))
    raise ValueError(f"Error getting clip looping: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_clip_looping(track_index: int, clip_index: int, looping: bool) -> str:
    """Set whether a clip should loop."""
    params = {"address": f"/live/clip/{track_index}/{clip_index}/set/looping", "args": [int(looping)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip {clip_index} on track {track_index} looping {'enabled' if looping else 'disabled'}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_playing(track_index: int, clip_index: int) -> bool:
    """Get whether a clip is currently playing."""
    params = {"address": f"/live/clip/{track_index}/{clip_index}/get/playing", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return bool(result['data'][0]) if result['data'] else False
        return bool(result.get('status', False))
    raise ValueError(f"Error getting clip playing: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def get_clip_length(track_index: int, clip_index: int) -> float:
    """Get the length of a clip in beats."""
    params = {"address": f"/live/clip/{track_index}/{clip_index}/get/length", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return float(result['data'][0]) if result['data'] else 0.0
        return float(result.get('status', 0))
    raise ValueError(f"Error getting clip length: {response.get('message', 'Unknown error')}")


'''

# Insert the new tools before the marker
new_content = content[:insertion_point] + clip_tools + content[insertion_point:]

# Write back
with open('mcp_ableton_server.py', 'w') as f:
    f.write(new_content)

print("Clip control tools added successfully!")
