<template>
  <div>
    <h1>Main Page</h1>
    <!-- Navigation links -->
    <router-link to="/register">Go to Register</router-link>

    <!-- Conditionally show login or logout link -->
    <router-link v-if="!authStore.isAuthenticated" to="/login">Go to Login</router-link>
    <button v-else @click="logout">Log out</button>
  </div>
</template>

<script>
import axios from 'axios';
import { mapStores } from 'pinia'
import { useAuthStore } from '../stores/auth';

export default {
  computed: {
    ...mapStores(useAuthStore)
  },
  methods: {
    async logout() {
      try {
        // Make an API request to your backend for logout
        const response = await axios.get('http://localhost:5000/logout');

        // Check the response from the server
        if (response.data.status === 'success') {
          console.log('Logged out successfully.');
          this.authStore.logout()
        } else {
          console.error('Logout failed.');
        }
      } catch (error) {
        console.error('Error during logout:', error);
      }
    },h 
  },
};
</script>