---
name: plan-and-goal
description: Use when the user wants to build an implementation plan and a matching `/goal` prompt to drive Claude Code through it autonomously. Triggers on phrases like "plan and goal", "/plan-and-goal", "build a plan and a goal prompt", or when the user asks to scope a task into a plan file plus a goal directive. Produces a plan markdown file in /tmp and a self-contained goal prompt that points back at the plan.
---

# Plan and Goal

The user wants two artifacts:

1. **A plan file** at `/tmp/<plan-name>.md` containing the implementation plan AND the acceptance criteria that prove the work is done.
2. **A `/goal` prompt** that another Claude Code session can paste in. The prompt tells that session to read the plan file, execute it, and verify against the acceptance criteria recorded in the same file.

The goal prompt should be self-contained but lean — the plan file holds the detail. The goal session uses bypass permissions and has no turn cap.

## When to activate

**Auto-trigger on signals:**
- The user types `/plan-and-goal` or says "use plan-and-goal"
- The user asks for "a plan and a goal" / "plan plus goal prompt" / "scope this into a plan and goal"
- The user describes a substantive task they want a separate Claude session to drive autonomously and asks for the artifacts to kick it off

**Don't activate when:**
- The user wants the plan only (no autonomous execution) — write the plan, skip the goal prompt
- The user wants execution right now in this session — just do the work, don't build artifacts
- The task is trivial enough that a one-line directive suffices

## What you produce

### 1. The plan file: `/tmp/<plan-name>.md`

Pick a short kebab-case slug for `<plan-name>` based on the task. Confirm the slug with the user if it's not obvious.

Structure:

```markdown
# <Task title>

## Context
<2–5 sentences. What's being built/changed and why. Reference specific files, services, or systems by name. Enough that someone reading the plan cold knows what they're walking into.>

## Assumptions
<Bulleted list of things you're taking as given. Surface assumptions explicitly so the implementer can challenge them if wrong.>

## Out of scope
<Bulleted list of things deliberately not included. Prevents scope creep during execution.>

## Implementation plan

### Step 1: <name>
<What changes, in which files. Concrete enough to execute. Include file paths and the shape of the change.>

### Step 2: <name>
...

## Acceptance criteria
<Numbered list. Each item must be something the executing Claude session can demonstrate in its transcript — a command output, a test result, a file diff, a grep hit. The /goal evaluator only sees what the session surfaces.>

1. <criterion> — proven by: <`command` / file existence / test pass / etc.>
2. ...

## Verification commands
<Concrete commands the executing session should run to demonstrate each criterion. One command per criterion when possible.>

```bash
<cmd 1>
<cmd 2>
```
```

**Rules for the plan file:**
- Keep the plan tight. Steps describe what changes, not narrate decisions.
- Acceptance criteria must be observable from the conversation — `/goal`'s evaluator can't run commands itself; it reads what the session has already output.
- Every acceptance criterion needs a concrete proof method (command, test, grep, file diff). "Code is clean" is not an acceptance criterion. "`npm run lint` exits 0" is.
- Include the verification commands inline so the executing session knows exactly what to run.

### 2. The goal prompt

Output the goal prompt in a fenced code block so the user can copy it. It should look like:

```text
/goal Read /tmp/<plan-name>.md, execute the implementation plan, and satisfy every numbered item in the Acceptance criteria section. After each step, run the relevant Verification commands from the plan and show the output. The condition is met when every acceptance criterion in the plan file has been demonstrated in this transcript with passing output. If a criterion fails, fix the underlying cause and re-run — do not skip, mock, or weaken any criterion. Do not modify the plan file's Acceptance criteria section.
```

**Rules for the goal prompt:**
- Single `/goal` directive. No extra prose around it.
- Point at the plan file by absolute path.
- Tell the session to surface command output (the evaluator only sees what's in the transcript).
- Forbid weakening or skipping acceptance criteria.
- **No turn cap.** Do not include "or stop after N turns" — the user wants it to run until done.
- **No mention of auto mode.** The user runs with bypass permissions, not auto mode.
- Keep it under ~600 chars when possible. The plan file carries the detail.

## Workflow

1. **Understand the task.** If the user gave a vague brief, ask 1–3 sharp questions to get the scope, constraints, and what "done" looks like. Don't ask if it's already clear.
2. **Pick a plan slug.** Short kebab-case. Mention it to the user.
3. **Write the plan file** to `/tmp/<plan-slug>.md` using the structure above.
4. **Output the goal prompt** in a copyable code block, referencing the plan file's absolute path.
5. **Tell the user the next step** — paste the goal prompt into a Claude Code session running with bypass permissions.

## Anti-patterns — STOP if you're doing these

| Anti-pattern | Fix |
|---|---|
| Acceptance criteria the evaluator can't see (e.g., "code is well-organized") | Replace with observable proof: command exits 0, test passes, grep returns expected count. |
| Goal prompt with a turn cap | Remove it. User explicitly asked for no turn cap. |
| Goal prompt mentioning auto mode | Remove. User uses bypass permissions. |
| Plan file padded with restatement of the user's brief | Cut it. Context section is 2–5 sentences max. |
| Plan and goal prompt duplicate the same content | Plan holds detail; goal prompt references it. Keep the goal prompt lean. |
| Verification commands the executing session can't actually run (wrong cwd, missing tools) | Write commands that work from the repo root with tools the session has. |
| Asking the user to confirm every step before writing the plan | One round of questions max. Then write. They can edit. |
| Writing the plan to the repo instead of `/tmp` | Always `/tmp/<plan-name>.md`. The plan is execution scaffolding, not a repo artifact. |

## Self-check before handing back to the user

- Does every acceptance criterion have a concrete proof method that will appear in the executing session's transcript?
- Does the plan file's Verification commands section actually run those proofs?
- Is the goal prompt a single `/goal …` line in a copyable code block, with no turn cap and no auto-mode reference?
- Is the plan path absolute (`/tmp/<plan-name>.md`) in the goal prompt?
- Did I tell the user where the plan lives and what to do with the goal prompt?
