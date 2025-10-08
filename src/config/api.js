// API Configuration
const API_CONFIG = {
  // Default to localhost for development
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:5001',
  
  // API endpoints
  ENDPOINTS: {
    ANALYTICS_SUBMISSIONS: '/api/analytics/submissions',
    SUBREDDIT_SUBSCRIBE: '/api/subreddits/subscribe',
    SUBMISSIONS: '/submissions',
    RECORDS: '/records',
    HEALTH: '/health'
  }
};

// Helper function to build full API URLs
export const buildApiUrl = (endpoint, ...params) => {
  const baseUrl = API_CONFIG.BASE_URL;
  const endpointPath = API_CONFIG.ENDPOINTS[endpoint];
  
  if (!endpointPath) {
    throw new Error(`Unknown endpoint: ${endpoint}`);
  }
  
  // Handle endpoints that need parameters
  if (params.length > 0) {
    return `${baseUrl}${endpointPath}/${params.join('/')}`;
  }
  
  return `${baseUrl}${endpointPath}`;
};

export default API_CONFIG;
