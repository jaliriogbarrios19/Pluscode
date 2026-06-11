---
name: model-router
description: "Trigger: modelo, model routing, qué modelo usar, MiMo, Deepseek, switch model, cambiar modelo. Route tasks to the optimal AI model with graceful fallback chains."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
  tags: [models, routing, cost-optimization, fallback]
  related_skills: []
  platforms: [linux, macos, windows]
---

## When to Use

- User asks which model to use for a task ("¿qué modelo uso para...?", "should I use MiMo or Deepseek?")
- Primary agent needs to delegate work and wants to pick the most efficient subagent+model
- Cost-sensitive workflows where model selection matters
- User mentions "modelo", "MiMo", "Deepseek", "cambio de modelo", "routing"

Don't use for:
- Tasks where the primary agent can handle it trivially in 1-2 steps — don't over-engineer
- When the user explicitly specifies a model — respect their choice, don't override

## Critical Rules

- **NEVER block on model unavailability.** If a subagent fails or its model is down, immediately fall back to the next in the chain without asking.
- **10-second timeout rule.** If a delegated task takes more than 10 seconds without a response, treat it as a failure and fall back to the next model. Never wait — the user's time is worth more than a slow model.
- **The matrix is a guide, not a hardcoded switch.** Use judgment — if a task spans multiple categories, pick the dominant one.
- **"A falta de pan, buenas son tortas."** The last fallback is ALWAYS the primary agent. The work gets done, period.
- **Cost-awareness**: `@deepseek-pro` handles all code work — analysis, implementation, debugging. Use `@gemini-flash-lite` for heavy context (100K+ tokens) to save cost. `@qwen-coder` (local, free) for quick/trivial tasks. Reserve MiMo for design and architecture.

## Workflow

### Step 1: Classify the Task

Read the user's request and map it to ONE row in the decision matrix below. If ambiguous, pick the closest match.

### Step 2: Delegate to First Choice

Use the `task` tool to delegate to the recommended subagent. (The user can also invoke them directly with `@mention`, but you as the agent use `task`.)

### Step 3: Graceful Fallback

If the subagent is unavailable or the model errors:
- The `task` tool will return an error (agent not found, model unavailable, timeout). Treat ANY non-success response as a failure.
- **10-second rule**: if a delegated task hasn't produced a response after 10 seconds, cancel it and fall back. Never keep the user waiting.
- Fall back to the next column in the same row immediately — do not retry the same agent twice.
- Continue down the chain until the work gets done.
- Never complain, never ask the user "which model should I use instead" — just execute the fallback silently.

## Decision Matrix

| Task Type | First Choice | Fallback 1 | Fallback 2 | Fallback 3 |
|-----------|-------------|------------|------------|------------|
| **Code: implementation, debugging, analysis, refactors** | `@deepseek-pro` | `@mimo-pro` | primary agent | — |
| **Architecture: system design, knowledge org, workflows** | `@mimo-pro` | `@deepseek-pro` | primary agent | — |
| **Visual: image generation, diagrams, multimodal content** | `@mimo-pro` | primary (textual alt) | — | — |
| **Fast: quick fixes, searches, trivial edits, one-liners** | `@qwen-coder` | `@deepseek-flash` | primary agent | — |
| **Heavy context: long docs, 100k+ token analysis** | `@gemini-flash-lite` | `@deepseek-pro` | `@mimo-pro` | primary agent |
| **UI code: HTML/CSS/JSX, component styling** | `@deepseek-pro` | `@mimo-pro` | primary agent | — |
| **Autonomous: multi-step workflows, agent chains** | `@mimo-pro` | `@deepseek-pro` | primary agent | — |
| **Bulk: mass text processing, format conversions, simple gen** | `@qwen-coder` | `@deepseek-flash` | `@deepseek-pro` | primary agent |

### Model Profiles

| Subagent | Model | Best For | Cost |
|----------|-------|----------|------|
| `@qwen-coder` | Qwen2.5-Coder 7B (Alibaba) | Quick fixes, boilerplate, simple refactors, bulk processing | Free (local) |
| `@gemini-flash-lite` | Gemini 2.5 Flash Lite (Google) | Heavy context analysis, 1M token docs, codebase review | $0.10/$0.40 |
| `@mimo-pro` | MiMo 2.5 Pro (Xiaomi) | Visual gen, system design, agentic tasks, multimodal | Higher |
| `@deepseek-pro` | Deepseek V4 Pro | Implementation, debugging, analysis, refactors, UI code | $0.44/$0.87 |
| `@deepseek-flash` | Deepseek V4 Flash | Quick fixes, searches, bulk simple tasks | $0.10/$0.20 |

### Architecture

- **Deepseek V4 Pro** es el cerebro principal para todo el ciclo de código: analiza, implementa, depura, refactoriza. Es tu caballo de batalla.
- **Gemini Flash Lite** se usa exclusivamente para heavy context (documentos enormes, codebases de 100K+ tokens) donde su ventana de 1M tokens y su precio 25× menor que V4 Pro lo hacen imbatible.
- **Qwen Coder** (local, gratuito) para tareas rápidas y bulk.
- **MiMo** para diseño, visual y arquitectura.

## Pitfalls

1. **Sending image generation to Deepseek.** Deepseek has no native image gen — MiMo is the only option for that.
2. **Using MiMo for trivial fixes.** MiMo is more expensive — a quick search or one-line fix wastes money on it.
3. **Getting stuck when a model is down.** The fallback chain exists for a reason. Use it immediately.
4. **Over-thinking the classification.** If a task is 60% coding and 40% design, pick coding. Don't split hairs.
5. **Sending complex multi-file refactors to Qwen.** Qwen2.5-Coder is 7B — it handles single-file edits well but degrades on cross-cutting changes. If the task spans more than 2 files or requires architectural reasoning, go straight to `@deepseek-pro`.
6. **OpenRouter models require API key.** `@gemini-flash-lite` goes through OpenRouter. If the `OPENROUTER_API_KEY` env var is missing, it falls back silently to `@deepseek-pro`.

## Verification Checklist

- [ ] Task was classified against the decision matrix
- [ ] First-choice subagent was attempted
- [ ] If first choice failed, fallback was attempted silently
- [ ] Primary agent handled the task as last resort if all else failed
- [ ] Cost-appropriate model was selected (local free → OpenRouter budget → cloud pro)
