/**
 * Cached Supabase operations for Server Components
 *
 * These functions use React.cache() for per-request memoization,
 * which helps deduplicate requests when the same data is needed
 * multiple times in a single render.
 *
 * Note: These should only be used in Server Components, not Server Actions.
 */

import { cache } from "react";
import { createClient } from "../server";
import { redirect } from "next/navigation";
import type { User } from "@supabase/supabase-js";
import type { OrganizationMembership } from "./organizations";
import type { OrganizationProject } from "./projects";

/**
 * Get the current authenticated user (cached)
 * Redirects to login if not authenticated
 */
export const getCurrentUser = cache(async (): Promise<User> => {
  const supabase = await createClient();
  const {
    data: { user },
    error,
  } = await supabase.auth.getUser();

  if (error || !user) {
    redirect("/auth/login");
  }

  return user;
});

/**
 * Get the current authenticated user without redirecting (cached)
 * Returns null if not authenticated
 */
export const getCurrentUserOptional = cache(async (): Promise<User | null> => {
  const supabase = await createClient();
  const {
    data: { user },
    error,
  } = await supabase.auth.getUser();

  if (error || !user) {
    return null;
  }

  return user;
});

/**
 * Get a single project by project ID (cached)
 */
export const getProject = cache(async (projectId: string): Promise<OrganizationProject | null> => {
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
});

/**
 * Get projects for an organization (cached)
 */
export const getOrganizationProjects = cache(async (orgId: string): Promise<OrganizationProject[]> => {
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
});

/**
 * Get organization details (cached)
 */
export const getOrganization = cache(async (orgId: string) => {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("organizations")
    .select("*")
    .eq("id", orgId)
    .single();

  if (error || !data) {
    return null;
  }

  return data;
});

/**
 * Get user's membership for a specific organization (cached)
 */
export const getOrganizationMembership = cache(async (
  userId: string,
  orgId: string,
  select?: string
): Promise<OrganizationMembership | null> => {
  const supabase = await createClient();
  const query = supabase
    .from("organization_members")
    .select(select || "role, organizations (*)")
    .eq("user_id", userId)
    .eq("organization_id", orgId)
    .single();

  const { data, error } = await query;

  if (error || !data) {
    return null;
  }

  return data as unknown as OrganizationMembership;
});

/**
 * Get all user's organization memberships (cached)
 */
export const getOrganizationMemberships = cache(async (
  userId: string,
  select?: string
): Promise<OrganizationMembership[]> => {
  const supabase = await createClient();
  const query = supabase
    .from("organization_members")
    .select(select || "organization_id, role, organizations (*)")
    .eq("user_id", userId)
    .order("created_at", { ascending: true });

  const { data, error } = await query;

  if (error || !data) {
    return [];
  }

  return data as unknown as OrganizationMembership[];
});

/**
 * Get organization membership for current user (cached)
 */
export const getOrganizationMembershipForCurrentUser = cache(async (
  orgId: string,
  select?: string
): Promise<OrganizationMembership | null> => {
  const user = await getCurrentUser();
  return await getOrganizationMembership(user.id, orgId, select);
});

/**
 * Get all organization memberships for current user (cached)
 */
export const getOrganizationMembershipsForCurrentUser = cache(async (
  select?: string
): Promise<OrganizationMembership[]> => {
  const user = await getCurrentUser();
  return await getOrganizationMemberships(user.id, select);
});

/**
 * Re-export getOrganizationDataWithPlan from organizations
 * Note: This function already uses cached functions internally, so it's safe to use in Server Components
 */
export { getOrganizationDataWithPlan } from "./organizations";
