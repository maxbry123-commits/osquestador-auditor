/**
 * Task API operations for AcontextClient
 */

import { Constructor, BaseClient } from "./base";

// ==================== Type Definitions ====================

export type TaskStatus = "success" | "failed" | "running" | "pending";

export interface Task {
  id: string;
  session_id: string;
  order: number;
  status: TaskStatus;
  is_planning: boolean;
  data: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface GetTasksResp {
  items: Task[];
  next_cursor?: string;
  has_more: boolean;
}

// ==================== Task Operations Mixin ====================

export function TaskOperations<T extends Constructor<BaseClient>>(Base: T) {
  return class extends Base {
    async getTasks(
      projectId: string,
      sessionId: string,
      limit: number = 20,
      cursor?: string
    ): Promise<GetTasksResp> {
      const params = new URLSearchParams({
        limit: limit.toString(),
      });
      if (cursor) {
        params.append("cursor", cursor);
      }

      const result = await this.request<{
        items?: Task[];
        tasks?: Task[];
        next_cursor?: string;
        has_more?: boolean;
      }>(`/api/v1/session/${sessionId}/task?${params.toString()}`, {
        projectId,
      });
      return {
        items: result.items || result.tasks || [],
        next_cursor: result.next_cursor,
        has_more: result.has_more || false,
      };
    }
  };
}
