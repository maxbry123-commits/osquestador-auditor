"use server";

import { createClient } from "../server";

// OrganizationProject is the database representation with project_id
// Project is the application type with id
// This type is kept for backward compatibility with database queries
export interface OrganizationProject {
  project_id: string;
  name: string;
  organization_id: string;
  created_at?: string;
}

// Helper type: Project from database (OrganizationProject)
// This can be converted to Project type by mapping project_id -> id

/**
 * Get projects for an organization
 */
export async function getOrganizationProjects(orgId: string) {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("organization_projects")
    .select("project_id, name, created_at")
    .eq("organization_id", orgId)
    .order("created_at", { ascending: true });

  if (error || !data) {
    return [];
  }

  return data as OrganizationProject[];
}

/**
 * Get a single project by project ID
 */
export async function getProject(projectId: string) {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("organization_projects")
    .select("project_id, name, organization_id, created_at")
    .eq("project_id", projectId)
    .single();

  if (error || !data) {
    return null;
  }

  return data as OrganizationProject;
}

/**
 * Update project name
 */
export async function updateProject(
  projectId: string,
  updates: { name?: string; [key: string]: unknown }
) {
  const supabase = await createClient();
  return await supabase
    .from("organization_projects")
    .update(updates)
    .eq("project_id", projectId);
}

/**
 * Delete project
 */
export async function deleteProject(projectId: string) {
  const supabase = await createClient();
  return await supabase
    .from("organization_projects")
    .delete()
    .eq("project_id", projectId);
}

/**
 * Create organization project using RPC
 */
export async function createOrganizationProject(params: {
  p_org_id: string;
  p_project_name: string;
  p_project_id: string;
}) {
  const supabase = await createClient();
  return await supabase.rpc("create_organization_project", params);
}

// ==================== Secret Key Rotations ====================

export interface SecretKeyRotation {
  id: string;
  user_email: string;
  project_id: string;
  secret_key: string;
  created_at: string;
  updated_at: string;
}

/**
 * Get secret key rotations for a project
 * Returns rotations ordered by created_at DESC (newest first)
 */
export async function getSecretKeyRotations(projectId: string): Promise<SecretKeyRotation[]> {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("project_secret_key_rotations")
    .select("*")
    .eq("project_id", projectId)
    .order("created_at", { ascending: false });

  if (error || !data) {
    return [];
  }

  return data as SecretKeyRotation[];
}

/**
 * Create a secret key rotation record
 * Note: secretKey should already be masked (first 8 + ***** + last 8)
 */
export async function createSecretKeyRotation(
  projectId: string,
  userEmail: string,
  maskedSecretKey: string
) {
  const supabase = await createClient();
  return await supabase
    .from("project_secret_key_rotations")
    .insert({
      project_id: projectId,
      user_email: userEmail,
      secret_key: maskedSecretKey,
    });
}

