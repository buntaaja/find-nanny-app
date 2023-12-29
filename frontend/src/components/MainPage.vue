<template>
  <div>
      <h1>Main Page</h1>
      <!-- Example navigation links -->
      <router-link to="/register">Go to Register</router-link>

      <!-- Conditionally show login or logout link -->
      <template v-if="!current_user.is_authenticated">
          <router-link to="/login">Go to Login</router-link>
      </template>
      <template v-else>
          <button @click="logout">Log out</button>
      </template>

      <router-view></router-view>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  computed: {
    current_user() {
      // Access the current user object from your backend
      return this.$store.state.current_user;
    },
  },
  methods: {
    async logout() {
      try {
        // Make an API request to your backend for logout
        const response = await axios.get('http://localhost:5000/logout');

        // Check the response from the server
        if (response.data.status === 'success') {
          console.log('Logged out successfully.');
        // Something went wrong
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