import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const analyzeVideo = async (url) => {
  const response = await api.post('/analyze', { url });
  return response.data;
};

export const getResults = async (videoId) => {
  const response = await api.get(`/results/${videoId}`);
  return response.data;
};

export const getAnalytics = async (videoId) => {
  const response = await api.get(`/analytics/${videoId}`);
  return response.data;
};

export const generateReply = async ({ commentText, author, intent, context }) => {
  const response = await api.post('/generate-reply', {
    comment_text: commentText,
    author,
    intent,
    context
  });
  return response.data;
};

export const getHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};

export const getVideosHistory = async () => {
  const response = await api.get('/videos');
  return response.data;
};

export default api;
