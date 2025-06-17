import axios from 'axios';
import { useAuthStore } from '@/stores/auth.store';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', // L'URL de base de notre backend
});

// Intercepteur : s'exécute avant chaque requête envoyée par ce service
api.interceptors.request.use(config => {
  const authStore = useAuthStore();
  const token = authStore.token;

  if (token) {
    // Si un token existe, on l'ajoute dans les en-têtes
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

export default api;