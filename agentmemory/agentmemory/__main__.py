"""
agentmemory V4 — CLI entry point.

Usage:
    python -m agentmemory serve --port 8000 --db agent.db
    python -m agentmemory mcp --db agent.db
    python -m agentmemory inspect --db agent.db
    python -m agentmemory bench
    python -m agentmemory import --file export.json --db agent.db
    python -m agentmemory export --db agent.db --output backup.json
"""

from __future__ import annotations
import argparse, asyncio, json, sys


def cmd_serve(args):
    from .server import create_app
    import uvicorn
    uvicorn.run(create_app(args.db), host=args.host, port=args.port)

def cmd_mcp(args):
    from .mcp import MCPServer
    asyncio.run(MCPServer(args.db).run_stdio())

def cmd_inspect(args):
    from .core import MemoryStore
    async def _inspect():
        store = MemoryStore(args.db)
        stats = await store.async_stats()
        health = await store.async_health_check()
        drift = await store.async_detect_drift()
        print(f"\n{'='*60}")
        print(f"  agentmemory V4 - Store Inspection")
        print(f"  Database: {args.db}")
        print(f"{'='*60}\n")
        print(f"  Total: {stats['total_memories']} | Active: {stats['active_memories']} "
              f"| Superseded: {stats['superseded']} | Expired: {stats.get('expired',0)}")
        print(f"  Edges: {stats['edges']} | ANN: {stats['ann_index_size']} "
              f"| Embedder: {stats.get('embedder_mode','?')} | Profile: {stats.get('profile','none')}")
        print(f"\n  By Tier:")
        for t, c in stats.get("by_tier", {}).items():
            print(f"    {t:10s} {c:5d} {'#' * min(c, 40)}")
        print(f"\n  Health:")
        print(f"    Contradiction rate:    {health.contradiction_rate:.1%}")
        print(f"    Stale fraction:        {health.stale_memory_fraction:.1%}")
        print(f"    Expired memories:      {health.expired_memories}")
        print(f"    Low quality consol:    {health.low_quality_consolidations}")
        print(f"    Calibration gap:       {health.calibration_gap:.3f}")
        if drift["warnings"]:
            print(f"\n  [!] Warnings:")
            for w in drift["warnings"]:
                print(f"    - {w}")
        else:
            print(f"\n  [OK] Healthy")
        print()
        await store.async_close()
    asyncio.run(_inspect())

def cmd_bench(args):
    from .benchmark import Benchmark
    bench = Benchmark(seed=args.seed)
    sizes = [int(s) for s in args.sizes.split(",")] if args.sizes else None
    for r in bench.run_all(sizes):
        print(r.summary())
        print()

def cmd_import(args):
    from .core import MemoryStore
    from .migration import MigrationImporter
    async def _do():
        store = MemoryStore(args.db)
        count = await MigrationImporter(store).from_file(args.file, format=args.format)
        print(f"Imported {count} memories from {args.file}")
        await store.async_close()
    asyncio.run(_do())

def cmd_export(args):
    from .core import MemoryStore
    from .migration import MigrationExporter
    async def _do():
        store = MemoryStore(args.db)
        await MigrationExporter(store).to_file(args.output, format=args.format)
        print(f"Exported to {args.output}")
        await store.async_close()
    asyncio.run(_do())

def main():
    parser = argparse.ArgumentParser(prog="agentmemory", description="agentmemory V4")
    sub = parser.add_subparsers(dest="command")
    p = sub.add_parser("serve"); p.add_argument("--port", type=int, default=8000)
    p.add_argument("--host", default="0.0.0.0"); p.add_argument("--db", default="agentmemory.db")
    p = sub.add_parser("mcp"); p.add_argument("--db", default="agentmemory.db")
    p = sub.add_parser("inspect"); p.add_argument("--db", default="agentmemory.db")
    p = sub.add_parser("bench"); p.add_argument("--seed", type=int, default=42)
    p.add_argument("--sizes", default=None)
    p = sub.add_parser("import"); p.add_argument("--file", required=True)
    p.add_argument("--format", default="auto"); p.add_argument("--db", default="agentmemory.db")
    p = sub.add_parser("export"); p.add_argument("--output", default="export.json")
    p.add_argument("--format", default="agentmemory"); p.add_argument("--db", default="agentmemory.db")
    args = parser.parse_args()
    cmds = {"serve": cmd_serve, "mcp": cmd_mcp, "inspect": cmd_inspect,
            "bench": cmd_bench, "import": cmd_import, "export": cmd_export}
    if args.command in cmds:
        cmds[args.command](args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
