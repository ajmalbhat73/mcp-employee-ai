import requests
import json
from openai import OpenAI

# ============================================================
# CONFIG
# ============================================================

MCP_SERVER = "http://localhost:3333"
client = OpenAI()

# ============================================================
# CONVERSATION MEMORY (STATE)
# ============================================================
# This is what makes the LLM "remember" context
conversation_history = [
    {
        "role": "system",
        "content": (
            "You are an HR analytics assistant. "
            "You remember conversation context and resolve pronouns "
            "like he, she, his, her, that employee based on prior answers. "
            "Use tools whenever structured employee data is required."
        )
    }
]

# ============================================================
# FETCH MCP TOOLS (DISCOVERY)
# ============================================================

def fetch_mcp_tools():
    """
    Fetch tool metadata from MCP server
    and convert it to OpenAI tool schema
    """
    mcp_tools = requests.get(f"{MCP_SERVER}/mcp/tools").json()

    openai_tools = []
    for tool in mcp_tools:
        openai_tools.append({
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": {
                    "type": "object",
                    "properties": {
                        key: {"type": "string"}
                        for key in tool["input_schema"].keys()
                    },
                    "required": list(tool["input_schema"].keys())
                }
            }
        })

    return openai_tools, mcp_tools


# ============================================================
# EXECUTE MCP TOOL
# ============================================================

def call_mcp_tool(tool_name, args, tool_registry):
    """
    Call MCP server tool dynamically
    """
    tool = next(t for t in tool_registry if t["name"] == tool_name)

    response = requests.post(
        f"{MCP_SERVER}{tool['endpoint']}",
        json=args
    )
    response.raise_for_status()
    return response.json()


# ============================================================
# MAIN ASK FUNCTION
# ============================================================

def ask(question: str):
    global conversation_history

    # Add user message to memory
    conversation_history.append(
        {"role": "user", "content": question}
    )

    openai_tools, tool_registry = fetch_mcp_tools()

    # ----------------------------
    # 1️⃣ LLM decides whether to use a tool
    # ----------------------------
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=conversation_history,
        tools=openai_tools,
        tool_choice="auto"
    )

    msg = response.choices[0].message

    # ----------------------------
    # 2️⃣ If LLM calls a tool
    # ----------------------------
    if msg.tool_calls:
        tool_call = msg.tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        print(f"\n🛠 LLM chose tool: {tool_name}")
        print(f"📥 Arguments: {tool_args}")

        # Store tool-call decision in memory
        conversation_history.append(msg)

        # Execute MCP tool
        tool_result = call_mcp_tool(tool_name, tool_args, tool_registry)

        # Store tool result in memory (CRITICAL)
        conversation_history.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result)
        })

        # ----------------------------
        # 3️⃣ LLM reasons over tool result
        # ----------------------------
        final_response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=conversation_history
        )

        assistant_message = final_response.choices[0].message
        conversation_history.append(assistant_message)

        return assistant_message.content

    # ----------------------------
    # 4️⃣ No tool needed
    # ----------------------------
    conversation_history.append(msg)
    return msg.content


# ============================================================
# CLI ENTRY POINT
# ============================================================

if __name__ == "__main__":
    print("🤖 MCP-powered HR Assistant")
    print("Context-aware | Tool-driven | Deterministic")
    print("Type 'exit' to quit\n")

    while True:
        q = input("Ask a question: ")
        if q.lower() == "exit":
            break

        answer = ask(q)
        print("\n💬 Answer:")
        print(answer)
        print("-" * 60)
