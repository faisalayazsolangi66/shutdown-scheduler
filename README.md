# Shutdown Scheduler

Schedule a system shutdown (or reboot, or cancel a pending shutdown).

## Safety

**Dry-run by default.** The tool prints the `shutdown` command it would
run and does nothing. The system is never shut down unless you pass
`--confirm`. Running it for real usually requires administrator
(sudo/root) privileges.

## Requirements

- Python 3.8+
- Standard library only — no third-party packages
- Linux with the `shutdown` command

## Usage

```bash
python3 main.py --in 10
python3 main.py --at 23:30 --message "Nightly shutdown"
python3 main.py --action reboot --in 5
python3 main.py --action cancel
python3 main.py --in 10 --confirm   # actually schedules the shutdown
```

## Example

```bash
$ python3 main.py --in 10
Action: shutdown in 10 minute(s)
Command: shutdown +10

[DRY RUN] Nothing was scheduled. Re-run with --confirm to actually run this command.
Note: running it usually requires administrator (sudo/root) privileges.
```

## License

MIT — see [LICENSE](LICENSE).
