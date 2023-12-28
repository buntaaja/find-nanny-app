<template>
    <div>
      <form @submit.prevent="submitForm">
        <label for="username_email">Email:</label>
        <input v-model="email" type="text" id="email" />
        
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
        email: '',
        password: '',
      };
    },
    methods: {
      submitForm() {
        // Handle form submission, for example, by making an API request to your Flask backend
        console.log('Form submitted:', this.email, this.password);
      },
    },
  };
  </script>