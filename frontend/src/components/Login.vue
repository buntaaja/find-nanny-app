<template>
    <div>
      <form @submit.prevent="submitForm">
        <label for="username_email">Username or Email:</label>
        <input v-model="username_email" type="text" id="username_email" />
        
        <label for="password">Password:</label>
        <input v-model="password" type="password" id="password" />
        
        <button type="submit">Login</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username_email: '',
        password: '',
      };
    },
    methods: {
      submitForm() {
        // Handle form submission, for example, by making an API request to your Flask backend
        console.log('Form submitted:', this.username_email, this.password);
      },
    },
  };
  </script>