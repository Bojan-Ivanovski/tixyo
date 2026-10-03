#!/usr/bin/env python3
"""Compatibility entry point for the migrated Tixyo triage command.

Prefer ``tixyo triage ISSUE_NUMBER`` for new usage.
"""

import argparse
import json
from dataclasses import asdict
import os

from tixyo.clients.github import GithubClient
from tixyo.decider.service import DEFAULT_MODEL, TriageService


def main() -> int:
    parser = argparse.ArgumentParser(description="Tixyo GitHub issue triage")
    parser.add_argument("issue_number", type=int)
    parser.add_argument("--repo", default=os.getenv("GITHUB_REPOSITORY"))
    parser.add_argument("--token", default=os.getenv("GITHUB_TOKEN"))
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()

    if not args.repo or not args.token:
        parser.error("set GITHUB_REPOSITORY and GITHUB_TOKEN, or pass --repo and --token")

    result = TriageService(GithubClient(args.token, args.repo), args.model).triage(
        args.issue_number,
        apply=args.apply,
    )
    if args.json_output:
        print(json.dumps(asdict(result), indent=2))
    else:
        print(f"Issue: {result.ticket_title}")
        print(f"Old labels: {result.previous_labels}")
        print(f"New labels: {result.proposed_labels}")
        for warning in result.warnings:
            print(f"WARNING: {warning}")
        print("Applied changes." if result.applied else "DRY RUN: nothing was changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
