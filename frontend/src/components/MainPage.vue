<template>
  <div class="main-container">
    <div class="navbar">
      <!-- Conditionally show login, register, or logout link -->
      <router-link v-if="!authStore.isAuthenticated" class="nav-link" to="/login">Go to Login</router-link>
      <router-link v-if="!authStore.isAuthenticated" class="nav-link" to="/register">Go to Register</router-link>
      <button v-else @click="logout" class="nav-button">Log out</button>
    </div>

    <div class="header">
      <h1>Find a Nanny!</h1>
    </div>

    <div class="content" v-if="!authStore.isAuthenticated">
      <div class="left-content">
        <h2>Are You Looking for a Nanny to take care of your kids while you go out on a date, brunch, shopping?</h2>
        <router-link class="find-nanny" to="/register">Register now to Find a Nanny</router-link>
      </div>

      <div class="right-content">
        <h2>Are you Looking to Become a Nanny?</h2>
        <h3>Do you have spare time? Do you love kids?</h3>
        <router-link class="nav-link" to="/register">Register now to Become a Nanny</router-link>
      </div>
    </div>

    <div v-if="authStore.isAuthenticated" class="authenticated-links">
      <div>
        <router-link class="find-nanny" to="/FindNanny">Look For Nanny</router-link>
      </div>

      <div>
        <router-link class="be-nanny" to="/BeNanny">Look For Nanny Jobs</router-link>
      </div>
    </div>
    
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
    },
  },
};
</script>

<style scoped>
body, html {
  margin: 0;
  padding: 0;
  height: 100%;
}
.main-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.navbar {
  position: absolute;
  top: 0;
  right: 0;
  padding: 10px;
  display: flex;
}

.nav-link {
  margin-right: 10px;
  text-decoration: none;
  color: #333; /* Adjust the color as needed */
}

.nav-button {
  padding: 8px 12px;
  background-color: #3498db; /* Adjust the color as needed */
  color: #fff; /* Adjust the color as needed */
  border: none;
  cursor: pointer;
}

.header {
  margin-top: 20px;
}

h1 {
  text-align: center;
}

.content {
  display: flex;
  justify-content: space-between;
  max-width: 800px;
  width: 100%;
  margin: 20px 0;
}

.left-content {
  width: 45%;
}

.right-content {
  width: 45%;
}
</style>