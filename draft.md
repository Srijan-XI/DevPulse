# DevPulse 
## Working Framework & Workflow
1️⃣ Core Philosophy (lock this in first)

DevPulse is:

- Local-first
- Read-only by default
- Zero configuration
- Fast (seconds, not minutes)

DevPulse is NOT:

- A replacement for GitHub Actions
- A deep security scanner
- A CI/CD tool

Everything else follows from this.

2️⃣ Recommended Tech Stack (minimal & honest)
Language

**Python 3.10+**

Why:

- **Cross-platform**
- **Great filesystem APIs**
- **Copilot CLI writes Python very well**
- **Easy to maintain and extend**
- **CLI Framework**
argparse (standard library)

Why:

No external dependency

Shows real CLI engineering

Easy for Copilot to reason about

(You can use typer, but standard lib looks more serious in a challenge.)

Optional libs (only if needed)
Purpose	Library
Colored output	rich (optional)
File type detection	pathlib
Regex scanning	re

Keep dependencies minimal — judges like that.

3️⃣ High-level Workflow (mental model)
User runs devpulse →
  Parse arguments →
    Scan project directory →
      Run independent checks →
        Aggregate results →
          Print human-readable report →
            (Optional) apply safe fixes


Simple, linear, debuggable.

4️⃣ CLI Commands Design
`Primary commands`
```
devpulse scan
devpulse scan --json
devpulse fix --safe
devpulse fix --interactive
```

Flags
`Flag	Meaning`
```
--path	Custom project directory
--json	Machine-readable output
--safe	Only non-destructive fixes
--interactive	Ask before changes
```
5️⃣ Internal Module Structure (important)
```
cli/
├── devpulse.py          # CLI entry point
├── core/
│   ├── scanner.py       # Orchestrates all checks
│   ├── reporter.py     # Formats output
│   └── fixer.py        # Applies fixes
├── checks/
│   ├── stack.py        # Tech stack detection
│   ├── hygiene.py      # Repo hygiene
│   ├── security.py     # Local secret scanning
│   └── size.py         # Large file detection
├── templates/
│   ├── README.md
│   ├── gitignore.txt
│   └── LICENSE.txt
└── utils/
    ├── fs.py
    └── patterns.py

```

This is small but professionally structured.

6️⃣ Step-by-step Execution Workflow
Step 1: Argument parsing

Read command
```
Resolve path (default = .)

Decide mode: scan / fix

User intent → CLI → internal config object
```
Step 2: Project scan

Scanner walks directory:
```
Ignores .git/, node_modules/, venv/
```
Collects metadata:

`file list`
`size info`
`extensions`

This data is reused by all checks (important for performance).

Step 3: Run checks (independent & composable)

Each check returns:
```

{
  "name": "Missing README",
  "status": "warning",
  "details": "README.md not found"
}
```
a) Stack detection

Looks for:
```
package.json → Node

requirements.txt / pyproject.toml → Python

Dockerfile

.github/workflows/
```
b) Hygiene checks
```
README exists?

.gitignore exists?

LICENSE exists?

tests directory present?
```
c) Security checks (basic, not fake)
```
.env tracked?

Regex match for:

API_KEY=

SECRET=

TOKEN=

Warn only (no false authority)
```
d) File hygiene
```
Files > 10MB

TODO / FIXME count

Orphan files (not referenced)
```
Step 4: Aggregate results

Results grouped by severity:

✅ OK

⚠️ Warning

🚨 Critical

This makes output readable.

Step 5: Reporting
```
Terminal output:

DevPulse Report — ./my-project

Tech Stack:
  ✔ Node.js
  ✔ Docker

Warnings:
  ⚠ Missing README.md
  ⚠ No LICENSE file

Critical:
  🚨 .env file tracked by git

```
Optional:
```
devpulse scan --json > report.json
```
Step 6: Fix workflow (safe by default)
```
devpulse fix --safe:

Generates README from template

Adds .gitignore

Adds MIT license

❗ NEVER:

delete files

modify user code

auto-commit

This keeps trust.
```
