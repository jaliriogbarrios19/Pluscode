# Pluscode

A curated opencode configuration preset — Gentle AI skills, SDD workflow, agent orchestration, and persistent memory. Model-agnostic: bring your own providers.

## What's inside

- **SDD Workflow** — Spec-Driven Development with 9 specialized sub-agents (init, explore, propose, spec, design, tasks, apply, verify, archive)
- **Agent Orchestration** — `gentle-orchestrator` coordinates sub-agents via background delegation
- **Model Router** — Automatic model-to-agent assignment based on task characteristics
- **20+ Skills** — Hermes-style skills for PRs, issues, commits, docs, code review, dual review, and more
- **Persistent Memory** — Engram integration for cross-session context (optional)
- **Agno Integration** — Agno-powered MCP server for web search, code analysis, and Python execution (optional)

## Prerequisites

- [opencode](https://opencode.ai) installed
- [Bun](https://bun.sh) (for plugins)
- [Python 3.11+](https://python.org) (for Agno MCP tools, optional)
- [Engram](https://github.com/anomalyco/engram) (for persistent memory, optional)

## Install

```bash
# Clone into opencode global config
git clone https://github.com/YOUR_USER/pluscode.git ~/.config/opencode

# Install plugin dependencies
cd ~/.config/opencode
bun install
```

## Configure Models

Pluscode is model-agnostic. The `model-router` skill selects the right agent for each task based on capabilities, not specific providers.

### Option 1: Single model for everything

Configure your primary provider in opencode. All agents will use it by default.

```
/add-provider
```

### Option 2: Assign models by capability

Edit `opencode.jsonc` and add `model` to each agent based on its needs:

```jsonc
{
  "agent": {
    "gentle-orchestrator": { "model": "your-provider/best-model" },
    "sdd-apply":           { "model": "your-provider/coding-model" },
    "sdd-design":          { "model": "your-provider/creative-model" },
    "sdd-tasks":           { "model": "your-provider/fast-model" }
  }
}
```

### Agent capability profiles

| Agent | Profile | Best for |
|-------|---------|----------|
| `gentle-orchestrator` | Coordination | Orchestrating sub-agents, decision-making |
| `sdd-design` | Creative | Architecture, UX, holistic system design |
| `sdd-apply` | Coding | Code generation, debugging, refactoring |
| `sdd-explore` | Analysis | Large codebase exploration, research |
| `sdd-propose`, `sdd-spec` | Reasoning | Structured proposals and specifications |
| `sdd-tasks`, `sdd-archive` | Speed | Mechanical decomposition, lightweight tasks |
| `sdd-verify` | Precision | Systematic validation and testing |

Three generic agent definitions are included for use with `delegate`:

| Agent | Type | Use for |
|-------|------|---------|
| `pro` | Primary | Code generation, debugging, refactoring, long context |
| `fast` | Fast/cheap | Quick fixes, simple searches, bulk text processing |
| `design` | Creative | Architecture, UX, system design, non-linear thinking |

### Optional: Engram persistent memory

[Install Engram](https://github.com/anomalyco/engram), then enable it in `opencode.jsonc`:

```jsonc
"engram": {
  "command": ["engram", "mcp", "--tools=agent"],
  "enabled": true,
  "type": "local"
}
```

### Optional: Agno MCP tools

Install Agno's Python dependencies:

```bash
pip install -e /path/to/agno/libs/agno mcp
```

The `web_search` and `python_exec` tools work out of the box. For `code_analyze`, set a model API key:

```bash
export OPENAI_API_KEY="sk-..."
```

## Structure

```
~/.config/opencode/
├── AGENTS.md              # Agent instructions (persona, rules, memory protocol)
├── opencode.jsonc         # Main config (agents, MCP servers, permissions)
├── package.json           # Plugin dependencies
│
├── agents/                # Generic sub-agent definitions
│   ├── pro.md             # Primary agent for complex work
│   ├── fast.md            # Fast agent for quick tasks
│   └── design.md          # Design-oriented agent
│
├── commands/              # Custom slash commands
│   └── sdd-*.md
│
├── plugins/               # Bun/TS plugins
│   ├── background-agents.ts  # Async delegation system
│   └── engram.ts             # Persistent memory adapter
│
├── prompts/               # SDD phase prompts
│   └── sdd/
│       ├── sdd-orchestrator.md
│       ├── sdd-apply.md, sdd-design.md, ...
│
├── skills/                # Hermes-style skills (20+)
│   ├── _shared/
│   ├── sdd-*/
│   ├── model-router/
│   ├── agno-agent/
│   ├── branch-pr/, chained-pr/, judgment-day/
│   └── ...
│
└── docs/
    └── skill-style-guide.md
```

## License

MIT
