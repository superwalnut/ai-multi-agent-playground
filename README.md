# ai-multi-agent-playground
3. Hierarchical (Orchestrator-Subagent) A top-level agent breaks down tasks and delegates to specialized subagents, which may themselves spawn further agents. Example: Manager agent → Specialist agents → Worker agents

## Hierarchical (Orchestrator-Subagent)
Best for complex, open-ended tasks that require planning, delegation, and synthesis.

Software engineering projects (plan → delegate features → integrate)
Business analysis requiring multiple specialist inputs
Large report generation with many sections and sources
Autonomous research agents that self-direct

Great choice — Orchestrator-Subagent is the most powerful and flexible pattern. Here are your main options for building it locally:

## Frameworks
1. LangGraph (most popular for this pattern)

Built specifically for multi-agent graphs with state management
You define nodes (agents) and edges (flow between them)
Supports cycles, human-in-the-loop, and persistence
Python-based

2. CrewAI

Higher-level abstraction — define "crews" with roles, goals, and tasks
Easier to get started, less flexible than LangGraph
Good for role-based agent teams (e.g., Researcher, Writer, Critic)

3. AutoGen (Microsoft)

Conversation-based multi-agent framework
Agents talk to each other via messages
Good for debate/collaborative patterns too

4. LlamaIndex Workflows

Event-driven orchestration
Good if you're already using LlamaIndex for RAG

5. Raw API (no framework)

Just use the Anthropic SDK directly
Orchestrator calls Claude, parses output, routes to subagent functions
Most control, most boilerplate


Local LLM Options (if you want fully local, no API cost)
ToolPurposeOllamaRun models locally (Llama 3, Mistral, Qwen, etc.)LM StudioGUI for running local modelsJanAnother local model runner
These expose an OpenAI-compatible API so LangGraph/CrewAI can point to them instead of Claude/OpenAI.

## Minimal Architecture (Raw API approach)

```
Orchestrator (Claude)
  ├── receives user task
  ├── breaks it into subtasks
  ├── calls SubagentA(subtask1)
  ├── calls SubagentB(subtask2)
  └── synthesizes results → final output
```

## I can generate a minimal working Orchestrator-Subagent setup in Python using either:
Raw Anthropic SDK (simplest, most transparent)
LangGraph (more scalable)
CrewAI (easiest to read)

Which would you prefer, and do you want it to use the Claude API or a local model via Ollama?

## Here's a clean, fully working Orchestrator-Subagent example using the raw Anthropic SDK:

Project Structure

multi_agent/
├── orchestrator.py      # Main orchestrator agent
├── subagents.py         # Specialist subagents
├── main.py              # Entry point
└── requirements.txt

### How to Run

```
# 1. Install dependencies
pip install anthropic python-dotenv

# 2. Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# 3. Run
python main.py
```
### What Happens Under the Hood

```
User task
   ↓
Orchestrator (decides plan)
   ↓
Tool call → research subagent → result
   ↓
Tool call → analyze subagent → result  
   ↓
Tool call → write subagent → result
   ↓
Orchestrator synthesizes → Final output
```

