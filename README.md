# Go Skills for Claude Code

Six [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) for Go work, published as a Claude Code marketplace: idiomatic Go, CLI architecture, design-spec review, release engineering, desktop apps, and file operations. Written by [spf13](https://github.com/spf13) — creator of Cobra, Viper, and Hugo, and former Go team lead.

## Skills

| Skill | What it covers | Install |
| --- | --- | --- |
| [`go`](./go/SKILL.md) | Idiomatic Go — package design, error handling, interfaces, concurrency, testing, and project layout. The one to read first. | `/plugin install go@go-skills` |
| [`cobra-viper`](./cobra-viper/SKILL.md) | CLI architecture with Cobra and Viper — command-first design, 12-factor configuration, environment-variable binding, and in-memory CLI testing. | `/plugin install cobra-viper@go-skills` |
| [`go-spec-reviewer`](./go-spec-reviewer/SKILL.md) | Review a Go design document before implementation begins — catches over-engineering, missing error paths, interface misuse, and Cobra/Viper convention violations while the plan is still cheap to change. | `/plugin install go-spec-reviewer@go-skills` |
| [`go-release`](./go-release/SKILL.md) | Release engineering — semantic-versioning promises, mechanical breaking-change detection, `Deprecated:` conventions, `go.mod` hygiene, and shipping binaries with GoReleaser. | `/plugin install go-release@go-skills` |
| [`wails`](./wails/SKILL.md) | Desktop apps in Go with Wails v2 (stable) and v3 (alpha) — including how to tell the two apart, since their APIs are incompatible and easily blended by mistake. | `/plugin install wails@go-skills` |
| [`fileflow-pathologize`](./fileflow-pathologize/SKILL.md) | Safe file operations with `spf13/fileflow` and `spf13/pathologize` — cross-filesystem move, copy, and rename with conflict-safe naming, plus OS-safe path sanitization. | `/plugin install fileflow-pathologize@go-skills` |

## Install

### Claude Code

```text
/plugin marketplace add spf13/go-skills
/plugin install <skill>@go-skills
```

Substitute any skill name from the table above.

### Other agents (Copilot, Cursor, etc.)

Link each skill directory into your agent's skills directory. On Windows, as Administrator:

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.agents\skills\<skill>" -Target "$PWD\<skill>"
```

On macOS and Linux:

```bash
ln -s "$PWD/<skill>" "$HOME/.agents/skills/<skill>"
```

Then restart your editor. The skills appear in the Copilot customizations index and are invoked automatically when relevant Go or CLI work is detected.

## Verify the install

In Claude Code:

```text
/plugin
```

Every installed skill is listed under its namespaced name (`<skill>@go-skills`). Then open a Go project, ask a question the skill covers — for example, "review this interface for idiomatic Go" — and confirm the skill fires.

## Requirements

- Claude Code with plugin and marketplace support (tested on 2.1.94). Other agents read skills from `.agents/skills`.
- No runtime dependencies.

## Why these skills exist

### Another Go project layout guide? No thanks.

As Go has grown in popularity, developers have imported structural baggage from other languages — specifically Java and Spring Boot — and rebranded it as "best practices."

Search for "Go project layout" and you will land on repositories like the notorious `golang-standards/project-layout`. These templates promote deeply nested directories, arbitrary architectural layers (`service/`, `repository/`, `pkg/`), heavy worker pools, and complex mocking frameworks.

Those are not Go patterns. They are Java patterns translated into Go syntax. They fight the language's design. Go was engineered for simplicity, readability, and flat, discoverable APIs. Force a layered, Spring-Boot-style architecture onto Go and you get circular dependencies, obscured control flow, and the loss of the breathtaking simplicity that makes the language worth using.

The problem has gotten worse with LLMs. AI coding assistants are trained on the full corpus of the internet — including all of those misguided "Go best practices" guides. The result is that they confidently generate Java-in-Go-syntax by default, then argue when you push back. These skills exist to correct that: authoritative, first-principles guidance so the model stops reaching for `internal/` junk drawers, BDD frameworks, and static worker pools.

### A course correction

As the creator of Hugo, Cobra, and Viper, and having spent years on the core Go team, I have a good sense of what a well-structured Go codebase looks like — and I am tired of arguing with LLMs trained on Java-style codebases. This playbook saves my sanity.

It strips away the noise and focuses on the architectures the Go standard library and the most successful, high-performance open-source projects actually use. It argues for:

- **Domains over layers.** Delete the `internal/` junk drawer and the `pkg/` anti-pattern. Organize code by what it *does*, not by what kind of file it is.
- **Standard library over frameworks.** Use `testing`, table-driven tests, and simple stubs instead of heavy BDD or mock-generation frameworks.
- **Channels over mutexes.** Use Go's native concurrency primitives for orchestration rather than rigid, static worker pools.
- **Command-first architecture.** Treat your application binary as a router for commands, entirely decoupled from your core business logic.

## The Golden Rule

*Clear is better than clever.* Go code should be boring in the best possible way—predictable, consistent, and immediately understandable to a new developer opening the file for the first time. When in doubt, delete the abstraction.

## License

[MIT](LICENSE)
