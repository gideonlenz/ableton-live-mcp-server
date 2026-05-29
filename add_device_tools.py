# Script to add device control tools to mcp_ableton_server.py

# Read the file
with open('mcp_ableton_server.py', 'r') as f:
    content = f.read()

# Find the insertion point (before # ----- TOOLS WITH RESPONSE -----)
insertion_marker = "# ----- TOOLS WITH RESPONSE -----"
insertion_point = content.find(insertion_marker)

# Device control tools to add
device_tools = '''
# ============= DEVICE CONTROL TOOLS =============

@mcp.tool()
async def get_device_name(track_index: int, device_index: int) -> str:
    """Get the name of a device on a track."""
    params = {"address": f"/live/device/{track_index}/{device_index}/get/name", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return str(result['data'][0]) if result['data'] else ""
        return str(result.get('status', ''))
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_device_parameters(track_index: int, device_index: int) -> str:
    """Get the parameters of a device as a list."""
    params = {"address": f"/live/device/{track_index}/{device_index}/get/parameters", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            params_list = result['data']
            if params_list:
                return ", ".join(str(p) for p in params_list)
            return "No parameters found"
        return str(result.get('status', ''))
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_device_parameter(track_index: int, device_index: int, param_index: int) -> float:
    """Get the value of a specific device parameter."""
    params = {"address": f"/live/device/{track_index}/{device_index}/get/parameter/{param_index}", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return float(result['data'][0]) if result['data'] else 0.0
        return float(result.get('status', 0))
    raise ValueError(f"Error getting device parameter: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_device_parameter(track_index: int, device_index: int, param_index: int, value: float) -> str:
    """Set the value of a specific device parameter."""
    params = {"address": f"/live/device/{track_index}/{device_index}/set/parameter/{param_index}", "args": [float(value)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Device {device_index} on track {track_index}, parameter {param_index} set to {value}"
    return f"Error: {response.get('message', 'Unknown error')}"


@mcp.tool()
async def get_device_bypass(track_index: int, device_index: int) -> bool:
    """Get whether a device is bypassed."""
    params = {"address": f"/live/device/{track_index}/{device_index}/get/bypass", "args": []}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        result = response.get('result', {})
        if 'data' in result:
            return bool(result['data'][0]) if result['data'] else False
        return bool(result.get('status', False))
    raise ValueError(f"Error getting device bypass: {response.get('message', 'Unknown error')}")


@mcp.tool()
async def set_device_bypass(track_index: int, device_index: int, bypass: bool) -> str:
    """Set whether a device should be bypassed."""
    params = {"address": f"/live/device/{track_index}/{device_index}/set/bypass", "args": [int(bypass)]}
    response = await ableton_client.send_rpc_request("send_message", params)
    if response['status'] == 'ok':
        return f"Device {device_index} on track {track_index} bypass {'enabled' if bypass else 'disabled'}"
    return f"Error: {response.get('message', 'Unknown error')}"


'''

# Insert the new tools before the marker
new_content = content[:insertion_point] + device_tools + content[insertion_point:]

# Write back
with open('mcp_ableton_server.py', 'w') as f:
    f.write(new_content)

print("Device control tools added successfully!")
