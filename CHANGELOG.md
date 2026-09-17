# Changelog

All notable changes to this catalog are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this catalog adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html). One version covers all six plugins; they move together.

## [1.0.0] - 2026-09-17

### Added

- `go` — idiomatic Go patterns: package design, error handling, interfaces, concurrency, testing, and project layout.
- `cobra-viper` — CLI architecture with Cobra and Viper: command-first design, 12-factor configuration, environment-variable binding, and in-memory CLI testing.
- `go-spec-reviewer` — review a Go design document before implementation begins.
- `go-release` — release engineering: semantic versioning, breaking-change detection, deprecation, `go.mod` hygiene, and GoReleaser.
- `wails` — desktop applications in Go with Wails v2 (stable) and v3 (alpha).
- `fileflow-pathologize` — safe cross-filesystem file operations with `spf13/fileflow` and `spf13/pathologize`.
- Claude Code marketplace support: `/plugin marketplace add spf13/go-skills`.
- `LICENSE` (MIT), `CONTRIBUTING.md`, and a new-skill scaffold under `templates/skill/`.
- CI validating the manifests, the cross-file invariants, and documentation links.

[1.0.0]: https://github.com/spf13/go-skills/releases/tag/v1.0.0
