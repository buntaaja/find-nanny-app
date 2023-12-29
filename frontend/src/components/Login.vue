<template>
    <div>
      <form @submit.prevent="submitForm" action="/login" method="post">
        <label for="username_email">Email:</label>
        <input v-model="email" type="text" id="email" />
        
        <label for="password">Password:</label>
        <input v-model="password" type="password" id="password" />
        
        <button type="submit">Login</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        email: '',
        password: '',
      };
    },
    methods: {
      async submitForm() {
        try {
          // Make an API request to your backend for login
          const response = await axios.post('http://localhost:5000/login', {
            email: this.email,
            password: this.password,
          }, {
            withCredentials: true, //To allow sending cookies
          });
  
          // Check the response from the server
          if (response.data.status === 'success') {
            console.log('Logged in successfully.');
  
            // Use Vue Router to navigate to the main page
            this.$router.push('/');
  
          } else {
            console.error('Login failed.');
          }
        } catch (error) {
          console.error('Error during login:', error);
        }
      },
    },
  };
  </script>