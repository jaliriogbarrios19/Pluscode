---
name: agno-agent
description: "Trigger: agno, agent runtime, build agent, delegate to agent, web search, code analysis. Create and run Agno agents as MCP tools."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
  tags: [agno, agent, mcp, tools]
  related_skills: [model-router]
---

## When to Use

- You need web search, code analysis, or Python execution beyond opencode's built-in tools
- You want to delegate complex multi-step reasoning to a specialized agent
- User mentions "agno", "agent runtime", "build an agent"
- You need RAG over documentation or knowledge bases

Don't use for:
- Simple file reads or edits — use opencode's native `read`, `edit`, `grep`
- Git operations — use `bash`
- Tasks that fit existing SDD sub-agents (apply, design, etc.)

## Critical Rules

- The MCP server runs via `python` using the system Python at `C:\Users\Usuario\AppData\Local\Python\bin\python.exe`
- API keys for models are read from environment variables (`OPENAI_API_KEY`, etc.)
- Tools without external API dependencies (web search, python exec) work without configuration

## Workflow

### Step 1: Ensure the MCP server is enabled

The `agno-agent` MCP server is configured in `opencode.jsonc`. Verify it's enabled.

### Step 2: Use tools in prompts

```
Search the web for "latest Python 3.14 release notes". use agno-agent
```

```
Analyze this code for potential bugs. use agno-agent
```

## Available Tools

| Tool | Description | Requires API Key |
|------|-------------|-----------------|
| `web_search` | Search the web using DuckDuckGo | No |
| `python_exec` | Execute Python code in a sandbox | No |
| `code_analyze` | Analyze code with an Agno agent | Yes (any model provider) |

## Pitfalls

1. **API key not set.** The `code_analyze` tool requires a model provider API key. Set `OPENAI_API_KEY` or equivalent env var.
2. **Python not found.** The MCP server command must point to the system Python at `C:\Users\Usuario\AppData\Local\Python\bin\python.exe`.

## Verification Checklist

- [ ] `web_search("test")` returns search results
- [ ] `python_exec("print(2+2)")` returns `4`
- [ ] MCP server shows as enabled in opencode
