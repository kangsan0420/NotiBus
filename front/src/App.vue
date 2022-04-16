<template>
  <div id="app">
    <NavBar
      ref="nav_bar"
      @loginChanged="loginChanged()"
      @clickHistory="historyChanged()"
      @settingChanged="settingChanged()"
      :is_history="is_history_mode"
    />
    <MainView v-if="is_logon && !is_history_mode" ref="main_view" />
    <HistoryView v-else-if="is_logon && is_history_mode" ref="history_view" />
    <b-alert v-else variant="info" class="text-center" show
      ><b-spinner small label="Spinning"></b-spinner> Login First.
    </b-alert>
  </div>
</template>

<script>
import NavBar from "./components/NavBar.vue";
import MainView from "./components/MainView.vue";
import HistoryView from "./components/HistoryView.vue";
import VueCookies from "vue-cookies";
// import axios from "axios";

export default {
  name: "App",
  components: {
    NavBar,
    MainView,
    HistoryView,
  },
  data() {
    return {
      is_logon: false,
      is_history_mode: false,
      base_url: "http://192.168.74.187:9026",
    };
  },
  provide() {
    return {
      base_url: this.base_url,
    };
  },
  mounted() {
    // VueCookies.set("logon", "kslee");
    // this.$refs.nav_bar.isLogon = true;
  },
  methods: {
    loginChanged() {
      this.is_logon = VueCookies.isKey("logon");
    },
    historyChanged() {
      if (this.is_logon) {
        if (!this.is_history_mode) {
          this.$refs.main_view.stopAll();
        }
        this.is_history_mode = !this.is_history_mode;
      }
    },
    settingChanged() {
      this.$refs.main_view.mainRequest();
      this.$refs.main_view.initTimerSec();
    },
  },
};
</script>

<style lang="scss"></style>
