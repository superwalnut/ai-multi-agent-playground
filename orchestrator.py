import anthropic
import json
from subagents import research_agent, analyst_agent, writer_agent

client = anthropic.Anthropic()
MODEL = "claude-sonnet-4-20250514"

# Define tools the orchestrator can use to dispatch subagents
TOOLS = [
    {
        "name": "research",
        "description": "Research a specific topic or question. Use this to gather raw information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "The topic or question to research"}
            },
            "required": ["topic"]
        }
    },
    {
        "name": "analyze",
        "description": "Analyze research data to find patterns, risks, and opportunities.",
        "input_schema": {
            "type": "object",
            "properties": {
                "data": {"type": "string", "description": "The research data to analyze"}
            },
            "required": ["data"]
        }
    },
    {
        "name": "write",
        "description": "Write a polished final output from the research and analysis.",
        "input_schema": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "The content to write up"},
                "format_type": {"type": "string", "description": "Type of output: report, summary, blog post, etc.", "default": "report"}
            },
            "required": ["content"]
        }
    }
]


def dispatch_tool(tool_name: str, tool_input: dict) -> str:
    """Route tool calls to the appropriate subagent."""
    print(f"\n  → Dispatching to [{tool_name}] subagent...")

    if tool_name == "research":
        result = research_agent(tool_input["topic"])
    elif tool_name == "analyze":
        result = analyst_agent(tool_input["data"])
    elif tool_name == "write":
        result = writer_agent(
            tool_input["content"],
            tool_input.get("format_type", "report")
        )
    else:
        result = f"Unknown tool: {tool_name}"

    print(f"  ✓ [{tool_name}] subagent complete ({len(result)} chars)")
    return result


def run_orchestrator(user_task: str) -> str:
    """
    Orchestrator agent loop.
    Keeps running until the orchestrator stops using tools and returns a final answer.
    """
    print(f"\n🎯 Task received: {user_task}")
    print("=" * 60)

    messages = [{"role": "user", "content": user_task}]

    # Agentic loop — runs until no more tool calls
    while True:
        print("\n🧠 Orchestrator thinking...")

        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system="""You are an orchestrator agent. Your job is to:
1. Break down the user's task into subtasks
2. Use your tools (research, analyze, write) in the right order
3. Pass outputs from one tool as inputs to the next
4. Synthesize a final answer once all subtasks are done

Always think step by step. Use tools when needed. When you have everything you need, respond with the final result directly.""",
            tools=TOOLS,
            messages=messages
        )

        # If no tool calls — orchestrator is done
        if response.stop_reason == "end_turn":
            final = next(
                (block.text for block in response.content if hasattr(block, "text")),
                "No response generated."
            )
            print("\n✅ Orchestrator complete.")
            return final

        # Process tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = dispatch_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        # Append assistant response + tool results to message history
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
