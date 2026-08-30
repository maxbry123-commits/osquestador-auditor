/**
 * End-to-end auto-learn demo: DevOps incident resolution.
 *
 * Demonstrates the full Acontext learning cycle in two acts:
 *   Act 1 — Agent diagnoses a 502 gateway error using mock DevOps tools.
 *           Session is recorded and a skill (SOP) is auto-generated.
 *   Act 2 — A similar incident occurs. The agent recalls the learned SOP
 *           via SKILL_TOOLS and resolves the issue with fewer tool calls.
 *
 * Requires: ACONTEXT_API_KEY, OPENAI_API_KEY
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import { AcontextClient } from '../src';
import { SKILL_TOOLS, SkillContext } from '../src/agent/skill';
import OpenAI from 'openai';

// ---------------------------------------------------------------------------
// Mock DevOps environment
// ---------------------------------------------------------------------------

interface ServiceInfo {
  status: string;
  error_rate_pct: number;
  p99_latency_ms?: number;
  connections_active?: number;
  type: string;
}

interface MockEnv {
  services: Record<string, ServiceInfo>;
  configs: Record<string, Record<string, unknown>>;
  logs: Record<string, string[]>;
}

function createAct1Env(): MockEnv {
  return {
    services: {
      'api-gateway': { status: 'unhealthy', error_rate_pct: 34, p99_latency_ms: 55, type: 'reverse-proxy' },
      'auth-service': { status: 'healthy', error_rate_pct: 0, p99_latency_ms: 85, type: 'application' },
      'backend-api': { status: 'healthy', error_rate_pct: 0, p99_latency_ms: 4200, type: 'application' },
      'notification-service': { status: 'degraded', error_rate_pct: 5, p99_latency_ms: 320, type: 'application' },
      'redis-cache': { status: 'healthy', error_rate_pct: 0, p99_latency_ms: 3, type: 'cache' },
      'user-db': { status: 'healthy', error_rate_pct: 0, connections_active: 45, type: 'database' },
    },
    configs: {
      'api-gateway': {
        upstream_timeout_ms: 5000, max_retries: 3,
        routes: { '/api/*': 'http://backend-api:8080', '/auth/*': 'http://auth-service:8080', '/notifications/*': 'http://notification-service:8080' },
      },
    },
    logs: {
      'api-gateway': [
        '[2026-03-26 09:12:03] ERROR  502 Bad Gateway returned to client  path=/api/orders  upstream=backend-api',
        '[2026-03-26 09:12:01] ERROR  502 Bad Gateway returned to client  path=/api/users  upstream=backend-api',
        '[2026-03-26 09:11:59] WARN   upstream response slow  service=backend-api  duration=4850ms',
        '[2026-03-26 09:11:58] WARN   retrying upstream request  attempt=3  service=backend-api',
        '[2026-03-26 09:11:55] ERROR  upstream health check failed  service=notification-service  consecutive_failures=5',
        '[2026-03-26 09:11:52] ERROR  502 Bad Gateway returned to client  path=/api/users  upstream=backend-api',
        '[2026-03-26 09:11:50] WARN   retrying upstream request  attempt=2  service=backend-api',
        '[2026-03-26 09:11:48] INFO   health check passed  service=auth-service  latency=80ms',
        '[2026-03-26 09:11:45] INFO   health check passed  service=redis-cache  latency=2ms',
      ],
      'auth-service': [
        '[2026-03-26 09:12:00] INFO   request completed  path=/auth/verify  duration=78ms',
      ],
      'backend-api': [
        '[2026-03-26 09:12:00] INFO   request completed  path=/api/users  duration=4150ms',
        '[2026-03-26 09:11:55] INFO   request completed  path=/api/orders  duration=4890ms',
        '[2026-03-26 09:11:50] WARN   DB query slow  table=orders  duration=3200ms',
      ],
      'notification-service': [
        '[2026-03-26 09:11:55] ERROR  SMTP relay connection refused  host=smtp.internal  retrying in 30s',
        '[2026-03-26 09:11:50] WARN   message queue backlog  depth=1240  oldest=45s',
        '[2026-03-26 09:11:45] ERROR  failed to deliver notification  channel=email  error=connection_refused',
      ],
      'redis-cache': [
        '[2026-03-26 09:12:00] INFO   keyspace hits=12450  misses=23',
      ],
    },
  };
}

function createAct2Env(): MockEnv {
  return {
    services: {
      'api-gateway': { status: 'unhealthy', error_rate_pct: 22, p99_latency_ms: 60, type: 'reverse-proxy' },
      'auth-service': { status: 'healthy', error_rate_pct: 0, p99_latency_ms: 90, type: 'application' },
      'backend-api': { status: 'healthy', error_rate_pct: 0, p99_latency_ms: 120, type: 'application' },
      'payment-service': { status: 'healthy', error_rate_pct: 0, p99_latency_ms: 45000, type: 'application' },
      'notification-service': { status: 'healthy', error_rate_pct: 0, p99_latency_ms: 200, type: 'application' },
      'redis-cache': { status: 'healthy', error_rate_pct: 0, p99_latency_ms: 3, type: 'cache' },
      'user-db': { status: 'healthy', error_rate_pct: 0, connections_active: 52, type: 'database' },
    },
    configs: {
      'api-gateway': {
        upstream_timeout_ms: 30000, max_retries: 3,
        routes: { '/api/*': 'http://backend-api:8080', '/auth/*': 'http://auth-service:8080', '/notifications/*': 'http://notification-service:8080', '/payments/*': 'http://payment-service:8080' },
      },
    },
    logs: {
      'api-gateway': [
        '[2026-03-26 14:30:12] ERROR  upstream timeout: payment-service did not respond within 30000 ms',
        '[2026-03-26 14:30:12] ERROR  502 Bad Gateway returned to client  path=/payments/checkout',
        '[2026-03-26 14:30:10] ERROR  upstream timeout: payment-service did not respond within 30000 ms',
        '[2026-03-26 14:30:10] ERROR  502 Bad Gateway returned to client  path=/payments/refund',
        '[2026-03-26 14:30:05] WARN   retrying upstream request  attempt=3  service=payment-service',
        '[2026-03-26 14:30:00] INFO   health check passed  service=backend-api  latency=110ms',
        '[2026-03-26 14:29:58] INFO   health check passed  service=auth-service  latency=85ms',
      ],
      'payment-service': [
        '[2026-03-26 14:30:11] INFO   request completed  path=/payments/checkout  duration=44200ms',
        '[2026-03-26 14:30:05] INFO   request completed  path=/payments/refund  duration=42800ms',
        '[2026-03-26 14:29:50] WARN   external payment gateway slow  provider=stripe  duration=41000ms',
      ],
    },
  };
}

function execMockTool(env: MockEnv, name: string, args: Record<string, unknown>): string {
  if (name === 'check_service_status') {
    const svc = args.service_name as string;
    const info = env.services[svc];
    if (!info) {
      return `Service '${svc}' not found. Available: ${Object.keys(env.services).join(', ')}`;
    }
    const lines = [`Service: ${svc}`];
    for (const [k, v] of Object.entries(info)) {
      lines.push(`  ${k}: ${v}`);
    }
    return lines.join('\n');
  }

  if (name === 'check_logs') {
    const svc = args.service_name as string;
    const n = Math.min(Number(args.lines ?? 10), 20);
    const entries = env.logs[svc];
    if (!entries?.length) return `No logs found for '${svc}'.`;
    return entries.slice(0, n).join('\n');
  }

  if (name === 'read_config') {
    const svc = args.service_name as string;
    const cfg = env.configs[svc];
    if (!cfg) return `No config found for '${svc}'.`;
    return JSON.stringify(cfg, null, 2);
  }

  if (name === 'update_config') {
    const svc = args.service_name as string;
    const key = args.key as string;
    let value: unknown = args.value;
    const cfg = env.configs[svc];
    if (!cfg) return `No config found for '${svc}'.`;
    const num = Number(value);
    if (!isNaN(num) && value !== '') value = num;
    cfg[key] = value;
    return `Updated ${svc} config: ${key} = ${value}`;
  }

  if (name === 'restart_service') {
    const svc = args.service_name as string;
    const info = env.services[svc];
    if (!info) return `Service '${svc}' not found.`;
    info.status = 'healthy';
    info.error_rate_pct = 0;
    return `Service '${svc}' restarted successfully. Status: healthy`;
  }

  return `Unknown tool: ${name}`;
}

const MOCK_TOOL_SCHEMAS: OpenAI.ChatCompletionTool[] = [
  {
    type: 'function',
    function: {
      name: 'check_service_status',
      description: 'Check the health status, error rate, and latency of a service.',
      parameters: {
        type: 'object',
        properties: {
          service_name: { type: 'string', description: 'Name of the service to check.' },
        },
        required: ['service_name'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'check_logs',
      description: 'Retrieve recent log entries for a service.',
      parameters: {
        type: 'object',
        properties: {
          service_name: { type: 'string', description: 'Name of the service.' },
          lines: { type: 'integer', description: 'Number of recent log lines to retrieve (max 20).' },
        },
        required: ['service_name'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'read_config',
      description: 'Read the current configuration of a service.',
      parameters: {
        type: 'object',
        properties: {
          service_name: { type: 'string', description: 'Name of the service.' },
        },
        required: ['service_name'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'update_config',
      description: 'Update a configuration value for a service.',
      parameters: {
        type: 'object',
        properties: {
          service_name: { type: 'string', description: 'Name of the service.' },
          key: { type: 'string', description: 'Configuration key to update.' },
          value: { type: 'string', description: 'New value for the configuration key.' },
        },
        required: ['service_name', 'key', 'value'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'restart_service',
      description: 'Restart a service to apply configuration changes.',
      parameters: {
        type: 'object',
        properties: {
          service_name: { type: 'string', description: 'Name of the service to restart.' },
        },
        required: ['service_name'],
      },
    },
  },
];

const MOCK_TOOL_NAMES = new Set(MOCK_TOOL_SCHEMAS.map(t => t.function.name));

// ---------------------------------------------------------------------------
// Agent loop
// ---------------------------------------------------------------------------

const SYSTEM_PROMPT =
  'You are a DevOps incident response agent with full authority to make changes. ' +
  'Diagnose the root cause, apply the fix immediately, and verify it works. ' +
  'Act autonomously — never ask for permission or confirmation. ' +
  'Diagnose the issue, fix it, and verify the fix. ' +
  'Think step by step and explain your reasoning.';

async function runAgent(
  openai: OpenAI,
  ac: AcontextClient,
  sessionId: string,
  env: MockEnv,
  userMessage: string,
  extraSystem: string = '',
  extraTools: OpenAI.ChatCompletionTool[] = [],
  skillCtx?: SkillContext,
): Promise<number> {
  const system = SYSTEM_PROMPT + (extraSystem ? '\n\n' + extraSystem : '');
  const tools: OpenAI.ChatCompletionTool[] = [...MOCK_TOOL_SCHEMAS, ...extraTools];

  const messages: OpenAI.ChatCompletionMessageParam[] = [
    { role: 'system', content: system },
    { role: 'user', content: userMessage },
  ];

  await ac.sessions.storeMessage(sessionId, { role: 'user', content: userMessage });

  let devopsToolCount = 0;
  const maxIterations = 15;

  for (let i = 0; i < maxIterations; i++) {
    const response = await openai.chat.completions.create({
      model: 'gpt-4.1',
      messages,
      tools,
    });

    const msg = response.choices[0].message;

    // Build assistant blob for Acontext
    let assistantBlob: Record<string, unknown>;
    if (msg.tool_calls?.length) {
      assistantBlob = {
        role: 'assistant',
        tool_calls: msg.tool_calls.map(tc => ({
          id: tc.id,
          type: 'function',
          function: { name: tc.function.name, arguments: tc.function.arguments },
        })),
      };
      if (msg.content) assistantBlob.content = msg.content;
    } else {
      assistantBlob = { role: 'assistant', content: msg.content ?? '' };
    }
    messages.push(msg as OpenAI.ChatCompletionMessageParam);
    await ac.sessions.storeMessage(sessionId, assistantBlob);

    if (!msg.tool_calls?.length) {
      console.log(`  Agent: ${msg.content}`);
      break;
    }

    for (const tc of msg.tool_calls) {
      const fnName = tc.function.name;
      const fnArgs = JSON.parse(tc.function.arguments);
      let result: string;

      if (MOCK_TOOL_NAMES.has(fnName)) {
        result = execMockTool(env, fnName, fnArgs);
        devopsToolCount++;
        const label = Object.entries(fnArgs).map(([k, v]) => `${k}=${v}`).join(', ');
        console.log(`    → ${fnName}(${label})`);
      } else if (skillCtx && SKILL_TOOLS.toolExists(fnName)) {
        result = await SKILL_TOOLS.executeTool(skillCtx, fnName, fnArgs);
        const skillName = fnArgs.skill_name ?? fnArgs.file_path ?? fnName;
        console.log(`    ★ ${fnName}(${skillName})`);
      } else {
        result = `Unknown tool: ${fnName}`;
      }

      const toolMsg: OpenAI.ChatCompletionToolMessageParam = {
        role: 'tool',
        tool_call_id: tc.id,
        content: result,
      };
      messages.push(toolMsg);
      await ac.sessions.storeMessage(sessionId, toolMsg as Record<string, unknown>);
    }
  }

  return devopsToolCount;
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function banner(title: string): void {
  console.log('\n' + '='.repeat(70));
  console.log(`  ${title}`);
  console.log('='.repeat(70));
}

async function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function waitForTasks(ac: AcontextClient, sessionId: string, timeout = 90000) {
  const deadline = Date.now() + timeout;
  while (Date.now() < deadline) {
    const status = await ac.sessions.messagesObservingStatus(sessionId);
    if (status.pending === 0 && status.in_process === 0) break;
    await sleep(2000);
  }
  const result = await ac.sessions.getTasks(sessionId);
  return result.items;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main(): Promise<void> {
  const ac = new AcontextClient({
    apiKey: process.env.ACONTEXT_API_KEY!,
    baseUrl: process.env.ACONTEXT_BASE_URL,
  });
  const openai = new OpenAI();

  // ── Act 1: Learning Run ───────────────────────────────────────────────

  banner('ACT 1 — Learning Run: Diagnose 502 errors');

  const space = await ac.learningSpaces.create();
  const session1 = await ac.sessions.create();
  await ac.learningSpaces.learn({ spaceId: space.id, sessionId: session1.id });

  const env1 = createAct1Env();
  const act1Tools = await runAgent(
    openai, ac, session1.id, env1,
    'Our API gateway is returning 502 errors on /api/* routes — ' +
    'about 34% of requests are failing. ' +
    'Diagnose the root cause and fix it.',
  );

  // Wait for task extraction
  console.log('\n  Waiting for task extraction...');
  await ac.sessions.flush(session1.id);
  const tasks = await waitForTasks(ac, session1.id);
  console.log(`  Extracted ${tasks.length} task(s):`);
  for (const t of tasks) {
    console.log(`    [${t.status}] ${t.data.task_description}`);
  }

  // Wait for skill learning
  console.log('\n  Waiting for skill learning pipeline...');
  const learnResult = await ac.learningSpaces.waitForLearning({
    spaceId: space.id, sessionId: session1.id, timeout: 180,
  });
  console.log(`  Learning status: ${learnResult.status}`);

  // Download generated skills to local directory
  const skills = await ac.learningSpaces.listSkills(space.id);
  const outDir = path.join(path.dirname(new URL(import.meta.url).pathname), 'learned_skills');
  await fs.mkdir(outDir, { recursive: true });
  console.log(`\n  Generated ${skills.length} skill(s) — downloading to learned_skills/`);
  for (const s of skills) {
    const skillDir = path.join(outDir, s.name);
    await fs.mkdir(skillDir, { recursive: true });
    for (const f of s.fileIndex) {
      const content = await ac.skills.getFile({ skillId: s.id, filePath: f.path });
      if (content.content) await fs.writeFile(path.join(skillDir, f.path), content.content.raw);
    }
    console.log(`    • ${s.name}: ${s.description}`);
  }

  // ── Act 2: Recall Run ────────────────────────────────────────────────

  banner('ACT 2 — Recall Run: New 502 incident (with learned skills)');

  const session2 = await ac.sessions.create();
  await ac.learningSpaces.learn({ spaceId: space.id, sessionId: session2.id });

  const skillIds = skills.map(s => s.id);
  const skillCtx = await SKILL_TOOLS.formatContext(ac, skillIds);
  const skillToolsSchema = SKILL_TOOLS.toOpenAIToolSchema() as OpenAI.ChatCompletionTool[];

  const env2 = createAct2Env();
  const act2Tools = await runAgent(
    openai, ac, session2.id, env2,
    'The API gateway started returning 502 errors again after today\'s deployment. ' +
    'About 22% of requests are failing. Please diagnose and fix.',
    'You have access to skills learned from previous incidents. ' +
    'ALWAYS check your skills first before starting diagnosis.\n\n' +
    skillCtx.getContextPrompt(),
    skillToolsSchema,
    skillCtx,
  );

  // ── Summary ───────────────────────────────────────────────────────────

  banner('RESULTS');
  console.log(`  Act 1 (no prior knowledge):  ${act1Tools} tool calls`);
  console.log(`  Act 2 (with learned skills): ${act2Tools} tool calls`);
  if (act2Tools < act1Tools) {
    const pct = Math.round((1 - act2Tools / act1Tools) * 100);
    console.log(`  → ${pct}% fewer tool calls with learned skills`);
  } else if (act2Tools === act1Tools) {
    console.log('  → Same number of tool calls');
  } else {
    console.log('  → Act 2 used more calls (LLM variance)');
  }
  console.log(`\n  Skills saved to: learned_skills/`);

  // Cleanup remote resources
  await ac.sessions.delete(session1.id);
  await ac.sessions.delete(session2.id);
  await ac.learningSpaces.delete(space.id);
  for (const s of skills) {
    await ac.skills.delete(s.id);
  }
  console.log('  Cleaned up remote sessions, learning space, and skills.');
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
