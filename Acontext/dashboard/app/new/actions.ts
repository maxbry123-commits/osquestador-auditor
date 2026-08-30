"use server";

import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { MAX_ORG_NAME_LENGTH } from "@/lib/utils";
import { encodeId } from "@/lib/id-codec";
import {
  getCurrentUser,
  createOrganization as createOrg,
} from "@/lib/supabase";

export async function createOrganization(formData: FormData) {
  await getCurrentUser();

  const name = formData.get("name") as string;

  if (!name || name.trim() === "") {
    redirect(`/new?error=${encodeURIComponent("Name is required")}`);
  }

  const trimmedName = name.trim();
  if (trimmedName.length > MAX_ORG_NAME_LENGTH) {
    redirect(
      `/new?error=${encodeURIComponent(`Name must be ${MAX_ORG_NAME_LENGTH} characters or less`)}`
    );
  }

  const { data, error } = await createOrg(trimmedName, "free");

  if (error) {
    redirect(`/new?error=${encodeURIComponent(error.message)}`);
  }

  if (!data) {
    redirect(`/new?error=${encodeURIComponent("Failed to create organization")}`);
  }

  revalidatePath("/", "layout");

  const encodedOrgId = encodeId(data);
  redirect(`/new/${encodedOrgId}`);
}

