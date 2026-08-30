"""
End-to-end auto-learn demo: DevOps incident resolution.

Demonstrates the full Acontext learning cycle in two acts:
  Act 1 — Agent diagnoses a 502 gateway error using mock DevOps tools.
          Session is recorded and a skill (SOP) is auto-generated.
  Act 2 — A similar incident occurs. The agent recalls the learned SOP
          via SKILL_TOOLS and resolves the issue with fewer tool calls.

Requires: ACONTEXT_API_KEY, OPENAI_API_KEY
"""

from __future__ import annotations

import json
import os
import sys
import time
from copy import deepcopy
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from openai import OpenAI

from acontext import AcontextClient
from acontext.agent.skill import SKILL_TOOLS

# ---------------------------------------------------------------------------
# Mock DevOps environment
# ---------------------------------------------------------------------------

ACT1_ENV: dict[str, Any] = {
    "services": {
        "api-gateway": {
            "status": "unhealthy",
            "error_rate_pct": 34,
            "p99_latency_ms": 55,
            "type": "reverse-proxy",
        },
        "auth-service": {
            "status": "healthy",
            "error_rate_pct": 0,
            "p99_latency_ms": 85,
            "type": "application",
        },
        "backend-api": {
            "status": "healthy",
            "error_rate_pct": 0,
            "p99_latency_ms": 4200,
            "type": "application",
        },
        "notification-service": {
            "status": "degraded",
            "error_rate_pct": 5,
            "p99_latency_ms": 320,
            "type": "application",
        },
        "redis-cache": {
            "status": "healthy",
            "error_rate_pct": 0,
            "p99_latency_ms": 3,
            "type": "cache",
        },
        "user-db": {
            "status": "healthy",
            "error_rate_pct": 0,
            "connections_active": 45,
            "type": "database",
        },
    },
    "configs": {
        "api-gateway": {
            "upstream_timeout_ms": 5000,
            "max_retries": 3,
            "routes": {
                "/api/*": "http://backend-api:8080",
                "/auth/*": "http://auth-service:8080",
                "/notifications/*": "http://notification-service:8080",
            },
        },
    },
    "logs": {
        "api-gateway": [
            "[2026-03-26 09:12:03] ERROR  502 Bad Gateway returned to client  path=/api/orders  upstream=backend-api",
            "[2026-03-26 09:12:01] ERROR  502 Bad Gateway returned to client  path=/api/users  upstream=backend-api",
            "[2026-03-26 09:11:59] WARN   upstream response slow  service=backend-api  duration=4850ms",
            "[2026-03-26 09:11:58] WARN   retrying upstream request  attempt=3  service=backend-api",
            "[2026-03-26 09:11:55] ERROR  upstream health check failed  service=notification-service  consecutive_failures=5",
            "[2026-03-26 09:11:52] ERROR  502 Bad Gateway returned to client  path=/api/users  upstream=backend-api",
            "[2026-03-26 09:11:50] WARN   retrying upstream request  attempt=2  service=backend-api",
            "[2026-03-26 09:11:48] INFO   health check passed  service=auth-service  latency=80ms",
            "[2026-03-26 09:11:45] INFO   health check passed  service=redis-cache  latency=2ms",
        ],
        "auth-service": [
            "[2026-03-26 09:12:00] INFO   request completed  path=/auth/verify  duration=78ms",
            "[2026-03-26 09:11:55] INFO   token refresh  user=u-1234  duration=65ms",
        ],
        "backend-api": [
            "[2026-03-26 09:12:00] INFO   request completed  path=/api/users  duration=4150ms",
            "[2026-03-26 09:11:55] INFO   request completed  path=/api/orders  duration=4890ms",
            "[2026-03-26 09:11:50] WARN   DB query slow  table=orders  duration=3200ms",
            "[2026-03-26 09:11:45] INFO   request completed  path=/api/users  duration=3950ms",
        ],
        "notification-service": [
            "[2026-03-26 09:11:55] ERROR  SMTP relay connection refused  host=smtp.internal  retrying in 30s",
            "[2026-03-26 09:11:50] WARN   message queue backlog  depth=1240  oldest=45s",
            "[2026-03-26 09:11:45] ERROR  failed to deliver notification  channel=email  error=connection_refused",
        ],
        "redis-cache": [
            "[2026-03-26 09:12:00] INFO   keyspace hits=12450  misses=23",
        ],
    },
}

ACT2_ENV: dict[str, Any] = {
    "services": {
        "api-gateway": {
            "status": "unhealthy",
            "error_rate_pct": 22,
            "p99_latency_ms": 60,
            "type": "reverse-proxy",
        },
        "auth-service": {
            "status": "healthy",
            "error_rate_pct": 0,
            "p99_latency_ms": 90,
            "type": "application",
        },
        "backend-api": {
            "status": "healthy",
            "error_rate_pct": 0,
            "p99_latency_ms": 120,
            "type": "application",
        },
        "payment-service": {
            "status": "healthy",
            "error_rate_pct": 0,
            "p99_latency_ms": 45000,
            "type": "application",
        },
        "notification-service": {
            "status": "healthy",
            "error_rate_pct": 0,
            "p99_latency_ms": 200,
            "type": "application",
        },
        "redis-cache": {
            "status": "healthy",
            "error_rate_pct": 0,
            "p99_latency_ms": 3,
            "type": "cache",
        },
        "user-db": {
            "status": "healthy",
            "error_rate_pct": 0,
            "connections_active": 52,
            "type": "database",
        },
    },
    "configs": {
        "api-gateway": {
            "upstream_timeout_ms": 30000,
            "max_retries": 3,
            "routes": {
                "/api/*": "http://backend-api:8080",
                "/auth/*": "http://auth-service:8080",
                "/notifications/*": "http://notification-service:8080",
                "/payments/*": "http://payment-service:8080",
            },
        },
    },
    "logs": {
        "api-gateway": [
            "[2026-03-26 14:30:12] ERROR  upstream timeout: payment-service did not respond within 30000 ms",
            "[2026-03-26 14:30:12] ERROR  502 Bad Gateway returned to client  path=/payments/checkout",
            "[2026-03-26 14:30:10] ERROR  upstream timeout: payment-service did not respond within 30000 ms",
            "[2026-03-26 14:30:10] ERROR  502 Bad Gateway returned to client  path=/payments/refund",
            "[2026-03-26 14:30:05] WARN   retrying upstream request  attempt=3  service=payment-service",
            "[2026-03-26 14:30:00] INFO   health check passed  service=backend-api  latency=110ms",
            "[2026-03-26 14:29:58] INFO   health check passed  service=auth-service  latency=85ms",
        ],
        "payment-service": [
            "[2026-03-26 14:30:11] INFO   request completed  path=/payments/checkout  duration=44200ms",
            "[2026-03-26 14:30:05] INFO   request completed  path=/payments/refund  duration=42800ms",
            "[2026-03-26 14:29:50] WARN   external payment gateway slow  provider=stripe  duration=41000ms",
        ],
    },
}


def _exec_mock_tool(env: dict[str, Any], name: str, args: dict) -> str:
    """Execute a mock DevOps tool against the in-memory environment."""
    if name == "check_service_status":
        svc = args.get("service_name", "")
        info = env["services"].get(svc)
        if not info:
            available = ", ".join(env["services"])
            return f"Service '{svc}' not found. Available: {available}"
        lines = [f"Service: {svc}"]
        for k, v in info.items():
            lines.append(f"  {k}: {v}")
        return "\n".join(lines)

    if name == "check_logs":
        svc = args.get("service_name", "")
        n = min(int(args.get("lines", 10)), 20)
        entries = env["logs"].get(svc, [])
        if not entries:
            return f"No logs found for '{svc}'."
        return "\n".join(entries[:n])

    if name == "read_config":
        svc = args.get("service_name", "")
        cfg = env["configs"].get(svc)
        if not cfg:
            return f"No config found for '{svc}'."
        return json.dumps(cfg, indent=2)

    if name == "update_config":
        svc = args.get("service_name", "")
        key = args.get("key", "")
        value = args.get("value", "")
        cfg = env["configs"].get(svc)
        if not cfg:
            return f"No config found for '{svc}'."
        try:
            value = int(value)
        except (ValueError, TypeError):
            pass
        cfg[key] = value
        return f"Updated {svc} config: {key} = {value}"

    if name == "restart_service":
        svc = args.get("service_name", "")
        info = env["services"].get(svc)
        if not info:
            return f"Service '{svc}' not found."
        info["status"] = "healthy"
        info["error_rate_pct"] = 0
        return f"Service '{svc}' restarted successfully. Status: healthy"

    return f"Unknown tool: {name}"


MOCK_TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "check_service_status",
            "description": "Check the health status, error rate, and latency of a service.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service to check.",
                    },
                },
                "required": ["service_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_logs",
            "description": "Retrieve recent log entries for a service.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service.",
                    },
                    "lines": {
                        "type": "integer",
                        "description": "Number of recent log lines to retrieve (max 20).",
                    },
                },
                "required": ["service_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_config",
            "description": "Read the current configuration of a service.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service.",
                    },
                },
                "required": ["service_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "update_config",
            "description": "Update a configuration value for a service.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service.",
                    },
                    "key": {
                        "type": "string",
                        "description": "Configuration key to update.",
                    },
                    "value": {
                        "type": "string",
                        "description": "New value for the configuration key.",
                    },
                },
                "required": ["service_name", "key", "value"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "restart_service",
            "description": "Restart a service to apply configuration changes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service_name": {
                        "type": "string",
                        "description": "Name of the service to restart.",
                    },
                },
                "required": ["service_name"],
            },
        },
    },
]

MOCK_TOOL_NAMES = {t["function"]["name"] for t in MOCK_TOOL_SCHEMAS}

# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are a DevOps incident response agent with full authority to make changes. "
    "Diagnose the root cause, apply the fix immediately, and verify it works. "
    "Act autonomously — never ask for permission or confirmation. "
    "Complete the full resolution cycle: diagnose → fix → verify."
)


def run_agent(
    openai_client: OpenAI,
    acontext_client: AcontextClient,
    session_id: str,
    env: dict[str, Any],
    user_message: str,
    extra_system: str = "",
    extra_tools: list[dict] | None = None,
    skill_ctx=None,
) -> int:
    """Run the OpenAI agent loop, recording messages to Acontext.

    Returns the number of mock DevOps tool calls made (excludes skill tool calls).
    """
    system = SYSTEM_PROMPT
    if extra_system:
        system += "\n\n" + extra_system

    tools = list(MOCK_TOOL_SCHEMAS)
    if extra_tools:
        tools.extend(extra_tools)

    messages: list[dict] = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_message},
    ]

    acontext_client.sessions.store_message(
        session_id, blob={"role": "user", "content": user_message}
    )

    devops_tool_count = 0
    max_iterations = 15

    for _ in range(max_iterations):
        response = openai_client.chat.completions.create(
            model="gpt-4.1", messages=messages, tools=tools
        )
        msg = response.choices[0].message

        if msg.tool_calls:
            assistant_blob: dict[str, Any] = {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ],
            }
            if msg.content:
                assistant_blob["content"] = msg.content
        else:
            assistant_blob = {"role": "assistant", "content": msg.content or ""}
        messages.append(assistant_blob)
        acontext_client.sessions.store_message(session_id, blob=assistant_blob)

        if not msg.tool_calls:
            print(f"  Agent: {msg.content}")
            break

        for tc in msg.tool_calls:
            fn_name = tc.function.name
            fn_args = json.loads(tc.function.arguments)

            if fn_name in MOCK_TOOL_NAMES:
                result = _exec_mock_tool(env, fn_name, fn_args)
                devops_tool_count += 1
                label = ", ".join(f"{k}={v}" for k, v in fn_args.items())
                print(f"    → {fn_name}({label})")
            elif skill_ctx and SKILL_TOOLS.tool_exists(fn_name):
                result = SKILL_TOOLS.execute_tool(skill_ctx, fn_name, fn_args)
                skill_name = fn_args.get("skill_name", fn_args.get("file_path", fn_name))
                print(f"    ★ {fn_name}({skill_name})")
            else:
                result = f"Unknown tool: {fn_name}"

            tool_msg = {"role": "tool", "tool_call_id": tc.id, "content": result}
            messages.append(tool_msg)
            acontext_client.sessions.store_message(session_id, blob=tool_msg)

    return devops_tool_count


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def banner(title: str) -> None:
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def wait_for_tasks(client: AcontextClient, session_id: str, timeout: int = 90) -> list:
    """Poll until task processing completes."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        status = client.sessions.messages_observing_status(session_id)
        if status.pending == 0 and status.in_process == 0:
            break
        time.sleep(2)
    return client.sessions.get_tasks(session_id).items


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    ac = AcontextClient(
        api_key=os.environ["ACONTEXT_API_KEY"],
        base_url=os.getenv("ACONTEXT_BASE_URL"),
    )
    oai = OpenAI()

    # ── Act 1: Learning Run ──────────────────────────────────────────────

    banner("ACT 1 — Learning Run: Diagnose 502 errors")

    space = ac.learning_spaces.create()
    session1 = ac.sessions.create()
    ac.learning_spaces.learn(space.id, session_id=session1.id)

    env1 = deepcopy(ACT1_ENV)
    act1_tools = run_agent(
        oai, ac, session1.id, env1,
        user_message=(
            "Our API gateway is returning 502 errors on /api/* routes — "
            "about 34% of requests are failing. "
            "Diagnose the root cause and fix it."
        ),
    )

    # Wait for task extraction
    print("\n  Waiting for task extraction...")
    ac.sessions.flush(session1.id)
    tasks = wait_for_tasks(ac, session1.id)
    print(f"  Extracted {len(tasks)} task(s):")
    for t in tasks:
        print(f"    [{t.status}] {t.data.task_description}")

    # Wait for skill learning
    print("\n  Waiting for skill learning pipeline...")
    result = ac.learning_spaces.wait_for_learning(
        space.id, session_id=session1.id, timeout=180
    )
    print(f"  Learning status: {result.status}")

    # Download generated skills to local directory
    skills = ac.learning_spaces.list_skills(space.id)
    out_dir = Path(__file__).parent / "learned_skills"
    out_dir.mkdir(exist_ok=True)
    print(f"\n  Generated {len(skills)} skill(s) — downloading to {out_dir}/")
    for s in skills:
        skill_dir = out_dir / s.name
        skill_dir.mkdir(exist_ok=True)
        for f in s.file_index:
            content = ac.skills.get_file(skill_id=s.id, file_path=f.path)
            if content.content:
                (skill_dir / f.path).write_text(content.content.raw)
        print(f"    • {s.name}: {s.description}")

    # ── Act 2: Recall Run ────────────────────────────────────────────────

    banner("ACT 2 — Recall Run: New 502 incident (with learned skills)")

    session2 = ac.sessions.create()
    ac.learning_spaces.learn(space.id, session_id=session2.id)

    skill_ids = [s.id for s in skills]
    skill_ctx = SKILL_TOOLS.format_context(ac, skill_ids)
    skill_tools_schema = SKILL_TOOLS.to_openai_tool_schema()

    env2 = deepcopy(ACT2_ENV)
    act2_tools = run_agent(
        oai, ac, session2.id, env2,
        user_message=(
            "The API gateway started returning 502 errors again after today's deployment. "
            "About 22% of requests are failing. Please diagnose and fix."
        ),
        extra_system=(
            "You have access to skills learned from previous incidents. "
            "ALWAYS check your skills first before starting diagnosis.\n\n"
            + skill_ctx.get_context_prompt()
        ),
        extra_tools=skill_tools_schema,
        skill_ctx=skill_ctx,
    )

    # ── Summary ──────────────────────────────────────────────────────────

    banner("RESULTS")
    print(f"  Act 1 (no prior knowledge):  {act1_tools} tool calls")
    print(f"  Act 2 (with learned skills): {act2_tools} tool calls")
    if act2_tools < act1_tools:
        pct = round((1 - act2_tools / act1_tools) * 100)
        print(f"  → {pct}% fewer tool calls with learned skills")
    elif act2_tools == act1_tools:
        print("  → Same number of tool calls")
    else:
        print("  → Act 2 used more calls (LLM variance)")
    print(f"\n  Skills saved to: {out_dir}/")

    # Cleanup remote resources
    ac.sessions.delete(session1.id)
    ac.sessions.delete(session2.id)
    ac.learning_spaces.delete(space.id)
    for s in skills:
        ac.skills.delete(s.id)
    print("  Cleaned up remote sessions, learning space, and skills.")


if __name__ == "__main__":
    main()
