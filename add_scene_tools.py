# Script to add scene control tools to mcp_ableton_server.py

# Read the file
with open('mcp_ableton_server.py', 'r') as f:
    content = f.read()

# Find the insertion point (before "# ----- TOOLS WITH RESPONSE -----")
insertion_point = content.find("# ----- TOOLS WITH RESPONSE -----")

# Scene control tools to add
scene_tools = """# ============= SCENE CONTROL TOOLS =============

@mcp.tool()
async def scene_launch(scene_index: int) -> str:
    \"\"\"Launch a scene.\"\"\"
    params = {"address": f"/live/scene/{scene_index}/launch", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Scene {scene_index} launched"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_scene_name(scene_index: int) -> str:
    \"\"\"Get the name of a scene.\"\"\"
    params = {"address": f"/live/scene/{scene_index}/get/name", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return str(result['data'][0]) if result['data'] else ""
        return str(result.get('status', ''))
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def set_scene_name(scene_index: int, name: str) -> str:
    \"\"\"Set the name of a scene.\"\"\"
    params = {"address": f"/live/scene/{scene_index}/set/name", "args": [str(name)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Scene {scene_index} name set to '{name}'"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_scene_color(scene_index: int) -> str:
    \"\"\"Get the color of a scene as hex string.\"\"\"
    params = {"address": f"/live/scene/{scene_index}/get/color", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return str(result['data'][0]) if result['data'] else ""
        return str(result.get('status', ''))
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def set_scene_color(scene_index: int, color: str) -> str:
    \"\"\"Set the color of a scene as hex string.\"\"\"
    params = {"address": f"/live/scene/{scene_index}/set/color", "args": [str(color)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Scene {scene_index} color set to '{color}'"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_scene_names() -> str:
    \"\"\"Get the names of all scenes.\"\"\"
    params = {"address": "/live/scene/get/names", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            scene_names = result['data']
            if scene_names:
                return ", ".join(str(name) for name in scene_names)
            return "No scenes found"
        return str(result.get('status', ''))
    return f"Error: {response.get('message', 'Unknown error')}"


"""

# Insert the scene tools
new_content = content[:insertion_point] + scene_tools + content[insertion_point:]

# Write back
with open('mcp_ableton_server.py', 'w') as f:
    f.write(new_content)

print("Scene control tools added successfully!")
