# Phase 01 operator tooling

All scripts are offline-first and write runtime data only to a caller-selected
private XDG root. They never install packages, edit the host, capture media, or
write canonical state into this checkout.

Typical clean-clone flow:

    export QUAL_ROOT=\"$HOME/.cache/companion/qualification/COMPANION-P00-QUAL-001\"
    ./scripts/bootstrap.sh
    ./scripts/verify.sh
    python3 scripts/health.py
    python3 scripts/cycle_matrix.py --cycles 1000 --seeds 17,23,41

The target-host floor is explicitly long-running:

    python3 scripts/soak.py --duration-seconds 3600 --interval 60 --output "$XDG_STATE_HOME/companion/phase01-soak.json"

The soak output is sanitized (hashes and counters only) and must stay outside
Git. A bounded visible-window probe is available as `scripts/godot_window_probe.sh`.
