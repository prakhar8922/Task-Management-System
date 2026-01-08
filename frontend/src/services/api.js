import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/users/token/refresh/`, {
            refresh: refreshToken,
          });
          
          const { access } = response.data;
          localStorage.setItem('access_token', access);
          
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/users/register/', data),
  login: (data) => api.post('/users/token/', data),
  getProfile: () => api.get('/users/profile/'),
  updateProfile: (data) => api.patch('/users/profile/', data),
};

// Projects API
export const projectsAPI = {
  list: () => api.get('/projects/'),
  create: (data) => api.post('/projects/', data),
  get: (id) => api.get(`/projects/${id}/`),
  update: (id, data) => api.patch(`/projects/${id}/`, data),
  delete: (id) => api.delete(`/projects/${id}/`),
  addMember: (id, userId) => api.post(`/projects/${id}/add_member/`, { user_id: userId }),
  removeMember: (id, userId) => api.post(`/projects/${id}/remove_member/`, { user_id: userId }),
};

// Tasks API
export const tasksAPI = {
  list: (params = {}) => api.get('/tasks/', { params }),
  create: (data) => api.post('/tasks/', data),
  get: (id) => api.get(`/tasks/${id}/`),
  update: (id, data) => api.patch(`/tasks/${id}/`, data),
  delete: (id) => api.delete(`/tasks/${id}/`),
};

// Tags API
export const tagsAPI = {
  list: () => api.get('/tasks/tags/'),
  create: (data) => api.post('/tasks/tags/', data),
};

// Comments API
export const commentsAPI = {
  list: (taskId) => api.get('/tasks/comments/', { params: { task: taskId } }),
  create: (data) => api.post('/tasks/comments/', data),
  update: (id, data) => api.patch(`/tasks/comments/${id}/`, data),
  delete: (id) => api.delete(`/tasks/comments/${id}/`),
};

export default api;
