"use server";

import { createClient } from "@/lib/supabase/server";

export interface AlertBannerData {
  id: string;
  visible: boolean;
  start_at?: string;
  end_at?: string;
  icon?: string;
  color?: string;
  url?: string;
  html: string;
}

function isBannerActive(data: AlertBannerData): boolean {
  if (!data.visible) return false;
  const now = Date.now();
  if (data.start_at && now < new Date(data.start_at).getTime()) return false;
  if (data.end_at && now > new Date(data.end_at).getTime()) return false;
  return true;
}

export async function getAlertBanner(): Promise<AlertBannerData | null> {
  try {
    const supabase = await createClient();
    const { data, error } = await supabase.functions.invoke("get-alert-banner");

    if (error) {
      console.error("Error fetching alert banner:", error);
      return null;
    }

    const response = data as AlertBannerData;
    if (!isBannerActive(response)) {
      return null;
    }

    return response;
  } catch (error) {
    console.error("Error fetching alert banner:", error);
    return null;
  }
}
