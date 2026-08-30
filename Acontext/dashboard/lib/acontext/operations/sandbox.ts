/**
 * Sandbox API operations for AcontextClient
 */

import { Constructor, BaseClient } from "./base";

// ==================== Type Definitions ====================

export interface HistoryCommand {
  command: string;
  exit_code: number;
}

export interface GeneratedFile {
  sandbox_path: string;
}

export interface SandboxLog {
  id: string;
  project_id: string;
  backend_type: string;
  backend_sandbox_id: string;
  created_at: string;
  updated_at: string;
  will_total_alive_seconds?: number;
  history_commands?: HistoryCommand[];
  generated_files?: GeneratedFile[];
}

export interface GetSandboxLogsResp {
  items: SandboxLog[];
  next_cursor?: string;
  has_more: boolean;
}

// ==================== Sandbox Operations Mixin ====================

export function SandboxOperations<T extends Constructor<BaseClient>>(Base: T) {
  return class extends Base {
    async getSandboxLogs(
      projectId: string,
      limit: number = 20,
      cursor?: string,
      timeDesc: boolean = false
    ): Promise<GetSandboxLogsResp> {
      const params = new URLSearchParams({
        limit: limit.toString(),
        time_desc: timeDesc.toString(),
      });
      if (cursor) {
        params.append("cursor", cursor);
      }

      const result = await this.request<{
        items?: SandboxLog[];
        next_cursor?: string;
        has_more?: boolean;
      }>(`/api/v1/sandbox/logs?${params.toString()}`, {
        projectId,
      });
      return {
        items: result.items || [],
        next_cursor: result.next_cursor,
        has_more: result.has_more || false,
      };
    }
  };
}
