#!/usr/bin/env python3
"""Deterministic SHARCK root-only launcher.

Wires existing SHARCK tests/queues and root-only specialist capabilities without
moving code outside the authorized SHARCK root.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve()
SHARCK_ROOT = HERE.parents[2]
CODE_ROOT = SHARCK_ROOT / "📂 input sharck code principal"
ACQ_ROOT = CODE_ROOT / "📂 component acquisition"
QUEUE_ROOT = ACQ_ROOT / "queues"
STATE_ROOT = ACQ_ROOT / "state"
MOTOR_ROOT = SHARCK_ROOT / "📂 motores canónicos copiados"
MOTOR2 = MOTOR_ROOT / "motor_2_queue_download_extract.py"
ENGINE = MOTOR_ROOT / "hf_download_extract_engine.py"\nCASE_ENGINE = SHARCK_ROOT / "📂 motores caso" / "motor_repair_download_extract.py"\nCASE_ENGINE_TEST = SHARCK_ROOT / "📂 motores caso" / "test_motor_repair_download_extract.py"
M59 = CODE_ROOT / "📂 sharck-v3-parallel-candidate"\nM59_ENTRYPOINT = M59 / "sharck_v3_entrypoint.py"\nM59_ENTRYPOINT_TEST = M59 / "test_sharck_v3_entrypoint.py"

TIMESFM = HERE.with_name("timesfm_capability.py")
TIMESFM_TEST = HERE.with_name("test_timesfm_capability.py")

PRESEARCH_ROOT = HERE / "📂 research-prepass-native"
PRESEARCH_ENGINE = PRESEARCH_ROOT / "research_prepass.py"
PRESEARCH_REGISTRY = PRESEARCH_ROOT / "source_registry_no_hf.json"
PRESEARCH_BRIDGE = M59 / "sharck_v3_presearch.py"
PRESEARCH_TESTS = [
    PRESEARCH_ROOT / "test_research_prepass.py",
    PRESEARCH_ROOT / "test_websearch_engine.py",
    M59 / "test_sharck_v3_presearch.py",
]

ALLOWED_PREFIX = SHARCK_ROOT.resolve()


def inside_root(path: Path) -> bool:
    try:
        path.resolve().relative_to(ALLOWED_PREFIX)
        return True
    except ValueError:
        return False


def assert_root_only(*paths: Path) -> None:
    bad = [str(p) for p in paths if not inside_root(p)]
    if bad:
        raise SystemExit(json.dumps({"verdict": "ROOT_SCOPE_VIOLATION", "paths": bad}, ensure_ascii=False))


def verify_root() -> int:
    required = [
        SHARCK_ROOT, CODE_ROOT, QUEUE_ROOT, STATE_ROOT, MOTOR2, ENGINE, M59,
        TIMESFM, TIMESFM_TEST, CASE_ENGINE, CASE_ENGINE_TEST, M59_ENTRYPOINT, M59_ENTRYPOINT_TEST, PRESEARCH_ROOT, PRESEARCH_ENGINE,
        PRESEARCH_REGISTRY, PRESEARCH_BRIDGE, *PRESEARCH_TESTS,
    ]
    assert_root_only(*required)
    missing = [str(p) for p in required if not p.exists()]
    result = {
        "schema": "sharck.root-only-runner.v3",
        "root": str(SHARCK_ROOT),
        "required": [str(p) for p in required],
        "missing": missing,
        "verdict": "PASS" if not missing else "GAP",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not missing else 2


def run_tests(tests: list[Path]) -> int:
    assert_root_only(*tests)
    missing = [str(p) for p in tests if not p.exists()]
    if missing:
        print(json.dumps({"verdict": "GAP", "missing": missing}, ensure_ascii=False))
        return 2
    failed = []
    for test in tests:
        proc = subprocess.run([sys.executable, str(test)], cwd=test.parent)
        if proc.returncode:
            failed.append({"test": test.name, "returncode": proc.returncode})
    print(json.dumps({
        "verdict": "PASS" if not failed else "GAP",
        "tests": [p.name for p in tests],
        "failed": failed,
    }, ensure_ascii=False))
    return 0 if not failed else 2


def test_m59() -> int:
    return run_tests([
        M59 / "test_sharck_v3_runtime.py",
        M59 / "test_provider_adapters.py",
        M59 / "test_sharck_v3_strict.py",
        M59 / "test_sharck_v3_presearch.py",
    ])


def test_presearch() -> int:
    return run_tests(PRESEARCH_TESTS)


def presearch(input_file: str, force: bool) -> int:
    request = Path(input_file)
    if not request.is_absolute():
        request = SHARCK_ROOT / request
    assert_root_only(request, PRESEARCH_ENGINE, PRESEARCH_REGISTRY)
    missing = [str(p) for p in (request, PRESEARCH_ENGINE, PRESEARCH_REGISTRY) if not p.exists()]
    if missing:
        print(json.dumps({"verdict": "GAP", "missing": missing}, ensure_ascii=False))
        return 2
    cmd = [
        sys.executable,
        str(PRESEARCH_ENGINE),
        "--input-file",
        str(request),
        "--registry",
        str(PRESEARCH_REGISTRY),
    ]
    if force:
        cmd.append("--force")
    env = dict(os.environ)
    env.pop("HF_TOKEN", None)
    env.pop("HUGGINGFACE_TOKEN", None)
    return subprocess.call(cmd, cwd=PRESEARCH_ROOT, env=env)


def test_timesfm() -> int:
    assert_root_only(TIMESFM, TIMESFM_TEST)
    if not TIMESFM_TEST.exists():
        print(json.dumps({"verdict": "GAP", "detail": "TimesFM contract test not found"}))
        return 2
    return subprocess.call([sys.executable, str(TIMESFM_TEST)], cwd=TIMESFM_TEST.parent)


def timesfm(input_file: str, execute: bool) -> int:
    request = Path(input_file)
    if not request.is_absolute():
        request = SHARCK_ROOT / request
    assert_root_only(request, TIMESFM)
    missing = [str(p) for p in (request, TIMESFM) if not p.exists()]
    if missing:
        print(json.dumps({"verdict": "GAP", "missing": missing}, ensure_ascii=False))
        return 2
    cmd = [sys.executable, str(TIMESFM), "--input", str(request)]
    if execute:
        cmd.append("--execute")
    return subprocess.call(cmd, cwd=SHARCK_ROOT)


def motor2_repair(queue_name: str, execute: bool) -> int:
    if Path(queue_name).name != queue_name:
        raise SystemExit("queue must be a filename inside the SHARCK queue directory")
    queue = QUEUE_ROOT / queue_name
    stem = queue.stem
    state = STATE_ROOT / f"{stem}-state.json"
    index = STATE_ROOT / f"{stem}-INDEX.md"
    assert_root_only(queue, state, index, MOTOR2, ENGINE, CASE_ENGINE)
    missing = [str(p) for p in (queue, MOTOR2, ENGINE, CASE_ENGINE) if not p.exists()]
    if missing:
        print(json.dumps({"verdict": "GAP", "missing": missing}, ensure_ascii=False))
        return 2
    plan = {
        "schema": "sharck.root-only-motor2-case-repair-plan.v1",
        "queue": str(queue),
        "state": str(state),
        "index": str(index),
        "motor": str(MOTOR2),
        "canonical_engine": str(ENGINE),
        "case_engine": str(CASE_ENGINE),
        "repair_existing": True,
        "github_actions": False,
        "huggingface_jobs": False,
        "execute": execute,
    }
    if not execute:
        print(json.dumps({**plan, "verdict": "PLAN_ONLY"}, ensure_ascii=False, indent=2))
        return 0
    env = dict(os.environ)
    env.update({
        "QUEUE_FILE": str(queue),
        "STATE_FILE": str(state),
        "INDEX_PATH": str(index),
        "ENGINE_PATH": str(CASE_ENGINE),
        "CANONICAL_ENGINE_PATH": str(ENGINE),
        "REPAIR_EXISTING": "1",
    })
    return subprocess.call([sys.executable, str(MOTOR2)], cwd=SHARCK_ROOT, env=env)


def motor2(queue_name: str, execute: bool) -> int:
    if Path(queue_name).name != queue_name:
        raise SystemExit("queue must be a filename inside the SHARCK queue directory")
    queue = QUEUE_ROOT / queue_name
    stem = queue.stem
    state = STATE_ROOT / f"{stem}-state.json"
    index = STATE_ROOT / f"{stem}-INDEX.md"
    assert_root_only(queue, state, index, MOTOR2, ENGINE)
    missing = [str(p) for p in (queue, MOTOR2, ENGINE) if not p.exists()]
    if missing:
        print(json.dumps({"verdict": "GAP", "missing": missing}, ensure_ascii=False))
        return 2
    plan = {
        "schema": "sharck.root-only-motor2-plan.v1",
        "queue": str(queue),
        "state": str(state),
        "index": str(index),
        "motor": str(MOTOR2),
        "engine": str(ENGINE),
        "execute": execute,
    }
    if not execute:
        print(json.dumps({**plan, "verdict": "PLAN_ONLY"}, ensure_ascii=False, indent=2))
        return 0
    env = dict(os.environ)
    env.update({
        "QUEUE_FILE": str(queue),
        "STATE_FILE": str(state),
        "INDEX_PATH": str(index),
        "ENGINE_PATH": str(ENGINE),
    })
    return subprocess.call([sys.executable, str(MOTOR2)], cwd=SHARCK_ROOT, env=env)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("verify-root")
    sub.add_parser("test-m59")
    sub.add_parser("test-presearch")\n    sub.add_parser("test-repair-motor")
    sub.add_parser("test-timesfm")

    p_presearch = sub.add_parser("presearch")
    p_presearch.add_argument("--input", required=True, help="Literal input file inside the authorized SHARCK root")
    p_presearch.add_argument("--force", action="store_true", help="Bypass research-prepass cache; still uses NO_HF registry.")

    p_timesfm = sub.add_parser("timesfm")
    p_timesfm.add_argument("--input", required=True, help="JSON request file inside the authorized SHARCK root")
    p_timesfm.add_argument("--execute", action="store_true", help="Run TimesFM 3. Default is PLAN_ONLY.")

    p_repair = sub.add_parser("motor2-repair")
    p_repair.add_argument("--queue", required=True)
    p_repair.add_argument("--execute", action="store_true", help="Execute canonical Motor 2 through the additive case-repair engine.")

    p_motor = sub.add_parser("motor2")
    p_motor.add_argument("--queue", required=True)
    p_motor.add_argument("--execute", action="store_true", help="Actually invoke Motor 2. Without this flag only emit a root-only plan.")

    args = parser.parse_args()
    if args.cmd == "verify-root":
        return verify_root()
    if args.cmd == "test-m59":
        return test_m59()
    if args.cmd == "test-presearch":
        return test_presearch()
    if args.cmd == "presearch":
        return presearch(args.input, args.force)
    if args.cmd == "test-timesfm":
        return test_timesfm()
    if args.cmd == "timesfm":
        return timesfm(args.input, args.execute)
    if args.cmd == "motor2-repair":
        return motor2_repair(args.queue, args.execute)
    if args.cmd == "motor2":
        return motor2(args.queue, args.execute)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
