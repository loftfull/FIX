from __future__ import annotations

import argparse
import json
import os

from host_history_discovery import HostHistoryDiscovery


def _discovery(args):
    env = dict(os.environ)
    if args.claude_root:
        env['CLAUDE_HISTORY_ROOT'] = args.claude_root
    if args.codex_home:
        env['CODEX_HOME'] = args.codex_home
    if args.chatgpt_export:
        env['CHATGPT_CONVERSATIONS_JSON'] = args.chatgpt_export
    return HostHistoryDiscovery(home=args.home, env=env)


def _add_source_args(parser):
    parser.add_argument('--home')
    parser.add_argument('--claude-root')
    parser.add_argument('--codex-home')
    parser.add_argument('--chatgpt-export')


def main() -> int:
    ap = argparse.ArgumentParser(description='Project History Agent v0.7 host-history CLI')
    sub = ap.add_subparsers(dest='cmd', required=True)
    discover = sub.add_parser('discover')
    _add_source_args(discover)
    search = sub.add_parser('search')
    search.add_argument('query')
    search.add_argument('--scope', default='conversations', choices=['conversations','files','plans','sessions','memories','all'])
    search.add_argument('--limit', type=int, default=20)
    _add_source_args(search)
    args = ap.parse_args()
    discovery = _discovery(args)
    report = discovery.discover()
    if args.cmd == 'discover':
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    adapter = discovery.build_adapter(report)
    if adapter is None:
        print(json.dumps({'error':'NO_HISTORY_SOURCE','authority':report['authority'],'sources':report['sources']}, ensure_ascii=False, indent=2))
        return 2
    results = adapter.search(args.scope, args.query, limit=args.limit)
    print(json.dumps({'authority':report['authority'],'scope':args.scope,'query':args.query,'count':len(results),'results':results}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
