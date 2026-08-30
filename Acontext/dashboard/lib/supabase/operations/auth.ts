"use server";

import { createClient } from "../server";
import { redirect } from "next/navigation";
import type { User, VerifyOtpParams } from "@supabase/supabase-js";

/**
 * Get the current authenticated user
 * Redirects to login if not authenticated
 */
export async function getCurrentUser(): Promise<User> {
  const supabase = await createClient();
  const {
    data: { user },
    error,
  } = await supabase.auth.getUser();

  if (error || !user) {
    redirect("/auth/login");
  }

  return user;
}

/**
 * Get the current authenticated user without redirecting
 * Returns null if not authenticated
 */
export async function getCurrentUserOptional(): Promise<User | null> {
  const supabase = await createClient();
  const {
    data: { user },
    error,
  } = await supabase.auth.getUser();

  if (error || !user) {
    return null;
  }

  return user;
}

/**
 * Sign in with email and password
 */
export async function signInWithPassword(email: string, password: string) {
  const supabase = await createClient();
  return await supabase.auth.signInWithPassword({ email, password });
}

/**
 * Sign in with OAuth provider
 */
export async function signInWithOAuth(
  provider: "google" | "github",
  next?: string
) {
  const supabase = await createClient();
  const callbackPath = next
    ? `/auth/callback?next=${encodeURIComponent(next)}`
    : "/auth/callback";
  return await supabase.auth.signInWithOAuth({
    provider,
    options: {
      redirectTo:
        process.env.NEXT_PUBLIC_BASE_URL! +
        (process.env.NEXT_PUBLIC_BASE_PATH || "") +
        callbackPath,
    },
  });
}

/**
 * Sign up with email and password
 */
export async function signUp(email: string, password: string) {
  const supabase = await createClient();
  return await supabase.auth.signUp({
    email,
    password,
    options: {
      emailRedirectTo:
        process.env.NEXT_PUBLIC_BASE_URL! +
        (process.env.NEXT_PUBLIC_BASE_PATH || "") +
        "",
    },
  });
}

/**
 * Sign out the current user
 */
export async function signOut() {
  const supabase = await createClient();
  return await supabase.auth.signOut();
}

/**
 * Reset password for email
 */
export async function resetPasswordForEmail(email: string) {
  const supabase = await createClient();
  return await supabase.auth.resetPasswordForEmail(email, {
    redirectTo:
      process.env.NEXT_PUBLIC_BASE_URL! +
      (process.env.NEXT_PUBLIC_BASE_PATH || "") +
      "/auth/update-password",
  });
}

/**
 * Update user password
 */
export async function updateUserPassword(password: string) {
  const supabase = await createClient();
  return await supabase.auth.updateUser({ password });
}

/**
 * Exchange code for session (OAuth callback)
 */
export async function exchangeCodeForSession(code: string) {
  const supabase = await createClient();
  return await supabase.auth.exchangeCodeForSession(code);
}

/**
 * Verify OTP with token_hash
 */
export async function verifyOtp(params: VerifyOtpParams) {
  const supabase = await createClient();
  return await supabase.auth.verifyOtp(params);
}

/**
 * Get current session
 */
export async function getSession() {
  const supabase = await createClient();
  return await supabase.auth.getSession();
}
