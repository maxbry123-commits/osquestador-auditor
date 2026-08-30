/**
 * UUID to Base64URL codec utilities
 *
 * Converts UUIDs (36 chars) to URL-safe Base64 strings (22 chars)
 * Example: 550e8400-e29b-41d4-a716-446655440000 → VQ6EAOKbQdSnFkRmVUQAAA
 */

// UUID v4 format: 8-4-4-4-12 hex digits with hyphens
const UUID_REGEX = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

// Base64URL format: 22 characters (no padding)
const BASE64URL_REGEX = /^[A-Za-z0-9_-]{22}$/;

/**
 * Check if a string is a valid UUID format
 */
export function isUuid(str: string): boolean {
  return UUID_REGEX.test(str);
}

/**
 * Check if a string is a valid Base64URL format (22 chars, UUID encoded)
 */
export function isBase64Url(str: string): boolean {
  return BASE64URL_REGEX.test(str);
}

/**
 * Convert UUID to Base64URL
 *
 * Process:
 * 1. Remove hyphens from UUID
 * 2. Convert hex string to bytes
 * 3. Encode to Base64
 * 4. Make URL-safe (+ → -, / → _, remove padding)
 *
 * @param uuid - UUID string with hyphens (e.g., "550e8400-e29b-41d4-a716-446655440000")
 * @returns Base64URL encoded string (22 chars)
 * @throws Error if uuid is not valid format
 */
export function uuidToBase64Url(uuid: string): string {
  if (!isUuid(uuid)) {
    throw new Error(`Invalid UUID format: ${uuid}`);
  }

  // Remove hyphens
  const hex = uuid.replace(/-/g, '');

  // Convert hex to bytes
  const bytes = new Uint8Array(16);
  for (let i = 0; i < 16; i++) {
    bytes[i] = parseInt(hex.substr(i * 2, 2), 16);
  }

  // Convert to Base64
  let base64 = '';
  if (typeof Buffer !== 'undefined') {
    // Node.js environment
    base64 = Buffer.from(bytes).toString('base64');
  } else {
    // Browser environment
    const binary = String.fromCharCode(...bytes);
    base64 = btoa(binary);
  }

  // Make URL-safe: replace + with -, / with _, remove padding =
  const base64url = base64
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');

  return base64url;
}

/**
 * Convert Base64URL to UUID
 *
 * Process:
 * 1. Convert URL-safe chars back to standard Base64
 * 2. Add padding if needed
 * 3. Decode to bytes
 * 4. Convert bytes to hex string
 * 5. Insert hyphens at proper positions
 *
 * @param base64url - Base64URL encoded string (22 chars)
 * @returns UUID string with hyphens
 * @throws Error if base64url is not valid format
 */
export function base64UrlToUuid(base64url: string): string {
  if (!isBase64Url(base64url)) {
    throw new Error(`Invalid Base64URL format: ${base64url}`);
  }

  // Convert URL-safe chars back to standard Base64
  let base64 = base64url
    .replace(/-/g, '+')
    .replace(/_/g, '/');

  // Add padding (UUID is 16 bytes = 24 base64 chars with padding)
  while (base64.length % 4 !== 0) {
    base64 += '=';
  }

  // Decode to bytes
  let bytes: Uint8Array;
  if (typeof Buffer !== 'undefined') {
    // Node.js environment
    bytes = new Uint8Array(Buffer.from(base64, 'base64'));
  } else {
    // Browser environment
    const binary = atob(base64);
    bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i);
    }
  }

  // Convert bytes to hex string
  const hex = Array.from(bytes)
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');

  // Insert hyphens at proper positions: 8-4-4-4-12
  const uuid = [
    hex.slice(0, 8),
    hex.slice(8, 12),
    hex.slice(12, 16),
    hex.slice(16, 20),
    hex.slice(20, 32),
  ].join('-');

  return uuid;
}

/**
 * Try to decode an ID that might be either UUID or Base64URL
 * Returns the UUID format
 *
 * @param id - Either UUID or Base64URL encoded ID
 * @returns UUID string
 */
export function decodeId(id: string): string {
  if (isUuid(id)) {
    return id;
  }
  if (isBase64Url(id)) {
    return base64UrlToUuid(id);
  }
  // If neither format matches, return as-is (will likely fail downstream)
  return id;
}

/**
 * Try to encode an ID that might be either UUID or Base64URL
 * Returns the Base64URL format
 *
 * @param id - Either UUID or Base64URL encoded ID
 * @returns Base64URL encoded string
 */
export function encodeId(id: string): string {
  if (isBase64Url(id)) {
    return id;
  }
  if (isUuid(id)) {
    return uuidToBase64Url(id);
  }
  // If neither format matches, return as-is
  return id;
}
