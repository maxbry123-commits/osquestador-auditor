"use client";

import { Suspense, useEffect, useState } from "react";
import { useFormStatus } from "react-dom";
import { useSearchParams } from "next/navigation";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";

import { createOrganization } from "@/app/new/actions";
import { useTopNavStore } from "@/stores/top-nav";
import { MAX_ORG_NAME_LENGTH } from "@/lib/utils";

function SubmitButton({
  label,
  loadingLabel,
}: {
  label: string;
  loadingLabel: string;
}) {
  const { pending } = useFormStatus();

  return (
    <Button type="submit" className="w-full" disabled={pending}>
      {pending ? loadingLabel : label}
    </Button>
  );
}

export default function NewOrganizationPage() {
  return (
    <Suspense>
      <NewOrganizationContent />
    </Suspense>
  );
}

function NewOrganizationContent() {
  const searchParams = useSearchParams();
  const error = searchParams.get("error");
  const { initialize } = useTopNavStore();
  const [name, setName] = useState<string>("");

  useEffect(() => {
    initialize({
      title: "New organization",
      organization: null,
      project: null,
      organizations: [],
      projects: [],
      hasSidebar: false,
    });
  }, [initialize]);

  return (
    <div className="flex-1 flex min-h-screen items-start justify-center p-4 pt-16">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Create a new organization</CardTitle>
          <CardDescription>
            Organizations are a way to group your projects. Each organization
            can be configured with different team members.
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <Alert variant="destructive" className="mb-4">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          <form action={createOrganization}>
            <input type="hidden" name="plan" value="free" />
            <div className="grid gap-6">
              <div className="grid gap-2">
                <div className="flex items-center justify-between">
                  <Label htmlFor="name">Name</Label>
                  <span className="text-xs text-muted-foreground">
                    {name.length}/{MAX_ORG_NAME_LENGTH}
                  </span>
                </div>
                <Input
                  id="name"
                  name="name"
                  type="text"
                  placeholder="My Organization"
                  maxLength={MAX_ORG_NAME_LENGTH}
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
              <SubmitButton
                label="Create Organization"
                loadingLabel="Creating..."
              />
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
