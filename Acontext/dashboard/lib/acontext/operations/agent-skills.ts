/**
 * Agent Skills API operations for AcontextClient
 */

import { Constructor, BaseClient } from "./base";

// ==================== Type Definitions ====================

export interface AgentSkillFileIndex {
  path: string;
  mime: string;
}

export interface AgentSkill {
  id: string;
  name: string;
  description: string;
  file_index: AgentSkillFileIndex[];
  meta?: Record<string, unknown>;
  user_id?: string;
  created_at: string;
  updated_at: string;
}

export interface AgentSkillListItem {
  id: string;
  name: string;
  description: string;
  meta?: Record<string, unknown>;
  user_id?: string;
  created_at: string;
  updated_at: string;
}

export interface GetAgentSkillsResp {
  items: AgentSkillListItem[];
  next_cursor?: string;
  has_more: boolean;
}

export interface AgentSkillFileContent {
  type: string;
  raw: string;
}

export interface GetAgentSkillFileResp {
  path: string;
  mime: string;
  content?: AgentSkillFileContent | null;
  url?: string | null;
}

// ==================== Agent Skills Operations Mixin ====================

export function AgentSkillsOperations<T extends Constructor<BaseClient>>(Base: T) {
  return class extends Base {
    /**
     * List all agent skills under a project
     */
    async getAgentSkills(
      projectId: string,
      limit: number = 20,
      cursor?: string,
      timeDesc: boolean = false,
      user?: string
    ): Promise<GetAgentSkillsResp> {
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
        items?: AgentSkillListItem[];
        next_cursor?: string;
        has_more?: boolean;
      }>(`/api/v1/agent_skills?${params.toString()}`, {
        projectId,
      });
      return {
        items: result.items || [],
        next_cursor: result.next_cursor,
        has_more: result.has_more || false,
      };
    }

    /**
     * Get agent skill by ID (includes file_index)
     */
    async getAgentSkill(projectId: string, skillId: string): Promise<AgentSkill> {
      const result = await this.request<AgentSkill>(
        `/api/v1/agent_skills/${skillId}`,
        {
          projectId,
        }
      );
      return result;
    }

    /**
     * Delete agent skill by ID
     */
    async deleteAgentSkill(projectId: string, skillId: string): Promise<void> {
      await this.request(`/api/v1/agent_skills/${skillId}`, {
        method: "DELETE",
        projectId,
      });
    }

    /**
     * Get file content or download URL from agent skill
     */
    async getAgentSkillFile(
      projectId: string,
      skillId: string,
      filePath: string,
      expire: number = 900
    ): Promise<GetAgentSkillFileResp> {
      const params = new URLSearchParams({
        file_path: filePath,
        expire: expire.toString(),
      });

      const result = await this.request<GetAgentSkillFileResp>(
        `/api/v1/agent_skills/${skillId}/file?${params.toString()}`,
        {
          projectId,
        }
      );
      return result;
    }

    /**
     * Create agent skill by uploading a zip file
     */
    async createAgentSkill(
      projectId: string,
      file: File,
      user?: string,
      meta?: Record<string, unknown>
    ): Promise<AgentSkill> {
      const formData = new FormData();
      formData.append("file", file);
      if (user) {
        formData.append("user", user);
      }
      if (meta && Object.keys(meta).length > 0) {
        formData.append("meta", JSON.stringify(meta));
      }

      const result = await this.request<AgentSkill>("/api/v1/agent_skills", {
        method: "POST",
        projectId,
        body: formData,
        useFormData: true,
      });
      return result;
    }
  };
}
