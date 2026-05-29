# Script to add test/debug tools to mcp_ableton_server.py

# Read the file
with open('mcp_ableton_server.py', 'r') as f:
    content = f.read()

# Find the insertion point (after VIEW CONTROL TOOLS section, before APPLICATION CONTROL TOOLS)
# Actually, let's add it after API CONTROL TOOLS and before APPLICATION
insertion_marker = "# ============= APPLICATION CONTROL TOOLS ============="
insertion_point = content.find(insertion_marker)

# Test/Debug control tools to add
test_tools = '''
# ============= TEST & DEBUG TOOLS =============

@mcp.tool()
async def test_connection() -> str:
    """Test the OSC connection to Ableton Live."""
    params = {"address": "/live/test", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return "OSC connection test successful"
    return f"Connection test failed: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def trigger_error(message: str) -> str:
    """Trigger an error message for debugging purposes."""
    params = {"address": "/live/error", "args": [str(message)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Error triggered: {message}"
    return f"Error: {response.get('message', 'Unknown error')}"


'''

# Insert the new tools before the marker
new_content = content[:insertion_point] + test_tools + content[insertion_point:]

# Write back
with open('mcp_ableton_server.py', 'w') as f:
    f.write(new_content)

print("Test/debug tools added successfully!")
print("Added 2 tools:")
print("  - test_connection")
print("  - trigger_error")
