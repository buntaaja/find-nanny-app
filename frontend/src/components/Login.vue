<template>
  <div>
    <form @submit.prevent="submitForm" action="/login" method="post">
      <label for="username_email">Email:</label>
      <input v-model="email" type="text" id="email" />
      <label for="password">Password:</label>
      <input v-model="password" type="password" id="password" />
      
      <button type="submit">Login</button>
    </form>
    <div v-if="loginError" class="error-message">
    {{ loginError }}
    </div>
  </div>
</template>
  
<script>
import axios from 'axios';
import { mapStores } from 'pinia';
import { useAuthStore } from '../stores/auth';

export default {
  computed: {
    ...mapStores(useAuthStore)
  },
  data() {
    return {
      email: '',
      password: '',
      loginError: '',
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await axios.post('http://localhost:5000/login', {
          email: this.email,
          password: this.password,
        }, {
          withCredentials: true,
        });

        if (response.data.status === 'success') {
          console.log('Logged in successfully.');
          this.authStore.login();
        } else {
          // Check for error_message in the response
          if (response.data.error_message) {
            this.loginError = response.data.error_message;
          } else {
            // Set a generic error message if no specific message is provided
            this.loginError = 'Login failed. Please check your credentials.';
          }
        }
      } catch (error) {
        console.error('Error during login:', error);
        // Use the error message from the server if available, otherwise set a generic message
        this.loginError = error.response ? error.response.data.message : 'An unexpected error occurred during login.';
      }
    },
  },
};
</script>

<style scoped>
.error-message {
  color: red;
  margin-top: 10px;
}
</style>