import { defineStore } from 'pinia'
import axios from 'axios'
import router from '@/router'

const backendUrl = 'http://127.0.0.1:8000';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('access_token') || null,
    errorMessage: '',
    isLoading: false,
  }),
  actions: {
    async login(username, password) {
      this.isLoading = true;
      this.errorMessage = '';

      const body = new URLSearchParams();
      body.set('username', username);
      body.set('password', password);
      
      try {
        const response = await axios.post(`${backendUrl}/auth/token`, body, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });

        // --- ESPION FRONTEND ---
        // On affiche dans la console du navigateur la réponse exacte du backend
        console.log('[FRONTEND DEBUG] Réponse reçue du backend :', response);
        console.log('[FRONTEND DEBUG] Contenu de response.data :', response.data);

        const token = response.data.access_token;
        
        // On vérifie si le token a bien été trouvé
        if (!token) {
          throw new Error("Le token n'a pas été trouvé dans la réponse du serveur.");
        }

        this.token = token;
        localStorage.setItem('access_token', token);
        
        // Redirection vers la page d'accueil après connexion
        await router.push('/home');

      } catch (error) {
        this.errorMessage = 'Nom d\'utilisateur ou mot de passe incorrect.';
        console.error('Erreur de connexion:', error);
      } finally {
        this.isLoading = false;
      }
    },
    logout() {
      this.token = null;
      localStorage.removeItem('access_token');
      router.push('/login');
    }
  },
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
});