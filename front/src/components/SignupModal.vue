<template>
  <div>
    <b-modal ref="modal" centered hide-footer>
      <!-- header -->
      <template #modal-title>Sign Up</template>

      <b-alert
        variant="danger"
        dismissible
        fade
        :show="err_msg !== ''"
        @dismissed="err_msg = ''"
      >
        {{ err_msg }}
      </b-alert>

      <!-- body -->
      <template>
        <b-form @submit="onSubmit" @reset="onCancel">
          <b-container>
            <b-row>
              <b-col cols="2"> ID: </b-col>
              <b-col cols="8">
                <b-form-group
                  label-for="input_signupId"
                  :invalid-feedback="invalidFeedback('ID')"
                >
                  <b-form-input
                    id="input_signupId"
                    v-model="signup_form.ID"
                    placeholder="Enter ID"
                    :state="lengthMinimum('ID')"
                    trim
                    required
                    @input="validity.ID = false"
                  ></b-form-input>
                </b-form-group>
              </b-col>
              <b-col cols="2">
                <b-button @click="checkID">Check</b-button>
              </b-col>
            </b-row>
            <b-row>
              <b-col cols="2">PW:</b-col>
              <b-col cols="8">
                <b-form-group
                  label-for="input_signupPw"
                  :invalid-feedback="invalidFeedback('PW')"
                >
                  <b-form-input
                    id="input_signupPw"
                    type="password"
                    v-model="signup_form.PW"
                    placeholder="Enter password"
                    :state="lengthMinimum('PW')"
                    required
                  ></b-form-input>
                </b-form-group>
              </b-col>
              <b-col cols="2"></b-col>
            </b-row>
            <b-row>
              <b-col cols="2"></b-col>
              <b-col cols="8">
                <b-form-group
                  id="group_pw2"
                  label-for="input_signupPw2"
                  :invalid-feedback="invalidFeedback('PW2')"
                >
                  <b-form-input
                    id="input_signupPw2"
                    type="password"
                    v-model="signup_form.PW2"
                    placeholder="Enter password again"
                    :state="lengthMinimum('PW2')"
                    required
                  ></b-form-input>
                </b-form-group>
              </b-col>
              <b-col cols="2"></b-col>
            </b-row>
            <hr />
            <h6>API Key</h6>
            <b-row>
              <b-col cols="2"> data.org: </b-col>
              <b-col cols="8">
                <b-form-group description=" ">
                  <b-form-input
                    v-model="signup_form.api_data"
                    placeholder="Enter API Key from data.org"
                  ></b-form-input>
                </b-form-group>
              </b-col>
              <b-col cols="2">
                <b-button>Check</b-button>
              </b-col>
            </b-row>
            <b-row>
              <b-col cols="2"> nCloud: </b-col>
              <b-col cols="8">
                <b-form-group description=" ">
                  <b-form-input
                    v-model="signup_form.api_ncloud"
                    placeholder="Enter API Key from nCloud"
                  ></b-form-input>
                </b-form-group>
              </b-col>
              <b-col cols="2">
                <b-button>Check</b-button>
              </b-col>
            </b-row>
            <hr />
            <p class="text-center">
              <b-button class="mx-1" type="submit" variant="outline-primary"
                >Sign Up</b-button
              >
              <b-button class="mx-1" type="reset" variant="outline-danger"
                >Cancel</b-button
              >
            </p>
          </b-container>
        </b-form>
      </template>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SignupModal",
  data() {
    return {
      signup_form: {
        ID: "",
        PW: "",
        PW2: "",
        api_data: "",
        api_ncloud: "",
      },
      validity: {
        ID: false,
        api_data: false,
        api_ncloud: false,
      },
      err_msg: "",
    };
  },
  computed: {
    lengthMinimum() {
      return (name) => {
        let isValid =
          this.signup_form[name].length >= 4 &&
          this.signup_form[name].length <= 16;
        if (name === "ID") {
          isValid = isValid && this.validity.ID;
        } else if (name === "PW2") {
          isValid = isValid && this.signup_form.PW === this.signup_form.PW2;
        }
        return isValid;
      };
    },
    invalidFeedback() {
      return (name) => {
        if (this.signup_form[name].length === 0) {
          return null;
        } else if (this.signup_form[name].length < 4) {
          return "Enter at least 4 characters.";
        } else {
          if (name === "ID") {
            return "Check Validity";
          } else if (name === "PW2") {
            return "Should be same value for passwords.";
          }
        }
      };
    },
  },
  inject: ["base_url"],
  methods: {
    checkID() {
      if (document.getElementById("input_signupId").value.length >= 4) {
        axios
          .post(this.base_url + "/checkId", this.signup_form)
          .then((response) => {
            let exist = response.data;
            if (exist) {
              this.err_msg = "ID already exists!";
            } else {
              this.validity.ID = true;
              this.err_msg = "";
            }
          })
          .catch((error) => {
            if (!error.response) {
              // network error
              this.errorStatus = "Error: Network Error";
            } else {
              this.errorStatus = error.response.data.message;
            }
          });
      }
    },
    onSubmit(event) {
      event.preventDefault();
      if (
        document.querySelector("#input_signupId").__vue__.state &&
        document.querySelector("#input_signupPw").__vue__.state &&
        document.querySelector("#input_signupPw2").__vue__.state
      ) {
        axios
          .post(this.base_url + "/signup", this.signup_form)
          .then((response) => {
            console.log("Signup Success:", response.data);
            this.reset_form();
          });
        this.$refs.modal.hide();
      } else {
        this.err_msg = "Check ID & Pw first!";
      }
    },
    onCancel() {
      this.$refs.modal.hide();
      this.reset_form();
    },
    reset_form() {
      this.signup_form = {
        ID: "",
        PW: "",
        PW2: "",
        api_data: "",
        api_ncloud: "",
      };
      this.validity = {
        ID: false,
        api_data: false,
        api_ncloud: false,
      };
    },
  },
};
</script>
