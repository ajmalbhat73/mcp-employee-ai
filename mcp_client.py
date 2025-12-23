import requests

MCP_SERVER = "http://localhost:3333"


def fetch_tools():
    """
    Discover available MCP tools
    """
    response = requests.get(f"{MCP_SERVER}/mcp/tools")
    response.raise_for_status()
    return response.json()


def call_tool(tool_name, args):
    """
    Execute an MCP tool dynamically
    """
    tools = fetch_tools()
    tool = next(t for t in tools if t["name"] == tool_name)

    response = requests.post(
        f"{MCP_SERVER}{tool['endpoint']}",
        json=args
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print("\n🔍 Discovering MCP tools...")
    tools = fetch_tools()
    for t in tools:
        print(f" - {t['name']}")

    print("\n🧪 Example MCP Calls\n")

    print("➡ Employees in Bangalore:")
    print(call_tool("get_employees_by_location", {"location": "Bangalore"}))

    print("\n➡ Details for Amit:")
    print(call_tool("get_employee_by_name", {"first_name": "Amit"}))

    print("\n➡ Employees reporting to EMP-1002:")
    print(call_tool("get_direct_reports", {"manager_employee_id": "EMP-1002"}))
