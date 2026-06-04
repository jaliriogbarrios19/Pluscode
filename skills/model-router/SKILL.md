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
- **The matrix is a guide, not a hardcoded switch.** Use judgment — if a task spans multiple categories, pick the dominant one.
- **"A falta de pan, buenas son tortas."** The last fallback is ALWAYS the primary agent. The work gets done, period.
- **Cost-awareness**: prefer `@deepseek-flash` for trivial work, reserve MiMo for its unique strengths (visual, design, agentic).

## Workflow

### Step 1: Classify the Task

Read the user's request and map it to ONE row in the decision matrix below. If ambiguous, pick the closest match.

### Step 2: Delegate to First Choice

Use the `task` tool to delegate to the recommended subagent. (The user can also invoke them directly with `@mention`, but you as the agent use `task`.)

### Step 3: Graceful Fallback

If the subagent is unavailable or the model errors:
- The `task` tool will return an error (agent not found, model unavailable, timeout). Treat ANY non-success response as a failure.
- Fall back to the next column in the same row immediately — do not retry the same agent twice.
- Continue down the chain until the work gets done.
- Never complain, never ask the user "which model should I use instead" — just execute the fallback silently.

## Decision Matrix

| Task Type | First Choice | Fallback 1 | Fallback 2 |
|-----------|-------------|------------|------------|
| **Code: generation, debugging, refactors, complex logic** | `@deepseek-pro` | `@mimo-pro` | primary agent |
| **Architecture: system design, knowledge org, workflows** | `@mimo-pro` | `@deepseek-pro` | primary agent |
| **Visual: image generation, diagrams, multimodal content** | `@mimo-pro` | primary (textual alt) | — |
| **Fast: quick fixes, searches, trivial edits, one-liners** | `@deepseek-flash` | primary agent | — |
| **Heavy context: long docs, 100k+ token analysis** | `@deepseek-pro` | `@mimo-pro` | primary agent |
| **UI code: HTML/CSS/JSX, component styling** | `@deepseek-pro` | `@mimo-pro` | primary agent |
| **Autonomous: multi-step workflows, agent chains** | `@mimo-pro` | `@deepseek-pro` | primary agent |
| **Bulk: mass text processing, format conversions, simple gen** | `@deepseek-flash` | `@deepseek-pro` | primary agent |

### Model Profiles

| Subagent | Model | Best For | Cost |
|----------|-------|----------|------|
| `@mimo-pro` | MiMo 2.5 Pro (Xiaomi) | Visual gen, system design, agentic tasks, multimodal | Higher |
| `@deepseek-pro` | Deepseek V4 Pro | Agentic coding, debugging, long context, UI code | Low |
| `@deepseek-flash` | Deepseek V4 Flash | Quick fixes, searches, bulk simple tasks | Lowest |

## Pitfalls

1. **Sending image generation to Deepseek.** Deepseek has no native image gen — MiMo is the only option for that.
2. **Using MiMo for trivial fixes.** MiMo is more expensive — a quick search or one-line fix wastes money on it.
3. **Getting stuck when a model is down.** The fallback chain exists for a reason. Use it immediately.
4. **Over-thinking the classification.** If a task is 60% coding and 40% design, pick coding. Don't split hairs.

## Verification Checklist

- [ ] Task was classified against the decision matrix
- [ ] First-choice subagent was attempted
- [ ] If first choice failed, fallback was attempted silently
- [ ] Primary agent handled the task as last resort if all else failed
- [ ] Cost-appropriate model was selected (flash for trivial, pro for complex)
