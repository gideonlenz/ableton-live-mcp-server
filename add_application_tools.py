# Script to add application control tools to mcp_ableton_server.py

# Read the file
with open('mcp_ableton_server.py', 'r') as f:
    content = f.read()

# Find the insertion point (before # ----- TOOLS WITH RESPONSE -----)
insertion_marker = "# ----- TOOLS WITH RESPONSE -----"
insertion_point = content.find(insertion_marker)

# Application control tools to add
application_tools = '''
# ============= APPLICATION CONTROL TOOLS =============

@mcp.tool()
async def get_application_version() -> str:
    """Get the version of Ableton Live."""
    params = {"address": "/live/application/get/version", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return str(result['data'][0]) if result['data'] else ""
        return str(result.get('status', ''))
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_application_author() -> str:
    """Get the author information of Ableton Live."""
    params = {"address": "/live/application/get/author", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return str(result['data'][0]) if result['data'] else ""
        return str(result.get('status', ''))
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_application_name() -> str:
    """Get the name of the application."""
    params = {"address": "/live/application/get/name", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return str(result['data'][0]) if result['data'] else ""
        return str(result.get('status', ''))
    return f"Error: {response.get('message', 'Unknown error')}"


'''

# Insert the new tools before the marker
new_content = content[:insertion_point] + application_tools + content[insertion_point:]

# Write back
with open('mcp_ableton_server.py', 'w') as f:
    f.write(new_content)

print("Application control tools added successfully!")
