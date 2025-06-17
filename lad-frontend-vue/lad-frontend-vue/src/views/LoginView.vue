<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="title">Connexion à LAD</h1>
      <p class="subtitle">Libraries Assets Designer</p>

      <div class="form">
        <input class="input-field" v-model="username" placeholder="Nom d'utilisateur" @keyup.enter="handleLogin">
        <input class="input-field" v-model="password" type="password" placeholder="Mot de passe" @keyup.enter="handleLogin">
      </div>
      
      <div v-if="authStore.errorMessage" class="error-message">
        {{ authStore.errorMessage }}
      </div>

      <button class="login-button" @click="handleLogin" :disabled="authStore.isLoading">
        <span v-if="!authStore.isLoading">Se connecter</span>
        <span v-else>Connexion...</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.store';

const username = ref('');
const password = ref('');
const authStore = useAuthStore();

const handleLogin = () => {
  if (username.value && password.value) {
    authStore.login(username.value, password.value);
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: radial-gradient(circle, #2a2a2a, #121212);
}
.login-card {
  background-color: #242424;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
  width: 100%;
  max-width: 400px;
  text-align: center;
}
.title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: #fff;
}
.subtitle {
  color: #a0a0a0;
  margin-bottom: 30px;
}
.form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 20px;
}
.input-field {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #444;
  background-color: #333;
  color: #fff;
  font-size: 1rem;
}
.login-button {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: none;
  background-color: #4f46e5;
  color: #fff;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}
.login-button:disabled {
  background-color: #555;
  cursor: not-allowed;
}
.login-button:hover:not(:disabled) {
  background-color: #4338ca;
}
.error-message {
  color: #ef4444;
  margin-bottom: 15px;
}
</style>