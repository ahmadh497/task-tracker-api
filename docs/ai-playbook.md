# My Personal AI Coding Playbook

## 1. When I reach for AI first

- I use AI first when I need to understand unfamiliar repository code or plan a change before editing.
- I use AI for repetitive work such as documentation, test ideas, code review, and checking configuration files.

## 2. When I do not reach for AI

- I do not use AI when the task would require sharing passwords, tokens, credentials, or private data.
- I do not accept an AI-generated change when I cannot explain what the code does myself.

## 3. My non-negotiables

- I inspect the diff before accepting or committing AI-assisted changes.
- I do not paste real secrets, credentials, customer data, or production data into an AI tool.
- I run the relevant tests or verification commands before considering work complete.

## 4. My review rules

- I check which files changed and make sure the AI did not modify files outside the requested scope.
- I compare generated code with the existing project rules and API behavior.
- If I cannot explain an important line or decision, I investigate it before keeping the change.

## 5. What I am still figuring out

- I am still learning when Codex's repository context is more useful than working locally with Claude Code.
- I am still figuring out how much repository context to provide so AI gets enough evidence without reading unnecessary files.

## Decision Card

- For a new feature I reach for: Claude Code
- For code review I reach for: Codex
- For debugging I reach for: Claude Code
- For infrastructure I reach for: Claude Code
- For planning and governance I reach for: Codex
- I will never paste passwords, API keys, access tokens, credentials, or private customer data into an AI tool.
- My one rule is: I do not keep AI-generated work that I cannot explain and verify.
