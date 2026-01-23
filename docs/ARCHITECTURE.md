# DevPulse Architecture Diagram

## High-Level Flow

```
┌──────────────────────────────────────────────────────────────┐
│                         USER                                  │
│                           │                                   │
│                           ▼                                   │
│                    python devpulse.py                         │
│                           │                                   │
│         ┌─────────────────┴─────────────────┐                │
│         │                                   │                │
│         ▼                                   ▼                │
│    devpulse scan                      devpulse fix           │
└─────────┬───────────────────────────────────┬────────────────┘
          │                                   │
          ▼                                   ▼
┌─────────────────────┐            ┌──────────────────┐
│  core/scanner.py    │            │  core/fixer.py   │
│  ┌───────────────┐  │            │  ┌────────────┐  │
│  │ 1. Collect    │  │            │  │ 1. Check   │  │
│  │    Metadata   │  │            │  │    Results │  │
│  └───────┬───────┘  │            │  └─────┬──────┘  │
│          ▼          │            │        │         │
│  ┌───────────────┐  │            │  ┌─────▼──────┐  │
│  │ 2. Run Checks │  │            │  │ 2. Apply   │  │
│  │    in Parallel│  │            │  │    Fixes   │  │
│  └───────┬───────┘  │            │  └────────────┘  │
│          ▼          │            └──────────────────┘
│  ┌───────────────┐  │
│  │ 3. Aggregate  │  │
│  │    Results    │  │
│  └───────┬───────┘  │
└──────────┼──────────┘
           ▼
┌──────────────────────┐
│  core/reporter.py    │
│  ┌────────────────┐  │
│  │ Format Output  │  │
│  └────────┬───────┘  │
│           ▼          │
│     ┌─────┴─────┐   │
│     │           │   │
│     ▼           ▼   │
│ Terminal      JSON  │
└──────────────────────┘
```

## Scanner Detail

```
┌─────────────────────────────────────────────────────────┐
│                    core/scanner.py                       │
│                                                          │
│  Step 1: Metadata Collection                            │
│  ┌────────────────────────────────────────────────┐     │
│  │  utils/fs.py                                   │     │
│  │  • walk_project()     → Get all files          │     │
│  │  • get_file_size()    → Calculate sizes        │     │
│  │  • get_extensions()   → Collect file types     │     │
│  └────────────────────────────────────────────────┘     │
│                        │                                 │
│                        ▼                                 │
│  Step 2: Independent Checks (run in sequence)           │
│  ┌────────────────┬────────────────┬──────────────┐     │
│  │ checks/        │ checks/        │ checks/      │     │
│  │ stack.py       │ hygiene.py     │ security.py  │     │
│  │                │                │              │     │
│  │ • Detect tech  │ • Check README │ • Scan .env  │     │
│  │   stack from   │ • Check LICENSE│ • Find       │     │
│  │   file         │ • Check        │   secrets    │     │
│  │   patterns     │   .gitignore   │ • Pattern    │     │
│  │                │ • Count TODOs  │   matching   │     │
│  └────────────────┴────────────────┴──────────────┘     │
│                        │                                 │
│                        ▼                                 │
│  Step 3: Result Aggregation                             │
│  ┌────────────────────────────────────────────────┐     │
│  │  Standardized Result Format:                   │     │
│  │  {                                             │     │
│  │    "name": "Check Name",                       │     │
│  │    "status": "ok|info|warning|critical",       │     │
│  │    "details": "Description",                   │     │
│  │    "fixable": true|false,                      │     │
│  │    "data": {...}                               │     │
│  │  }                                             │     │
│  └────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## Check Modules Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    checks/ Directory                      │
│                                                           │
│  ┌─────────────────────────────────────────────────┐     │
│  │ stack.py - Tech Stack Detection                 │     │
│  │ ┌─────────────────────────────────────────────┐ │     │
│  │ │ Patterns:                                   │ │     │
│  │ │ • package.json    → Node.js                 │ │     │
│  │ │ • requirements.txt → Python                 │ │     │
│  │ │ • pom.xml         → Java                    │ │     │
│  │ │ • Dockerfile      → Docker                  │ │     │
│  │ │ • .github/workflows/ → GitHub Actions       │ │     │
│  │ └─────────────────────────────────────────────┘ │     │
│  └─────────────────────────────────────────────────┘     │
│                                                           │
│  ┌─────────────────────────────────────────────────┐     │
│  │ hygiene.py - Repository Hygiene                 │     │
│  │ ┌─────────────────────────────────────────────┐ │     │
│  │ │ Checks:                                     │ │     │
│  │ │ • README.md exists?                         │ │     │
│  │ │ • LICENSE exists?                           │ │     │
│  │ │ • .gitignore exists?                        │ │     │
│  │ │ • Test directory present?                   │ │     │
│  │ │ • Count TODO/FIXME comments                 │ │     │
│  │ └─────────────────────────────────────────────┘ │     │
│  └─────────────────────────────────────────────────┘     │
│                                                           │
│  ┌─────────────────────────────────────────────────┐     │
│  │ security.py - Basic Security Scanning           │     │
│  │ ┌─────────────────────────────────────────────┐ │     │
│  │ │ Patterns:                                   │ │     │
│  │ │ • .env file tracked?                        │ │     │
│  │ │ • API_KEY=...                              │ │     │
│  │ │ • SECRET=...                               │ │     │
│  │ │ • TOKEN=...                                │ │     │
│  │ │ • PASSWORD=...                             │ │     │
│  │ └─────────────────────────────────────────────┘ │     │
│  └─────────────────────────────────────────────────┘     │
│                                                           │
│  ┌─────────────────────────────────────────────────┐     │
│  │ size.py - File Size Analysis                    │     │
│  │ ┌─────────────────────────────────────────────┐ │     │
│  │ │ Analysis:                                   │ │     │
│  │ │ • Find files > 10MB                         │ │     │
│  │ │ • Calculate total project size              │ │     │
│  │ │ • Count files by extension                  │ │     │
│  │ └─────────────────────────────────────────────┘ │     │
│  └─────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────┘
```

## Fixer Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    core/fixer.py                          │
│                                                           │
│  Input: Scan Results                                     │
│  ┌─────────────────────────────────────────────────┐     │
│  │ Filter: result.fixable == true                  │     │
│  └────────────────┬────────────────────────────────┘     │
│                   ▼                                       │
│  ┌─────────────────────────────────────────────────┐     │
│  │ Interactive Mode?                               │     │
│  │ If yes: Ask user for each fix                   │     │
│  │ If no: Apply all fixes automatically            │     │
│  └────────────────┬────────────────────────────────┘     │
│                   ▼                                       │
│  ┌─────────────────────────────────────────────────┐     │
│  │ Apply Fixes:                                    │     │
│  │                                                 │     │
│  │ Missing README?                                 │     │
│  │  → Load templates/README.md                     │     │
│  │  → Replace {project_name}                       │     │
│  │  → Write to project root                        │     │
│  │                                                 │     │
│  │ Missing LICENSE?                                │     │
│  │  → Load templates/LICENSE.txt                   │     │
│  │  → Replace {project_author}                     │     │
│  │  → Write to project root                        │     │
│  │                                                 │     │
│  │ Missing .gitignore?                             │     │
│  │  → Load templates/gitignore.txt                 │     │
│  │  → Write to project root                        │     │
│  └─────────────────────────────────────────────────┘     │
│                                                           │
│  Safety Checks:                                          │
│  • NEVER overwrite existing files                        │
│  • NEVER delete files                                    │
│  • NEVER modify user code                                │
│  • NEVER auto-commit to git                              │
└──────────────────────────────────────────────────────────┘
```

## Reporter Output Flow

```
┌──────────────────────────────────────────────────────────┐
│                   core/reporter.py                        │
│                                                           │
│  Input: Results + Metadata                               │
│                   │                                       │
│                   ▼                                       │
│  ┌──────────────────────────────────────────────┐        │
│  │ Group by Status:                             │        │
│  │ • Critical (🚨)                              │        │
│  │ • Warning (⚠)                                │        │
│  │ • Info (ℹ)                                   │        │
│  │ • OK (✓)                                     │        │
│  └───────────────────┬──────────────────────────┘        │
│                      ▼                                    │
│       ┌──────────────┴──────────────┐                    │
│       │                             │                    │
│       ▼                             ▼                    │
│  Terminal Output              JSON Output                │
│  ┌──────────────────┐        ┌──────────────────┐        │
│  │ ============     │        │ {                │        │
│  │ DevPulse Report │        │   "project": ...,│        │
│  │ ============     │        │   "results": [...│        │
│  │                  │        │   "summary": {   │        │
│  │ Tech Stack:      │        │     "critical": │        │
│  │   ✓ Python       │        │     "warnings": │        │
│  │   ✓ Docker       │        │     "fixable":  │        │
│  │                  │        │   }              │        │
│  │ Warnings:        │        │ }                │        │
│  │   ⚠ Missing...   │        └──────────────────┘        │
│  │                  │                                    │
│  │ Critical:        │                                    │
│  │   🚨 Security... │                                    │
│  │                  │                                    │
│  │ Summary:         │                                    │
│  │   Total: 7       │                                    │
│  │   Critical: 1    │                                    │
│  │   Warnings: 3    │                                    │
│  └──────────────────┘                                    │
└──────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
User Command
    │
    ├─→ "scan" ────────────────────────┐
    │                                  │
    └─→ "fix" ─────────────────┐       │
                               │       │
                               ▼       ▼
                          ┌────────────────┐
                          │ Parse Args     │
                          │ Validate Path  │
                          └────────┬───────┘
                                   │
                 ┌─────────────────┴─────────────────┐
                 │                                   │
                 ▼                                   ▼
        ┌─────────────────┐              ┌──────────────────┐
        │ Scanner         │              │ Fixer            │
        │ • Collect       │              │ • Filter fixable │
        │   metadata      │──results──→  │   issues         │
        │ • Run checks    │              │ • Apply fixes    │
        │ • Aggregate     │              └──────────────────┘
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Reporter        │
        │ • Group results │
        │ • Format output │
        └────────┬────────┘
                 │
         ┌───────┴────────┐
         │                │
         ▼                ▼
    Terminal           JSON
     Output           Output
```

## Module Dependencies

```
devpulse.py
    │
    ├── argparse (stdlib)
    │
    ├── core/
    │   ├── scanner.py
    │   │   ├── utils/fs.py
    │   │   │   └── pathlib, os (stdlib)
    │   │   │
    │   │   └── checks/
    │   │       ├── stack.py
    │   │       ├── hygiene.py
    │   │       ├── security.py
    │   │       └── size.py
    │   │           └── utils/patterns.py
    │   │               └── re (stdlib)
    │   │
    │   ├── reporter.py
    │   │   └── json (stdlib)
    │   │
    │   └── fixer.py
    │       └── pathlib (stdlib)
    │
    └── External Dependencies: NONE ✓
```

## Performance Characteristics

```
┌────────────────────────────────────────────────────┐
│ Project Size    │ Scan Time  │ Memory Usage       │
├─────────────────┼────────────┼────────────────────┤
│ Small (<100)    │ < 0.5s     │ < 10 MB            │
│ Medium (100-1K) │ 0.5-2s     │ 10-30 MB           │
│ Large (1K-10K)  │ 2-5s       │ 30-100 MB          │
│ Very Large (10K+│ 5-15s      │ 100-200 MB         │
└────────────────────────────────────────────────────┘

Key optimizations:
• Single metadata collection (not per-check)
• Ignores common large directories (.git, node_modules)
• Lazy file reading (only when needed)
• Limited output (first N items for large results)
```

---

**Architecture designed for:**
- ✓ **Speed**: Minimal file reads
- ✓ **Safety**: Read-only by default
- ✓ **Simplicity**: Clear module boundaries
- ✓ **Extensibility**: Easy to add new checks
