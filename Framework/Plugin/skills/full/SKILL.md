---
name: full
description: "Run the end-to-end philosophy paper pipeline: start, status, or resume a persisted state machine from intake to citation closure."
disable-model-invocation: true
---

# phil:full

> **Paths.** `<root>` is the nearest ancestor of the working directory containing `Framework/Workflow/manifest.json`; if there is none, stop and report it. `Framework/…` and `Private/…` paths resolve from `<root>`. Bare `Methods/`, `Services/`, `Rules/`, `Schemas/`, `Scripts/`, `Contracts/`, `Commands/`, `References/`, and `Templates/` paths resolve from `<root>/Framework/Workflow/`. Run scripts with `<root>` as the working directory.

Read `Commands/phil-full.md` and execute its state machine with the user's arguments (`start`, `status`, or `resume`). That file is the authoritative contract.
