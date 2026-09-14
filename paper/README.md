# Paper about the Kourovka experiment

This directory contains the later manuscript project. The experiment itself
is frozen at `cff2c37b9bf6b737e8ad5f7ead12291a551b5201`.
The full requested scope and review requirements are in [PLAN.md](PLAN.md).
The paper is under construction; [STATUS.md](STATUS.md) records progress.

Reproduce the session and Git measurements from the supplied session files:

```sh
python3 paper/scripts/analyze_experiment.py
python3 paper/scripts/analyze_experiment.py --check
```

The analyzer uses only Python's standard library and Git. It never executes
a mathematical verifier or contacts the network. It reads the retained
export rather than treating its advertised event total as a complete log.
The generated data include exact cumulative counters, their ambiguities,
commit dates, and the first appearance of principal proof artifacts.

`data/author-metadata.json` separates user-supplied metadata from measurements.
Raw `session/` exports remain outside this manuscript's tracked files;
their byte sizes and SHA-256 digests are recorded in the generated data.
The visible-message projection excludes directives and hidden/internal
content. No manuscript submission or repository push is performed here.
