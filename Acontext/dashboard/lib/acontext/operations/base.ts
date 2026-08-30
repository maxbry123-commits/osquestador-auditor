/**
 * Base types for operation mixins
 */

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type Constructor<T = object> = new (...args: any[]) => T;

export interface BaseClient {
  request<T>(
    endpoint: string,
    options?: {
      method?: string;
      projectId?: string;
      body?: BodyInit;
      headers?: Record<string, string>;
      useFormData?: boolean;
    }
  ): Promise<T>;
  formatDate(dateStr: string): string;
}
