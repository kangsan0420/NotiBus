<template>
  <b-table striped hover :items="items"></b-table>
</template>

<script>
import axios from "axios";
import VueCookies from "vue-cookies";

export default {
  data() {
    return {
      items: [],
    };
  },
  inject: ["base_url"],
  mounted() {
    axios
      .get(this.base_url + "/getHistory", {
        params: {
          ID: VueCookies.get("logon"),
        },
      })
      .then((res) => {
        this.items = res.data;
      });
  },
};
</script>
