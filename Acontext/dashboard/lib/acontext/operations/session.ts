/**
 * Session API operations for AcontextClient
 */

import { Constructor, BaseClient } from "./base";

// ==================== Type Definitions ====================

export interface Session {
  id: string;
  project_id?: string;
  user_id?: string;
  configs: Record<string, unknown>;
  disable_task_tracking?: boolean;
  created_at: string;
  updated_at: string;
}

export interface GetSessionsResp {
  items: Session[];
  next_cursor?: string;
  has_more: boolean;
}

export interface GetSessionConfigsResp {
  configs: Record<string, unknown>;
}

// ==================== Session Operations Mixin ====================

export function SessionOperations<T extends Constructor<BaseClient>>(Base: T) {
  return class extends Base {
    async getSessions(
      projectId: string,
      limit: number = 20,
      cursor?: string,
      timeDesc: boolean = false,
      user?: string
    ): Promise<GetSessionsResp> {
      const params = new URLSearchParams({
        limit: limit.toString(),
        time_desc: timeDesc.toString(),
      });
      if (cursor) {
        params.append("cursor", cursor);
      }
      if (user) {
        params.append("user", user);
      }

      const result = await this.request<{
        items?: Session[];
        sessions?: Session[];
        next_cursor?: string;
        has_more?: boolean;
      }>(`/api/v1/session?${params.toString()}`, {
        projectId,
      });
      return {
        items: result.items || result.sessions || [],
        next_cursor: result.next_cursor,
        has_more: result.has_more || false,
      };
    }

    async createSession(
      projectId: string,
      configs?: Record<string, unknown>,
      user?: string,
      disableTaskTracking?: boolean
    ): Promise<Session> {
      const body: Record<string, unknown> = {};
      if (configs) {
        body.configs = configs;
      }
      if (user) {
        body.user = user;
      }
      if (disableTaskTracking !== undefined) {
        body.disable_task_tracking = disableTaskTracking;
      }

      const result = await this.request<{ session?: Session } | Session>(
        "/api/v1/session",
        {
          method: "POST",
          projectId,
          body: JSON.stringify(body),
        }
      );
      if (result && typeof result === "object" && "session" in result) {
        return (result as { session?: Session }).session || (result as Session);
      }
      return result as Session;
    }

    async deleteSession(projectId: string, sessionId: string): Promise<void> {
      await this.request(`/api/v1/session/${sessionId}`, {
        method: "DELETE",
        projectId,
      });
    }

    async getSessionConfigs(projectId: string, sessionId: string): Promise<GetSessionConfigsResp> {
      const result = await this.request<{ configs?: Record<string, unknown> } | Record<string, unknown>>(
        `/api/v1/session/${sessionId}/configs`,
        {
          projectId,
        }
      );
      if (result && typeof result === "object" && "configs" in result) {
        return {
          configs: (result as { configs?: Record<string, unknown> }).configs || {},
        };
      }
      return {
        configs: result as Record<string, unknown>,
      };
    }

    async updateSessionConfigs(
      projectId: string,
      sessionId: string,
      configs: Record<string, unknown>
    ): Promise<void> {
      await this.request(`/api/v1/session/${sessionId}/configs`, {
        method: "PUT",
        projectId,
        body: JSON.stringify({ configs }),
      });
    }
  };
}
