from __future__ import annotations

import argparse
import json
import sys

from .exporters import export_authorities
from .indexing import AuthorityIndexer


def build_parser(default_command: str | None = None) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HOOD-LAW authority tooling")
    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser("index", help="Index authority markdown files")
    index_parser.add_argument("--input", required=True, help="Directory containing markdown authority files")

    export_parser = subparsers.add_parser("export", help="Export authority markdown files to JSON")
    export_parser.add_argument("--input", required=True, help="Directory containing markdown authority files")
    export_parser.add_argument("--output", help="Destination JSON file")
    return parser


def main(argv: list[str] | None = None, default_command: str | None = None) -> int:
    args_list = list(sys.argv[1:] if argv is None else argv)
    if default_command and (not args_list or args_list[0] not in {"index", "export"}):
        args_list = [default_command, *args_list]

    parser = build_parser(default_command=default_command)
    args = parser.parse_args(args_list)
    indexer = AuthorityIndexer()

    if args.command == "index":
        authority_index = indexer.index_directory(args.input)
        print(json.dumps(authority_index.to_dict(), indent=2))
        return 0

    if args.command == "export":
        authority_index = indexer.index_directory(args.input)
        payload = export_authorities(authority_index, output_path=args.output)
        print(json.dumps(payload, indent=2))
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2


def index_main() -> int:
    return main(default_command="index")


def export_main() -> int:
    return main(default_command="export")
