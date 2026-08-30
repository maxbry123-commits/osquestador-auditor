/**
 * Disk API operations for AcontextClient
 */

import { Constructor, BaseClient } from "./base";

// ==================== Type Definitions ====================

export interface Disk {
  id: string;
  project_id: string;
  user_id?: string;
  created_at: string;
  updated_at: string;
}

export interface Artifact {
  disk_id: string;
  path: string;
  filename: string;
  meta: {
    __artifact_info__: {
      filename: string;
      mime: string;
      path: string;
      size: number;
    };
    [key: string]: unknown;
  };
  created_at: string;
  updated_at: string;
}

export interface ListArtifactsResp {
  artifacts: Artifact[];
  directories: string[];
}

export interface FileContent {
  type: string;
  raw: string;
}

export interface GetArtifactResp {
  artifact: Artifact;
  public_url: string | null;
  content?: FileContent | null;
}

export interface GetDisksResp {
  items: Disk[];
  next_cursor?: string;
  has_more: boolean;
}

// ==================== Disk Operations Mixin ====================

export function DiskOperations<T extends Constructor<BaseClient>>(Base: T) {
  return class extends Base {
    async getDisks(
      projectId: string,
      limit: number = 20,
      cursor?: string,
      timeDesc: boolean = false,
      user?: string
    ): Promise<GetDisksResp> {
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
        items?: Disk[];
        disks?: Disk[];
        next_cursor?: string;
        has_more?: boolean;
      }>(`/api/v1/disk?${params.toString()}`, {
        projectId,
      });
      return {
        items: result.items || result.disks || [],
        next_cursor: result.next_cursor,
        has_more: result.has_more || false,
      };
    }

    async getListArtifacts(
      projectId: string,
      diskId: string,
      path: string
    ): Promise<ListArtifactsResp> {
      const result = await this.request<{
        artifacts?: Artifact[];
        directories?: string[];
      }>(`/api/v1/disk/${diskId}/artifact/ls?path=${encodeURIComponent(path)}`, {
        projectId,
      });
      return {
        artifacts: result.artifacts || [],
        directories: result.directories || [],
      };
    }

    async getArtifact(
      projectId: string,
      diskId: string,
      filePath: string,
      withContent: boolean = true
    ): Promise<GetArtifactResp> {
      const result = await this.request<{
        artifact?: Artifact;
        public_url?: string | null;
        content?: FileContent | null;
      }>(
        `/api/v1/disk/${diskId}/artifact?file_path=${encodeURIComponent(filePath)}&with_content=${withContent}`,
        {
          projectId,
        }
      );
      return {
        artifact: result.artifact!,
        public_url: result.public_url || null,
        content: result.content || undefined,
      };
    }

    async createDisk(projectId: string, user?: string): Promise<Disk> {
      const body: Record<string, string> = {};
      if (user) {
        body.user = user;
      }

      const result = await this.request<{ disk?: Disk } | Disk>(
        "/api/v1/disk",
        {
          method: "POST",
          projectId,
          body: JSON.stringify(body),
        }
      );
      if (result && typeof result === "object" && "disk" in result) {
        return (result as { disk?: Disk }).disk || (result as Disk);
      }
      return result as Disk;
    }

    async deleteDisk(projectId: string, diskId: string): Promise<void> {
      await this.request(`/api/v1/disk/${diskId}`, {
        method: "DELETE",
        projectId,
      });
    }

    async uploadArtifact(
      projectId: string,
      diskId: string,
      filePath: string,
      file: File,
      meta?: Record<string, string>
    ): Promise<void> {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("file_path", filePath);
      if (meta && Object.keys(meta).length > 0) {
        formData.append("meta", JSON.stringify(meta));
      }

      await this.request(`/api/v1/disk/${diskId}/artifact`, {
        method: "POST",
        projectId,
        body: formData,
        useFormData: true,
      });
    }

    async deleteArtifact(projectId: string, diskId: string, filePath: string): Promise<void> {
      await this.request(
        `/api/v1/disk/${diskId}/artifact?file_path=${encodeURIComponent(filePath)}`,
        {
          method: "DELETE",
          projectId,
        }
      );
    }

    async updateArtifactMeta(
      projectId: string,
      diskId: string,
      filePath: string,
      meta: Record<string, unknown>
    ): Promise<void> {
      await this.request(`/api/v1/disk/${diskId}/artifact`, {
        method: "PUT",
        projectId,
        body: JSON.stringify({
          file_path: filePath,
          meta: JSON.stringify(meta),
        }),
      });
    }
  };
}
