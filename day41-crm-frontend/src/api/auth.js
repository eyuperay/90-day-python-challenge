import api from './client';

export const authAPI = {
  login: (username, password) => 
    api.post('/auth/login', { username, password }),
  register: (data) => api.post('/auth/register', data),
  me: () => api.get('/auth/me'),
};
