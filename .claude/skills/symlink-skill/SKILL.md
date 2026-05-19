---
name: symlink-skill
description: Use when the user wants to install a skill from this AgentScripts repo into their global `~/.claude/skills/` directory by creating a symlink. Triggers on phrases like "symlink the skill", "install this skill globally", "link the <name> skill", or "/symlink-skill <name>". Creates `~/.claude/skills/<skill-name>` pointing to `./.claude/skills/<skill-name>` in this repo so edits in the repo take effect everywhere.
allowed-tools: Bash(ls:*), Bash(ln:*), Bash(test:*), Bash(readlink:*), Bash(rm:*)
---

# Symlink Skill

The user is iterating on skills in `~/workspace/AgentScripts/.claude/skills/` and wants them available globally at `~/.claude/skills/<skill-name>` via a symlink — so a single edit in the repo is picked up by every Claude Code session.

## When to activate

- The user says "symlink the `<name>` skill", "install `<name>` skill globally", "link `<name>`"
- The user invokes `/symlink-skill <name>` or runs the skill by name with a target
- The user just finished creating a new skill in this repo and asks to make it available

## Inputs

You need one input: `<skill-name>` — the directory name under `./.claude/skills/`.

If the user didn't pass one explicitly:
- If they just created or edited a skill in this conversation, infer that name and confirm in one short sentence before linking.
- Otherwise ask which skill to link.

## Procedure

Run from the repo root (`/Users/kevinluo/workspace/AgentScripts`). Use absolute paths so it doesn't matter where the user invoked from.

For a given `<skill-name>`:

1. **Verify source exists.** `test -d /Users/kevinluo/workspace/AgentScripts/.claude/skills/<skill-name>`. If not, stop and tell the user the skill directory doesn't exist.

2. **Check the target.** `ls -la ~/.claude/skills/<skill-name>` — there are four cases:
   - **Doesn't exist** → create the symlink.
   - **Already a symlink to the correct source** → tell the user it's already linked, do nothing.
   - **A symlink to a different path** → show the current target, ask the user to confirm replacement before `rm` + relink.
   - **A real directory or file** → STOP. Do not delete it. Show the user what's there and ask how to proceed (they may have a non-symlinked copy with edits).

3. **Create the symlink.** `ln -s /Users/kevinluo/workspace/AgentScripts/.claude/skills/<skill-name> /Users/kevinluo/.claude/skills/<skill-name>`. Use absolute paths — relative symlinks break when resolved from `~/.claude/skills/`.

4. **Verify.** `readlink ~/.claude/skills/<skill-name>` and confirm it matches the source path. Report the result in one line.

## Anti-patterns — STOP if you're doing these

| Anti-pattern | Fix |
|---|---|
| Using a relative symlink target like `../../workspace/AgentScripts/...` | Always use the absolute path — it's stable regardless of where the link is resolved from. |
| Deleting an existing real directory at the target without asking | Real directories may contain unmerged work. Ask first. |
| Silently replacing a symlink that points elsewhere | Confirm with the user; the existing link may be intentional. |
| Running `ln` without first checking the source exists | Check first — a broken symlink to a missing source is worse than a clear error. |
| Asking the user for the skill name when they just told you in the previous turn | Infer from context, confirm in one line, proceed. |

## Example

User: *"symlink the plan-and-goal skill"*

You:
1. Confirm `./.claude/skills/plan-and-goal/` exists.
2. Check `~/.claude/skills/plan-and-goal` — doesn't exist.
3. `ln -s /Users/kevinluo/workspace/AgentScripts/.claude/skills/plan-and-goal /Users/kevinluo/.claude/skills/plan-and-goal`
4. `readlink ~/.claude/skills/plan-and-goal` → matches.
5. Report: "Linked `plan-and-goal` → `~/.claude/skills/plan-and-goal`. Available globally now."
