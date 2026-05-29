# Script to add clip slot control tools to mcp_ableton_server.py

# Read the file
with open('mcp_ableton_server.py', 'r') as f:
    content = f.read()

# Find the insertion point (after CLIP CONTROL TOOLS section, before DEVICE CONTROL TOOLS)
# We'll add it after the last clip tool (get_clip_length) and before the DEVICE comment
insertion_marker = "# ============= DEVICE CONTROL TOOLS ============="
insertion_point = content.find(insertion_marker)

# Clip slot control tools to add
clip_slot_tools = '''
# ============= CLIP SLOT CONTROL TOOLS =============

@mcp.tool()
async def get_clip_slot_name(track_index: int, slot_index: int) -> str:
    """Get the name of a specific clip slot."""
    params = {"address": f"/live/clip_slot/{track_index}/{slot_index}/get/name", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return str(result['data'][0]) if result['data'] else ""
        return str(result.get('status', ''))
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def set_clip_slot_name(track_index: int, slot_index: int, name: str) -> str:
    """Set the name of a specific clip slot."""
    params = {"address": f"/live/clip_slot/{track_index}/{slot_index}/set/name", "args": [str(name)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip slot {slot_index} on track {track_index} name set to '{name}'"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_slot_color(track_index: int, slot_index: int) -> str:
    """Get the color of a specific clip slot as hex string."""
    params = {"address": f"/live/clip_slot/{track_index}/{slot_index}/get/color", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return str(result['data'][0]) if result['data'] else ""
        return str(result.get('status', ''))
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def set_clip_slot_color(track_index: int, slot_index: int, color: str) -> str:
    """Set the color of a specific clip slot as hex string."""
    params = {"address": f"/live/clip_slot/{track_index}/{slot_index}/set/color", "args": [str(color)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Clip slot {slot_index} on track {track_index} color set to '{color}'"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_clip_slot_has_clip(track_index: int, slot_index: int) -> bool:
    """Get whether a clip slot contains a clip."""
    params = {"address": f"/live/clip_slot/{track_index}/{slot_index}/get/has_clip", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return bool(result['data'][0]) if result['data'] else False
        return bool(result.get('status', False))
    raise ValueError(f"Error getting clip slot has_clip: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def get_clip_slot_state(track_index: int, slot_index: int) -> str:
    """Get the state of a specific clip slot."""
    params = {"address": f"/live/clip_slot/{track_index}/{slot_index}/get/state", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return str(result['data'][0]) if result['data'] else ""
        return str(result.get('status', ''))
    return f"Error: {response.get('message', 'Unknown error')}"


'''

# Insert the new tools before the marker
new_content = content[:insertion_point] + clip_slot_tools + content[insertion_point:]

# Write back
with open('mcp_ableton_server.py', 'w') as f:
    f.write(new_content)

print("Clip slot control tools added successfully!")
print("Added 6 tools:")
print("  - get_clip_slot_name")
print("  - set_clip_slot_name")
print("  - get_clip_slot_color")
print("  - set_clip_slot_color")
print("  - get_clip_slot_has_clip")
print("  - get_clip_slot_state")
