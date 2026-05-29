# Script to add API control tools to mcp_ableton_server.py

# Read the file
with open('mcp_ableton_server.py', 'r') as f:
    content = f.read()

# Find the insertion point (after VIEW CONTROL TOOLS section, before APPLICATION CONTROL TOOLS)
# We'll add it after the last view tool and before the APPLICATION comment
insertion_marker = "# ============= APPLICATION CONTROL TOOLS ============="
insertion_point = content.find(insertion_marker)

# API control tools to add
api_tools = '''
# ============= API CONTROL TOOLS =============

@mcp.tool()
async def get_api_version() -> str:
    """Get the OSC API version."""
    params = {"address": "/live/api/get/version", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return str(result['data'][0]) if result['data'] else ""
        return str(result.get('status', ''))
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_api_info() -> str:
    """Get API information."""
    params = {"address": "/live/api/get/info", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            info_parts = [str(d) for d in result['data']] if result['data'] else []
            return ", ".join(info_parts) if info_parts else ""
        return str(result.get('status', ''))
    return f"Error: {response.get('message', 'Unknown error')}"


'''

# Insert the new tools before the marker
new_content = content[:insertion_point] + api_tools + content[insertion_point:]

# Write back
with open('mcp_ableton_server.py', 'w') as f:
    f.write(new_content)

print("API control tools added successfully!")
print("Added 2 tools:")
print("  - get_api_version")
print("  - get_api_info")
