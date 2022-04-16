<template>
  <div>
    <b-modal ref="modal" size="lg" centered hide-footer>
      <!-- header -->
      <template #modal-title>Search by Station Name</template>

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
        <b-form @submit="onSubmit">
          <b-container>
            <b-row>
              <b-col cols="1"></b-col>
              <b-col cols="8">
                <b-form-input
                  v-model="station_name"
                  placeholder="한글 역명"
                ></b-form-input>
              </b-col>
              <b-col cols="1">
                <b-button variant="primary" @click="onSearch">Search</b-button>
              </b-col>
              <b-col cols="1"></b-col>
            </b-row>

            <b-row>
              <MapCard
                :service_key="key_ncloud"
                :obj="item"
                :item_id="item.stationId"
                v-for="item in station_list"
                :key="item.stationId"
                :size="300"
                @click="onCardClick"
                @selected="onSelected"
                :ref="item.stationId"
              />
            </b-row>

            <div v-if="show_footer">
              <hr />
              <p class="text-center">
                <b-button class="mx-1" type="submit" variant="outline-primary"
                  >Save</b-button
                >
                <b-button
                  class="mx-1"
                  type="reset"
                  variant="outline-danger"
                  @click="onCancel"
                  >Cancel</b-button
                >
              </p>
            </div>
          </b-container>
        </b-form>
      </template>
    </b-modal>
  </div>
</template>

<script>
import axios from "axios";
import MapCard from "./NaverDynamicMap.vue";

export default {
  data() {
    return {
      station_name: "",
      err_msg: "",
      show_footer: false,
      station_list: [],
      selected: null,
    };
  },
  components: { MapCard },
  props: ["key_data", "key_ncloud"],
  inject: ["base_url"],
  emits: ["select_station"],
  methods: {
    onSelected(station_id, mobile_no) {
      this.$refs.modal.hide();
      this.$emit("select_station", station_id, mobile_no);
    },
    onCardClick(item_id) {
      if (this.selected) {
        this.$refs[this.selected][0].deSelect();
      }
      this.selected = item_id;
      this.$refs[this.selected][0].select();
    },
    onSearch(event) {
      event.preventDefault();
      axios
        .post(this.base_url + "/searchByStationName", {
          KEY: this.key_data,
          ITEM: this.station_name,
        })
        .catch((error) => {
          console.log("Error on searchByStationName:", error.request);
          console.log(error.message);
        })
        .then((res) => {
          if (!res.data.success) {
            this.err_msg = "Error: " + res.data.data;
          } else {
            this.err_msg = "";
            this.station_list = res.data.data;
          }
        });
    },
    onSubmit() {
      //
    },
    onCancel() {
      //
    },
  },
};
</script>
