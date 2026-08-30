/**
 * Unified Supabase operations library
 *
 * This module provides a centralized location for all Supabase database
 * and authentication operations, making them easier to manage and reuse.
 *
 * Structure:
 * - operations/ - Business logic and database operations (CRUD, queries, mutations)
 * - operations/cached.ts - Cached operations for Server Components
 * - server.ts - Server-side Supabase client creation
 * - client.ts - Browser-side Supabase client creation
 */

// Re-export all operations
export * from "./operations";

// Client creation
export { createClient } from "./server";
export { createClient as createBrowserClient } from "./client";

