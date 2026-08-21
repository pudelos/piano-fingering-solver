# Piano Fingering Solver

Automatic generator of piano fingerings based on MusicXML files.

## Input assumptions

- one MusicXML part
- one monophonic melodic line
- no chords or overlapping notes

## Current status

- [x] MusicXML importer
- [ ] Fingering solver
- [x] MusicXML exporter

## Development

Install dependencies:

```bash
uv sync
```

Run linting:

```bash
uv run ruff check .
```

Run tests:

```bash
uv run pytest
```
