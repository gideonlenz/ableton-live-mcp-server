# Script to add track creation tools to mcp_ableton_server.py

with open('mcp_ableton_server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Insert point: find set_song_loop function and insert after its block
marker = "async def set_song_loop(enabled: bool) -> str:"
marker_index = content.find(marker)

if marker_index == -1:
    print("Error: Could not find set_song_loop in mcp_ableton_server.py")
    exit(1)

# Find the end of the set_song_loop function (next blank line or next @mcp.tool())
next_block_index = content.find("@mcp.tool()", marker_index + len(marker))

if next_block_index == -1:
    print("Error: Could not find next @mcp.tool()")
    exit(1)

track_tools = '''@mcp.tool()
async def create_midi_track(track_index: int = -1) -> str:
    """Create a new MIDI track in Ableton Live at the specified index.
    
    Args:
        track_index: 0-based index to insert the track at (-1 to append at the end)
    """
    params = {"address": "/live/song/create_midi_track", "args": [int(track_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"MIDI track created at index {track_index}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def create_audio_track(track_index: int = -1) -> str:
    """Create a new audio track in Ableton Live at the specified index.
    
    Args:
        track_index: 0-based index to insert the track at (-1 to append at the end)
    """
    params = {"address": "/live/song/create_audio_track", "args": [int(track_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Audio track created at index {track_index}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def delete_track(track_index: int) -> str:
    """Delete a track at the specified index from the song.
    
    Args:
        track_index: 0-based track index to delete
    """
    params = {"address": "/live/song/delete_track", "args": [int(track_index)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Track at index {track_index} deleted"
    return f"Error: {response.get('message', 'Unknown error')}"


'''

new_content = content[:next_block_index] + track_tools + content[next_block_index:]

with open('mcp_ableton_server.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Track creation tools added successfully!")
