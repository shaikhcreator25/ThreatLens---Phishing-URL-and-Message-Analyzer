/**
 * PhishGuard AI — API Service
 *
 * Handles communication with the FastAPI backend.
 * All analysis logic lives server-side; this is a thin fetch wrapper.
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Analyze a suspicious message and/or URL.
 *
 * @param {{ message?: string, url?: string }} payload
 * @returns {Promise<{
 *   classification: string,
 *   risk_score: number,
 *   message_score: number,
 *   url_score: number,
 *   reasons: string[]
 * }>}
 */
export async function analyzeThreats({ message, url }) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 15000); // 15s timeout

  try {
    const response = await fetch(`${API_URL}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: message || '', url: url || '' }),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      const detail = errorData?.detail || `Server error (${response.status})`;
      throw new Error(detail);
    }

    return await response.json();
  } catch (err) {
    clearTimeout(timeoutId);

    if (err.name === 'AbortError') {
      throw new Error('Request timed out. Please check if the backend is running.');
    }
    if (err.message === 'Failed to fetch') {
      throw new Error('Cannot connect to the backend. Please ensure the server is running on ' + API_URL);
    }
    throw err;
  }
}

/**
 * Health check.
 * @returns {Promise<{ status: string }>}
 */
export async function checkHealth() {
  const response = await fetch(`${API_URL}/health`);
  if (!response.ok) throw new Error('Health check failed');
  return response.json();
}
