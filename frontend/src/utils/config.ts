// Configuration for API endpoints and other global settings

// Get the API base URL from environment variables or use a default
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Function to get the full URL for website previews
export const getFullWebsiteUrl = (relativeUrl: string): string => {
  if (!relativeUrl) return '';
  
  // If the URL is already absolute (starts with http), return it as is
  if (relativeUrl.startsWith('http')) {
    return relativeUrl;
  }
  
  // Otherwise, prepend the API base URL
  return `${API_BASE_URL}${relativeUrl}`;
};
