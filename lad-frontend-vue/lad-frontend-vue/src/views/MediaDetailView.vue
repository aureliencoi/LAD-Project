<template>
  <div v-if="mediaStore.isLoading" class="loading-full-page">Chargement...</div>
  <div v-else-if="mediaStore.error" class="error-full-page">{{ mediaStore.error }}</div>
  
  <div v-else-if="media" class="detail-page">
    <div class="page-background" :style="{ backgroundImage: pageBackgroundUrl ? 'url(' + pageBackgroundUrl + ')' : 'none' }">
      <div class="page-overlay"></div>
    </div>

    <h1>{{ media.title }} ({{ media.year }})</h1>
    <p>{{ media.overview }}</p>

    </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { useMediaStore } from '@/stores/media.store';

const route = useRoute();
const mediaStore = useMediaStore();

// Propriété "calculée" qui renvoie le média actuel du store
const media = computed(() => mediaStore.currentMediaDetail);

// Propriété "calculée" pour l'URL de l'arrière-plan
const pageBackgroundUrl = computed(() => {
  const backdrops = media.value?.tmdb_images?.backdrops;
  if (backdrops && backdrops.length > 0) {
    return 'https://image.tmdb.org/t/p/original' + backdrops[0].file_path;
  }
  return null;
});

// Quand le composant est affiché, on lance la récupération des données
onMounted(() => {
  const type = route.path.startsWith('/movie') ? 'movie' : 'series';
  const id = route.params.id;
  mediaStore.fetchMediaDetail(type, id);
});
</script>

<style scoped>
.loading-full-page, .error-full-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  font-size: 2rem;
}
.error-full-page {
  color: #ef4444;
}
.page-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center center;
  z-index: -2;
  transition: background-image 0.5s ease-in-out;
}
.page-overlay {
  width: 100%;
  height: 100%;
  background-color: rgba(18, 18, 18, 0.8);
  backdrop-filter: blur(10px);
  z-index: -1;
}
.detail-page {
  padding: 80px 40px 40px 40px;
}
</style>