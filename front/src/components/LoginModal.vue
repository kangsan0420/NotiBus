<template>
  <div>
    <b-modal ref="modal" centered hide-footer @show="initialize">
      <!-- header -->
      <template #modal-title>Login</template>

      <b-alert
        variant="danger"
        dismissible
        fade
        :show="err_msg !== ''"
        @dismissed="err_msg = false"
      >
        {{ err_msg }}
      </b-alert>

      <!-- body -->
      <template
        ><b-form @submit="onSubmit" @reset="onCancel"
          ><b-container>
            <b-row>
              <b-col class="text-right">ID:</b-col>
              <b-col cols="9">
                <b-form-group>
                  <b-form-input
                    id="input_loginId"
                    v-model="login_form.ID"
                    placeholder="Enter ID"
                    required
                  ></b-form-input>
                </b-form-group>
              </b-col>
            </b-row>
            <b-row>
              <b-col class="text-right">PW:</b-col>
              <b-col cols="9">
                <b-form-group>
                  <b-form-input
                    id="input_loginPw"
                    type="password"
                    v-model="login_form.PW"
                    placeholder="Enter password"
                    required
                  ></b-form-input>
                </b-form-group>
              </b-col>
            </b-row>
            <b-row>
              <b-col class="text-center">
                <span class="href-link">Forgot</span> /
                <span
                  class="href-link"
                  @click="$refs.modal_signup.$refs.modal.show()"
                  >Sign Up</span
                >
              </b-col>
            </b-row>
            <hr />
            <p class="text-center">
              <b-button class="mx-1" type="submit" variant="outline-primary"
                >Login</b-button
              >
              <b-button class="mx-2" type="reset" variant="outline-danger"
                >Cancel</b-button
              >
            </p>
          </b-container></b-form
        ></template
      >
    </b-modal>
    <SignupModal ref="modal_signup" />
  </div>
</template>

<script>
import axios from "axios";
import VueCookies from "vue-cookies";
import SignupModal from "./SignupModal.vue";

export default {
  name: "LoginModal",
  components: { SignupModal },
  data() {
    return {
      login_form: {
        ID: "",
        PW: "",
      },
      err_msg: "",
    };
  },
  inject: ["base_url"],
  emits: ["loginout"],
  methods: {
    openModal() {
      if (VueCookies.isKey("logon")) {
        VueCookies.remove("logon");
        this.$emit("loginout", false);
      } else {
        this.$refs.modal.show();
      }
    },
    onSubmit(event) {
      event.preventDefault();
      axios
        .post(this.base_url + "/login", this.login_form, {
          withCredentials: true,
        })
        .then((response) => {
          if (response.data.msg) {
            this.err_msg = response.data.msg;
          } else {
            this.$refs.modal.hide();
            VueCookies.set("logon", JSON.parse(response.config.data).ID);
            this.$emit("loginout", true);
          }
        });
    },
    onCancel() {
      this.$refs.modal.hide();
      this.login_form.ID = "";
      this.login_form.PW = "";
    },
    initialize() {
      this.err_msg = "";
    },
  },
};
</script>

<style lang="scss" scoped>
@import "node_modules/bootstrap/scss/bootstrap";

.href-link {
  &:hover {
    color: $primary;
  }
}
</style>
