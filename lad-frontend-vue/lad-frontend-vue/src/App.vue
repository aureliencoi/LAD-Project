<template>
  <RouterView />
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router';
</script>

<style>
/* On peut mettre ici des styles vraiment globaux si besoin */
body {
  margin: 0;
  font-family: 'Inter', sans-serif; /* Assurez-vous d'importer la police */
  background-color: #121212;
  color: #e0e0e0;
}
</style>