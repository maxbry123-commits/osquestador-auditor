/**
 * User API operations for AcontextClient
 */

import { Constructor, BaseClient } from "./base";

// ==================== Type Definitions ====================

export interface User {
  id: string;
  identifier: string;
  project_id: string;
  created_at: string;
  updated_at: string;
}

export interface GetUsersResp {
  items: User[];
  next_cursor?: string;
  has_more: boolean;
}

export interface UserResourceCounts {
  disks_count: number;
  sessions_count: number;
  skills_count: number;
  spaces_count: number;
}

export interface GetUserResourcesResp {
  counts: UserResourceCounts;
}

// ==================== User Operations Mixin ====================

export function UserOperations<T extends Constructor<BaseClient>>(Base: T) {
  return class extends Base {
    /**
     * List all users under a project
     */
    async getUsers(
      projectId: string,
      limit: number = 0,
      cursor?: string,
      timeDesc: boolean = false
    ): Promise<GetUsersResp> {
      const params = new URLSearchParams();
      if (limit > 0) {
        params.append("limit", limit.toString());
      }
      if (cursor) {
        params.append("cursor", cursor);
      }
      params.append("time_desc", timeDesc.toString());

      const result = await this.request<{
        items?: User[];
        users?: User[];
        next_cursor?: string;
        has_more?: boolean;
      }>(`/api/v1/user/ls?${params.toString()}`, {
        projectId,
      });
      return {
        items: result.items || result.users || [],
        next_cursor: result.next_cursor,
        has_more: result.has_more || false,
      };
    }

    /**
     * Delete a user by identifier (cascade deletes all associated resources)
     */
    async deleteUser(projectId: string, identifier: string): Promise<void> {
      await this.request(`/api/v1/user/${encodeURIComponent(identifier)}`, {
        method: "DELETE",
        projectId,
      });
    }

    /**
     * Get user resource counts (disks, sessions, skills, spaces)
     */
    async getUserResources(
      projectId: string,
      identifier: string
    ): Promise<GetUserResourcesResp> {
      const result = await this.request<{
        counts?: UserResourceCounts;
      }>(`/api/v1/user/${encodeURIComponent(identifier)}/resources`, {
        projectId,
      });
      return {
        counts: result.counts || {
          disks_count: 0,
          sessions_count: 0,
          skills_count: 0,
          spaces_count: 0,
        },
      };
    }
  };
}
