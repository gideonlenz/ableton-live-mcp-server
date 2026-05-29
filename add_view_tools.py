# Script to add view control tools to mcp_ableton_server.py

# Read the file
with open('mcp_ableton_server.py', 'r') as f:
    content = f.read()

# Find the insertion point (before # ----- TOOLS WITH RESPONSE -----)
insertion_marker = "# ----- TOOLS WITH RESPONSE -----"
insertion_point = content.find(insertion_marker)

# View control tools to add
view_tools = '''
# ============= VIEW CONTROL TOOLS =============

@mcp.tool()
async def get_selected_track() -> int:
    """Get the index of the currently selected track."""
    params = {"address": "/live/view/get/selected_track", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return int(result['data'][0]) if result['data'] else 0
        return int(result.get('status', 0))
    raise ValueError(f"Error getting selected track: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_selected_track(track_index: int) -> str:
    """Set the currently selected track."""
    params = {"address": "/live/view/set/selected_track", "args": [int(track_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Selected track set to {track_index}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_selected_scene() -> int:
    """Get the index of the currently selected scene."""
    params = {"address": "/live/view/get/selected_scene", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return int(result['data'][0]) if result['data'] else 0
        return int(result.get('status', 0))
    raise ValueError(f"Error getting selected scene: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_selected_scene(scene_index: int) -> str:
    """Set the currently selected scene."""
    params = {"address": "/live/view/set/selected_scene", "args": [int(scene_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Selected scene set to {scene_index}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def focus_view() -> str:
    """Focus the Live view (bring Ableton window to front)."""
    params = {"address": "/live/view/focus/view", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return "Live view focused"
    return f"Error: {response.get('message', 'Unknown error')}"


'''

# Insert the new tools before the marker
new_content = content[:insertion_point] + view_tools + content[insertion_point:]

# Write back
with open('mcp_ableton_server.py', 'w') as f:
    f.write(new_content)

print("View control tools added successfully!")
