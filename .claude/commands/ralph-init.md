---
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion
description: Generate a PROMPT.md for running Ralph loops based on your project spec
---

Your task is to help the user create a PROMPT.md file for running Ralph loops with the ralph-loop plugin.

## Background

The ralph-loop plugin runs Claude Code in an iterative loop until a completion promise is detected:
```bash
/ralph-loop:ralph-loop @PROMPT.md --completion-promise "RALPH_COMPLETE" --max-iterations 50
```

Each iteration, Claude sees the same prompt but with modified files and git history from previous iterations. Key principles:
- One task per iteration - let Claude pick the most important thing
- Keep fix_plan.md as a rolling TODO list
- Git commit when tests pass
- Search before assuming something isn't implemented
- No placeholder implementations
- Output the completion promise when ALL tasks in fix_plan.md are done

## Your Task

1. First, search for existing spec files in the project:
   - Look for `specs/`, `spec/`, `SPEC.md`, `spec.md`, or similar
   - Look for `fix_plan.md` or `TODO.md`
   - Look for `CLAUDE.md` or `AGENT.md`

2. If specs exist, read them to understand the project.

3. Ask the user clarifying questions using AskUserQuestion:
   - What is the main goal for the Ralph loop? (e.g., "implement the spec", "fix bugs", "add tests")
   - What commands run the tests/build? (e.g., `npm test`, `pytest`, `cargo build`)
   - Any specific constraints? (e.g., "don't modify the database schema", "use existing UI components")

4. Generate a PROMPT.md file in the project root with this structure:

```markdown
# PROMPT.md - Ralph Loop Instructions

## Project Context
[Brief description of what this project is]

## Study These First
1. Read `specs/` to understand what needs to be built
2. Read `fix_plan.md` to see what's been done and what remains
3. Read `CLAUDE.md` for project-specific guidance

## Your Task This Iteration

1. Study `fix_plan.md` and choose the SINGLE most important incomplete item
2. Before coding, SEARCH the codebase - don't assume something isn't implemented
3. Implement the feature/fix FULLY - no placeholders or minimal implementations
4. Run tests: `[test command]`
5. If tests pass:
   - Update `fix_plan.md` (mark item complete, add any new discoveries)
   - Commit: `git add -A && git commit -m "[descriptive message]"`
6. If tests fail:
   - Debug and fix
   - Update `fix_plan.md` with what you learned

## Completion Check

After each task, check `fix_plan.md`:
- If ALL items are complete and tests pass: Output <promise>RALPH_COMPLETE</promise>
- If items remain: Continue to next iteration (do not output the promise)

## Rules

1. ONE task per iteration - pick the most important thing
2. SEARCH before implementing - use subagents to verify code doesn't exist
3. FULL implementations only - no placeholders, no TODOs, no "minimal" versions
4. ALWAYS update fix_plan.md - mark progress, add discoveries, note blockers
5. COMMIT when tests pass - descriptive messages, include fix_plan.md changes
6. If stuck after 3 attempts on same item, document the blocker and move on

## Commands
```
[build/test commands here]
```
```

5. Also create a `fix_plan.md` if one doesn't exist, seeded from the spec with items like:
```markdown
# Fix Plan

## Completed
- [ ] (items will be checked off as completed)

## In Progress
- [ ] (current focus)

## TODO
- [ ] Item 1 from spec
- [ ] Item 2 from spec
- [ ] etc.

## Blocked / Notes
(learnings and blockers go here)
```

6. Tell the user how to start their Ralph loop:

```
To start your Ralph loop:

1. Make sure the ralph-loop plugin is installed:
   /plugin → search "ralph-loop" → Space to select → "i" to install

2. Start the loop:
   /ralph-loop:ralph-loop @PROMPT.md --completion-promise "RALPH_COMPLETE" --max-iterations 50

3. Monitor progress:
   - Watch the terminal or check back periodically
   - Review git history to see what Ralph accomplished
   - Check fix_plan.md for current status

4. To stop early:
   /cancel-ralph
```
