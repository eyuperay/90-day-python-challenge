import api from './client';
export const customerAPI = { getAll: () => api.get('/customers/'), getById: (id) => api.get(/customers/), create: (data) => api.post('/customers/', data), update: (id, data) => api.put(/customers/, data), delete: (id) => api.delete(/customers/) };
