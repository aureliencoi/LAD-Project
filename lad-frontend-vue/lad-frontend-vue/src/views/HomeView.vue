<template>
  <div class="home-container">
    <h1>Mes Médias</h1>

    <div v-if="mediaStore.isLoading && mediaStore.movies.length === 0" class="loading">Chargement...</div>
    <div v-if="mediaStore.error" class="error">{{ mediaStore.error }}</div>

    <div v-if="!mediaStore.isLoading && !mediaStore.error">
      <h2>Films</h2>
      <div v-if="mediaStore.movies.length > 0" class="media-grid">
        <RouterLink v-for="movie in mediaStore.movies" :key="movie.id" :to="`/movie/${movie.id}`" class="media-card">
          <img :src="movie.poster_url" :alt="movie.title" />
          <div class="media-title">{{ movie.title }}</div>
        </RouterLink>
      </div>
      <p v-else>Aucun film trouvé. Veuillez configurer Radarr.</p>

      <hr />

      <h2>Séries</h2>
      <div v-if="mediaStore.series.length > 0" class="media-grid">
        <RouterLink v-for="seriesItem in mediaStore.series" :key="seriesItem.id" :to="`/series/${seriesItem.id}`" class="media-card">
          <img :src="seriesItem.poster_url" :alt="seriesItem.title" />
          <div class="media-title">{{ seriesItem.title }}</div>
        </RouterLink>
      </div>
      <p v-else>Aucune série trouvée. Veuillez configurer Sonarr.</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useMediaStore } from '@/stores/media.store';
import { RouterLink } from 'vue-router'; // N'oubliez pas d'importer RouterLink

const mediaStore = useMediaStore();

onMounted(() => {
  mediaStore.fetchAllMedia();
});
</script>

<style scoped>
.home-container {
  padding: 20px 40px;
}
h1, h2 {
  color: #fff;
  border-bottom: 1px solid #444;
  padding-bottom: 10px;
  margin-bottom: 20px;
}
.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
}
.media-card {
  text-decoration: none; /* Enlève le soulignement des liens */
  color: inherit; /* Utilise la couleur de texte parente */
  background-color: #2a2a2a;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
  transition: transform 0.2s ease-in-out;
}
.media-card:hover {
  transform: scale(1.05);
}
.media-card img {
  width: 100%;
  height: auto;
  display: block;
}
.media-title {
  padding: 10px;
  font-size: 0.9rem;
  text-align: center;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.loading, .error {
  font-size: 1.2rem;
  text-align: center;
  padding: 50px;
}
.error {
  color: #ef4444;
}
</style>