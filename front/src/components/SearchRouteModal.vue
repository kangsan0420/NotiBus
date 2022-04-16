<template>
  <div>
    <b-modal ref="modal" size="lg" centered hide-footer @show="onLoad">
      <!-- header -->
      <template #modal-title>Search Route</template>
      <h1></h1>
      <hr />

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
        <b-container>
          <b-row align-h="center">
            <b-button
              class="mx-1"
              type="submit"
              :variant="selected_item ? 'outline-primary' : 'outline-secondary'"
              :disabled="!selected_item"
              @click="onSelect"
              >Select</b-button
            >
            <b-button
              class="mx-1"
              variant="outline-danger"
              @click="$refs.modal.hide()"
              >Cancel</b-button
            >
          </b-row>
          <b-row><hr /></b-row>
        </b-container>
        <b-table
          :items="route_list"
          :fields="fields"
          selectable
          select-mode="single"
          @row-selected="onRowSelected"
        />
      </template>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      err_msg: "",
      route_list: [],
      fields: [
        { key: "regionName", label: "지역" },
        { key: "routeName", label: "노선명" },
        { key: "routeTypeName", label: "타입" },
        { key: "routeId", label: "노선ID" },
      ],
      selected_item: undefined,
    };
  },
  props: ["key_data", "stId", "mbNo"],
  inject: ["base_url"],
  emits: ["select_route"],
  methods: {
    onSelect() {
      this.$emit("select_route", this.selected_item["routeId"]);
      this.$refs.modal.hide();
    },
    onRowSelected(item) {
      this.selected_item = item[0];
    },
    onLoad() {
      axios
        .post(this.base_url + "/searchRoute", {
          KEY: this.key_data,
          ITEM1: this.stId,
          ITEM2: this.mbNo,
        })
        .catch((error) => {
          console.log("Error on searchRoute:", error.request);
          console.log(error.message);
        })
        .then((res) => {
          if (!res.data.success) {
            this.err_msg = "Error: " + res.data.data;
          } else {
            this.err_msg = "";
            this.route_list = res.data.data;
          }
        });
    },
  },
};
</script>
