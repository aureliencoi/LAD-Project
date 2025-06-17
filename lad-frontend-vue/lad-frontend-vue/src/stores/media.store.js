import { defineStore } from 'pinia';
import api from '@/services/api.service';

export const useMediaStore = defineStore('media', {
  state: () => ({
    movies: [],
    series: [],
    // --- NOUVEAU : Pour stocker le média actuellement consulté ---
    currentMediaDetail: null, 
    isLoading: false,
    error: null,
  }),
  actions: {
    async fetchAllMedia() {
      if (this.movies.length > 0 || this.series.length > 0) return;

      this.isLoading = true;
      this.error = null;
      
      try {
        const [moviesResponse, seriesResponse] = await Promise.all([
          api.get('/api/movies'),
          api.get('/api/series')
        ]);
        
        this.movies = moviesResponse.data;
        this.series = seriesResponse.data;

      } catch (error) {
        console.error("Erreur lors de la récupération des médias:", error);
        this.error = "Impossible de charger les médias depuis le serveur.";
      } finally {
        this.isLoading = false;
      }
    },

    // --- NOUVELLE ACTION ---
    async fetchMediaDetail(type, id) {
      this.currentMediaDetail = null; // Réinitialise avant de charger
      this.isLoading = true;
      this.error = null;

      try {
        const response = await api.get(`/api/${type}/${id}`);
        this.currentMediaDetail = response.data;
      } catch (error) {
        console.error(`Erreur lors de la récupération du média ${type} ${id}:`, error);
        this.error = `Impossible de charger les détails pour ce média.`;
      } finally {
        this.isLoading = false;
      }
    }
  },
});