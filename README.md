<div align="center">

# Tixyo

**Confidence-gated, model-assisted issue triage for engineering teams.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/tixyo?logo=pypi&logoColor=white)](https://pypi.org/project/tixyo/)
[![Mapika Decider](https://img.shields.io/badge/powered%20by-Mapika%20Decider-6f42c1)](https://huggingface.co/Mapika)
[![GitHub](https://img.shields.io/badge/platform-GitHub-181717?logo=github)](https://github.com/Bojan-Ivanovski/tixyo)

</div>

Tixyo turns incoming issues into structured, reviewable triage decisions. It
reads the issue and recent discussion, classifies it with Mapika Decider, and
proposes consistent labels and ownership without silently changing your
repository.

Dry-run is the default. Changes are only eligible for automatic application
when their probability crosses the configured confidence threshold, and
security-sensitive issues suppress normal automated routing.

## Why Tixyo?

- **Safe by default** — preview every decision before applying it.
- **Confidence gated** — uncertain classifications stay queued for human review.
- **Shared taxonomy** — keep types, components, priorities, statuses, and sizes
  consistent across repositories.
- **Multi-component aware** — one issue can belong to several engineering areas.
- **Provider-oriented design** — the triage engine depends on a common client
  interface, with GitHub as the first implementation.
- **Local model workflow** — classification is powered by Mapika Decider rather
  than a hosted text-generation API.

## What it classifies

| Descriptor | Behavior |
| --- | --- |
| Type | Selects the primary nature of the issue. |
| Component | Selects one or more affected project areas. |
| Priority | Estimates impact and urgency. |
| Status | Proposes the appropriate delivery state. |
| Size | Estimates relative scope and decomposition level. |
| Signals | Detects security, privacy, compliance, missing information, and reproduction needs. |
| Assignee | Proposes an initial owner when confidence is sufficient. |

## Installation

Tixyo requires Python 3.11 or newer. Install the published package with:

```bash
pip install tixyo
```

Or install the latest source version:

```bash
git clone https://github.com/Bojan-Ivanovski/tixyo.git
cd tixyo
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Set the target repository and a GitHub token with issue and label permissions:

```bash
export GITHUB_TOKEN=github_pat_...
export GITHUB_REPOSITORY=owner/repository
```

The first triage run may download and initialize the configured Decider model.

## Quick start

```bash
tixyo triage 123                     # preview decisions
tixyo triage 123 --apply             # apply high-confidence changes
tixyo triage 123 --json              # machine-readable output
tixyo triage 123 --model Mapika/decider-4b
```

## Shared descriptors

The canonical taxonomy lives in `tixyo/data/descriptors.py`. Types and
components can be synchronized with GitHub labels; priority, status, and size
remain static shared definitions.

```bash
tixyo descriptors view
tixyo descriptors view --diff
tixyo descriptors apply
tixyo descriptors apply --force
```

`descriptors apply` adds missing labels and updates mismatched descriptions or
colors. `--force` deletes and recreates mutable type and component labels, so
review the diff before using it on an established repository.

## Safety model

Tixyo separates a model recommendation from permission to mutate a repository:

1. The issue, bounded body text, and recent comments become model context.
2. Decider evaluates closed descriptor choices and independent risk signals.
3. Tixyo parses probabilities and applies confidence thresholds.
4. The CLI prints the proposed label and assignment changes.
5. GitHub is only modified when `--apply` is explicitly provided.

High-confidence security-sensitive results suppress normal label and assignee
updates so maintainers can route them through a private security process.

## Architecture

```text
tixyo/
├── cli/                 Typer commands and presentation
├── clients/             Provider-neutral interfaces
│   └── github/          GitHub transport, tickets, and descriptors
├── data/                Canonical descriptor registry
└── decider/             Context, model adapter, policy, and result models
```

The core `TriageService` accepts the shared `Client` abstraction. Additional
issue trackers can implement the same ticket, descriptor, and transport
interfaces without changing the classifier.

## Development

```bash
pip install -e '.[dev]'
tox -e lint
```

The lint environment runs Pyright, isort, and Black checks.

## Project status

Tixyo is early-stage software. Run it in dry-run mode first, verify your label
taxonomy, and review model recommendations before enabling repository writes.

Contributions, issue reports, and provider integrations are welcome.

## License

Tixyo is available under the [MIT License](LICENSE).
