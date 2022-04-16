<template>
  <div>
    <b-navbar variant="light">
      <b-navbar-brand tag="h1" class="mb-0">Notibus</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item href="#">
            <b-button
              pill
              variant="light"
              title="login"
              @click="$refs.modal_login.openModal()"
            >
              {{ !this.isLogon ? "Login" : "Logout" }}
            </b-button>
          </b-nav-item>
          <b-nav-item>
            <b-button pill variant="light" title="history">
              <b-icon
                icon="clock-history"
                :variant="is_history ? 'primary' : 'default'"
                @click="$emit('clickHistory')"
                aria-hidden="true"
              ></b-icon>
            </b-button>
          </b-nav-item>
          <b-nav-item id="nav_setting" :disabled="!this.isLogon">
            <b-button
              pill
              variant="light"
              title="setting"
              @click="$refs.modal_setting.$refs.modal.show()"
            >
              <b-icon
                icon="gear-fill"
                :variant="is_onSetting ? 'primary' : 'default'"
                aria-hidden="true"
              ></b-icon>
            </b-button>
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <LoginModal ref="modal_login" @loginout="loginStatusChanged" />
    <SettingModal
      @openChanged="onSettingChanged"
      ref="modal_setting"
      @settingChanged="$emit('loginChanged')"
    />
  </div>
</template>

<script>
import LoginModal from "./LoginModal.vue";
import SettingModal from "./SettingModal.vue";

export default {
  name: "NavBar",
  components: { LoginModal, SettingModal },
  data() {
    return {
      isLogon: false,
      is_onSetting: false,
    };
  },
  emits: ["loginChanged", "clickHistory", "settingChanged"],
  props: ["is_history"],
  methods: {
    loginStatusChanged(status) {
      this.isLogon = status;
      this.$emit("loginChanged");
    },
    onSettingChanged(status) {
      this.is_onSetting = status;
      this.$emit("settingChanged");
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss"></style>
