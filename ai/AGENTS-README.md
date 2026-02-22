
## Setup commands
- Install deps: `pnpm install`
- Start dev server: `pnpm dev`
- Run tests: `pnpm test`

## Code style
- TypeScript strict mode
- Single quotes, no semicolons
- Use functional patterns where possible

Why AGENTS.md?
README.md files are for humans: quick starts, project descriptions, and contribution guidelines.

AGENTS.md complements this by containing the extra, sometimes detailed context coding agents need: build steps, tests, and conventions that might clutter a README or aren’t relevant to human contributors.

We intentionally kept it separate to:

Give agents a clear, predictable place for instructions.

Keep READMEs concise and focused on human contributors.

Provide precise, agent-focused guidance that complements existing README and docs.

Rather than introducing another proprietary file, we chose a name and format that could work for anyone. If you’re building or using coding agents and find this helpful, feel free to adopt it.

One AGENTS.md works across many agents
Your agent definitions are compatible with a growing ecosystem of AI coding agents and tools: 

How to use AGENTS.md?
1. Add AGENTS.md
Create an AGENTS.md file at the root of the repository. Most coding agents can even scaffold one for you if you ask nicely.
2. Cover what matters
Add sections that help an agent work effectively with your project. Popular choices:

Project overview
Build and test commands
Code style guidelines
Testing instructions
Security considerations
3. Add extra instructions
Commit messages or pull request guidelines, security gotchas, large datasets, deployment steps: anything you’d tell a new teammate belongs here too.
4. Large monorepo? Use nested AGENTS.md files for subprojects
Place another AGENTS.md inside each package. Agents automatically read the nearest file in the directory tree, so the closest one takes precedence and every subproject can ship tailored instructions. For example, at time of writing the main OpenAI repo has 88 AGENTS.md files.
About
AGENTS.md emerged from collaborative efforts across the AI software development ecosystem, including OpenAI Codex, Amp, Jules from Google, Cursor, and Factory.

We’re committed to helping maintain and evolve this as an open format that benefits the entire developer community, regardless of which coding agent you use.

AGENTS.md is now stewarded by the Agentic AI Foundation under the Linux Foundation. Learn more →

FAQ
Are there required fields?
No. AGENTS.md is just standard Markdown. Use any headings you like; the agent simply parses the text you provide.
What if instructions conflict?
The closest AGENTS.md to the edited file wins; explicit user chat prompts override everything.
Will the agent run testing commands found in AGENTS.md automatically?
Yes—if you list them. The agent will attempt to execute relevant programmatic checks and fix failures before finishing the task.
Can I update it later?
Absolutely. Treat AGENTS.md as living documentation.
How do I migrate existing docs to AGENTS.md?
Rename existing files to AGENTS.md and create symbolic links for backward compatibility:

mv AGENT.md AGENTS.md && ln -s AGENTS.md AGENT.md

How do I configure Aider?
Configure Aider to use AGENTS.md in .aider.conf.yml:

read: AGENTS.md

How do I configure Gemini CLI?
Configure Gemini CLI to use AGENTS.md in .gemini/settings.json:

{ "contextFileName": "AGENTS.md" }
