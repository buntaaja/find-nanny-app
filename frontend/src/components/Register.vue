<template>
  <div>
    <div class="_reg">
      <div class="_reg2">
        <!-- Your image and title -->
        <img src="https://static.xx.fbcdn.net/rsrc.php/v3/yZ/r/C6QZ-pcv3Bd.png" alt="" width="24" height="24" id="x_sign" />
        <div class="sign_up">
          <div class="sign_up2">Sign Up</div>
        </div>

        <!-- Your form -->
        <form @submit.prevent="submitForm" method="post" id="reg">
          <!-- Alert Message -->
          <div v-if="showMessage" class="alert alert-success" role="alert">
            {{ message }}
          </div>
          <!-- First name and Last name -->
          <div>
            <input type="text" name="firstName" v-model="formData.firstName" placeholder="First Name"/>
          </div>
          <div>
            <input type="text" name="lastName" v-model="formData.lastName" placeholder="Last Name" />
          </div>

          <!-- Email -->
          <div>
            <input type="text" name="email" v-model="formData.email" placeholder="Email" />
          </div>

          <!-- Password -->
          <div>
            <input type="password" name="password" v-model="formData.password" placeholder="Password" />
          </div>

          <!-- Confirm Password -->
          <div>
            <input type="password" name="confirm_pasword" v-model="formData.confirm_password" placeholder="Confirm Password" />
          </div>

          <!-- Birthday -->
          <div>
            <div>Birthday</div>
            <div>
              <label for="birthdayMonth">Month:</label>
              <select id="birthdayMonth" name="birthday_month" title="Month" v-model="formData.birthdayMonth">
                <option value="01">January</option>
                <option value="02">February</option>
                <option value="03">March</option>
                <option value="04">April</option>
                <option value="05">May</option>
                <option value="06">June</option>
                <option value="07">July</option>
                <option value="08">August</option>
                <option value="09">September</option>
                <option value="10">October</option>
                <option value="11">November</option>
                <option value="12">December</option>
              </select>

              <label for="birthdayDay">Day:</label>
              <select id="birthdayDay" name="birthday_day" title="Day" v-model="formData.birthdayDay">
                <option v-for="day in 31" :key="day" :value="day">{{ day }}</option>
              </select>

              <label for="birthdayYear">Year:</label>
              <select id="birthdayYear" name="birthday_year" title="Year" v-model="formData.birthdayYear">
                <!-- Add your year options here -->
                <option v-for="year in years.slice().reverse()" :key="year" :value="year">{{ year }}</option>
              </select>
            </div>
          </div>

          <!-- Gender -->
          <div>
            <div>Gender</div>
            <div>
              <label>
                <input type="radio" name="gender" value="female" v-model="formData.gender" />
                Female
              </label>

              <label>
                <input type="radio" name="gender" value="male" v-model="formData.gender" />
                Male
              </label>

              <label>
                <input type="radio" name="gender" value="other" v-model="formData.gender" />
                Other
              </label>
            </div>
          </div>

          <!-- Sign Up button -->
          <div class="">
            <button type="submit">Sign Up</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    const currentYear = new Date().getFullYear();
    const startYear = 1920;
    const years = Array.from({ length: currentYear - startYear + 1 }, (_, index) => (startYear + index).toString());

    return {
      formData: {
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirm_password: '',
        birthdayMonth: '',
        birthdayDay: '',
        birthdayYear: '',
        gender: ''
      },
      years: years,
      showMessage: false, // define showMessage
      message: ''
    };
  },
  methods: {
    submitForm() {
      const payload = {
        firstName: this.formData.firstName,
        lastName: this.formData.lastName,
        email: this.formData.email,
        password: this.formData.password,
        confirm_password: this.formData.confirm_password,
        birthday_month: this.formData.birthdayMonth,
        birthday_day: this.formData.birthdayDay,
        birthday_year: this.formData.birthdayYear,
        gender: this.formData.gender,
      };
      console.log('Payload:', this.formData);
      const path = "http://localhost:5000/register";
      axios
        .post(path, payload, {
          headers: {
              'Content-Type': 'application/json',
          },
        })
        .then((res) => {
          // Set notification message
          this.message = res.data.message;
          // Show notification
          this.showMessage = true;
          // Redirect them to login page
          this.$router.push("/login");

          // Notify MainPage component that the user has registered
          this.$emit('userRegistered', payload);
        })
        .catch((error) => {
          console.error(error);
          // If registration fails, show an error message
          this.message = "Registration failed. Please try again.";
          this.showMessage = true;
          this.$router.push("/register");
        });
      },
  },
};
</script>