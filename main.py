#!/usr/bin/env python3
"""Schedule a system shutdown.

Dry-run by default: prints the command that would run. The system is
never shut down unless --confirm is given.
"""
import argparse
import shutil
import subprocess
import sys

VALID_ACTIONS = ("shutdown", "reboot", "cancel")


def build_command(action, delay_minutes, message):
    if action == "cancel":
        return ["shutdown", "-c"]
    cmd = ["shutdown"]
    if action == "reboot":
        cmd.append("-r")
    cmd.append(f"+{delay_minutes}")
    if message:
        cmd.append(message)
    return cmd


def main():
    p = argparse.ArgumentParser(description="Schedule a system shutdown (dry-run by default).")
    p.add_argument("--action", choices=VALID_ACTIONS, default="shutdown",
                   help="shutdown, reboot, or cancel a pending shutdown (default: shutdown)")
    p.add_argument("--in", dest="delay", type=int, default=5,
                   help="Minutes from now to act (default: 5)")
    p.add_argument("--at", help="Clock time instead of a delay, e.g. 23:30 (HH:MM)")
    p.add_argument("--message", help="Message broadcast to logged-in users")
    p.add_argument("--confirm", action="store_true",
                   help="Actually run the shutdown command; without this, only prints it")
    args = p.parse_args()

    if args.action == "cancel":
        delay_arg = None
    elif args.at:
        if not (len(args.at) == 5 and args.at[2] == ":" and
                args.at[:2].isdigit() and args.at[3:].isdigit()):
            p.error("--at must be HH:MM, e.g. 23:30")
        delay_arg = args.at
    else:
        if args.delay < 0:
            p.error("--in must be 0 or more")
        delay_arg = f"+{args.delay}"

    if not shutil.which("shutdown"):
        print("Error: no `shutdown` command found on this system.", file=sys.stderr)
        return 1

    if args.action == "cancel":
        cmd = ["shutdown", "-c"]
    else:
        cmd = ["shutdown"]
        if args.action == "reboot":
            cmd.append("-r")
        cmd.append(delay_arg)
        if args.message:
            cmd.append(args.message)

    when = "now" if args.action == "cancel" else (f"at {args.at}" if args.at else f"in {args.delay} minute(s)")
    print(f"Action: {args.action} {when}")
    print("Command: " + " ".join(cmd))
    if not args.confirm:
        print("\n[DRY RUN] Nothing was scheduled. Re-run with --confirm to actually run this command.")
        print("Note: running it usually requires administrator (sudo/root) privileges.")
        return 0
    print("Running shutdown command (requires admin privileges)...")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: shutdown command failed: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
