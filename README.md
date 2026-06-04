# Pluscode

A curated opencode configuration preset — Gentle AI skills, SDD workflow, agent orchestration, and persistent memory.

## What's inside

- **SDD Workflow** — Spec-Driven Development with 9 specialized sub-agents (init, explore, propose, spec, design, tasks, apply, verify, archive)
- **Agent Orchestration** — gentle-orchestrator coordinates sub-agents via background delegation
- **20+ Skills** — Hermes-style skills for PRs, issues, commits, docs, code review, dual review, and more
- **Persistent Memory** — Engram integration for cross-session context
- **Model Router** — Automatic model selection (Deepseek V4 Pro/Flash, MiMo 2.5 Pro)
- **Agno Integration** — Agno-powered MCP server for web search, code analysis, and Python execution

## Prerequisites

- [opencode](https://opencode.ai) installed
- [Bun](https://bun.sh) (for plugins)

## Install

```bash
# Clone into opencode global config
git clone https://github.com/YOUR_USER/pluscode.git ~/.config/opencode

# Install plugin dependencies
cd ~/.config/opencode
bun install
```

## Structure

```
~/.config/opencode/
├── AGENTS.md              # Agent instructions (persona, rules, memory protocol)
├── opencode.jsonc         # Main config (agents, MCP servers, permissions)
├── package.json           # Plugin dependencies
│
├── agents/                # Custom sub-agent definitions
│   ├── deepseek-pro.md
│   ├── deepseek-flash.md
│   └── mimo-pro.md
│
├── commands/              # Custom slash commands
│   ├── sdd-*.md
│
├── plugins/               # Bun/TS plugins
│   ├── background-agents.ts  # Async delegation system
│   └── engram.ts             # Persistent memory
│
├── prompts/               # SDD phase prompts
│   └── sdd/
│
├── skills/                # Hermes-style skills (20+)
│   ├── _shared/
│   ├── sdd-*/
│   ├── model-router/
│   ├── branch-pr/
│   ├── chained-pr/
│   ├── judgment-day/
│   ├── agno-agent/
│   └── ...
│
└── docs/
    └── skill-style-guide.md
```

## License

MIT
