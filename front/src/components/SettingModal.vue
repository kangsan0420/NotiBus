<template>
  <div>
    <b-modal
      ref="modal"
      v-model="is_open"
      size="lg"
      centered
      hide-footer
      @show="onLoad"
    >
      <!-- header -->
      <template #modal-title>
        <b-container>
          <b-row>
            <b-col class="text-left">Setting</b-col>
            <b-col class="text-right"
              ><b-button variant="outline-dark">
                <b-icon
                  icon="question-circle"
                  @click="$refs.modal_help.$refs.modal.show()"
                ></b-icon>
              </b-button>
            </b-col>
          </b-row>
        </b-container>
      </template>

      <b-alert
        :variant="alert_type"
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
            <b-row class="my-1">
              <b-col cols="2">data.go.kr</b-col>
              <b-col cols="8">
                <b-form-input
                  v-model="setting_form.api_data"
                  placeholder='data.go.kr "경기도_정류소 조회"의 "일반 인증키(Decoding)"'
                ></b-form-input>
              </b-col>
              <b-col cols="2">
                <b-button @click="validate_api_data">Check</b-button>
              </b-col>
            </b-row>

            <b-row class="my-1">
              <b-col cols="2">nCloud</b-col>
              <b-col cols="8">
                <b-form-input v-model="setting_form.api_ncloud"></b-form-input>
              </b-col>
              <b-col cols="2">
                <b-button @click="validate_api_nCloud">Check</b-button>
              </b-col>
            </b-row>

            <b-row class="my-1">
              <b-col cols="2">Alarm</b-col>
              <b-col cols="8">
                <b-input-group append="minute">
                  <b-form-input v-model="setting_form.alarm_min"></b-form-input>
                </b-input-group>
              </b-col>
              <b-col cols="2"> </b-col>
            </b-row>

            <b-row class="my-1">
              <b-col cols="2">Station</b-col>
              <b-col cols="3">
                <b-form-input v-model="setting_form.station_id"></b-form-input>
              </b-col>
              <b-col cols="2">Code</b-col>
              <b-col cols="3">
                <b-form-input v-model="setting_form.mobile_no"></b-form-input>
              </b-col>
              <b-col cols="2">
                <b-button @click="$refs.modal_ss.$refs.modal.show()"
                  >Search</b-button
                >
              </b-col>
            </b-row>

            <b-row class="my-1">
              <b-col cols="2">Route</b-col>
              <b-col cols="8">
                <b-form-input v-model="setting_form.route"></b-form-input>
              </b-col>
              <b-col cols="2">
                <b-button
                  @click="$refs.modal_sr.$refs.modal.show()"
                  :disabled="
                    !setting_form.station_id ||
                    setting_form.station_id.length === 0
                  "
                  >Search</b-button
                >
              </b-col>
            </b-row>

            <b-row class="my-1">
              <b-col cols="2">Request</b-col>
              <b-col cols="8">
                <b-input-group append="second">
                  <b-form-input v-model="setting_form.req_term"></b-form-input>
                </b-input-group>
              </b-col>
              <b-col cols="2"> </b-col>
            </b-row>
            <hr />
            <p class="text-center">
              <b-button
                class="mx-1"
                type="submit"
                :variant="
                  changed <= 1 ? 'outline-secondary' : 'outline-primary'
                "
                :disabled="changed <= 1"
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
          </b-container>
        </b-form>
      </template>
    </b-modal>
    <SearchStationModal
      ref="modal_ss"
      :key_data="setting_form.api_data"
      :key_ncloud="setting_form.api_ncloud"
      @select_station="onSelectStation"
    />
    <SearchRouteModal
      ref="modal_sr"
      :stId="setting_form.station_id"
      :mbNo="setting_form.mobile_no"
      :key_data="setting_form.api_data"
      @select_route="onSelectRoute"
    />
    <HelpModal ref="modal_help" />
  </div>
</template>

<script>
import axios from "axios";
import VueCookies from "vue-cookies";
import SearchStationModal from "./SearchStationModal.vue";
import SearchRouteModal from "./SearchRouteModal.vue";
import HelpModal from "./HelpModal.vue";

export default {
  components: { SearchStationModal, SearchRouteModal, HelpModal },
  data() {
    return {
      alert_type: "danger",
      err_msg: "",
      setting_form: {
        api_data: "",
        api_ncloud: "",
        alarm_min: "",
        station_id: "",
        mobile_no: "",
        route: "",
        req_term: "",
      },
      changed: 0,
      is_open: false,
    };
  },
  watch: {
    setting_form: {
      deep: true,
      handler() {
        this.changed += 1;
      },
    },
    is_open() {
      this.$emit("openChanged", this.is_open);
    },
  },
  inject: ["base_url"],
  emits: ["settingChanged", "openChanged"],
  methods: {
    onSelectStation(station_id, mobile_no) {
      this.setting_form.station_id = station_id;
      this.setting_form.mobile_no = mobile_no;
    },
    onSelectRoute(route_id) {
      this.setting_form.route = route_id;
    },
    onLoad() {
      this.changed = 0;
      this.err_msg = "";
      axios
        .get(this.base_url + "/getSetting", {
          params: {
            ID: VueCookies.get("logon"),
          },
        })
        .then((res) => {
          this.setting_form = res.data;
        });
    },
    onSubmit(event) {
      event.preventDefault();
      axios
        .put(this.base_url + "/changeSetting", {
          ID: VueCookies.get("logon"),
          API_DATA: this.setting_form.api_data || null,
          API_NCLOUD: this.setting_form.api_ncloud || null,
          ALARM_MIN: this.setting_form.alarm_min,
          STATION_ID: this.setting_form.station_id || null,
          MOBILE_NO: this.setting_form.mobile_no || null,
          ROUTE: this.setting_form.route || null,
          REQ_TERM: this.setting_form.req_term,
        })
        .catch((error) => {
          console.log("Error on changeSetting:", error.request);
          console.log(error.message);
        })
        .then(() => {
          this.$emit("settingChanged");
        });
      this.$refs.modal.hide();
    },
    onCancel() {
      this.$refs.modal.hide();
    },
    validate_api_data() {
      axios
        .post(this.base_url + "/checkDataAPI", {
          KEY: this.setting_form.api_data,
        })
        .then((response) => {
          if (!response.data) {
            this.alert_type = "danger";
            this.err_msg = "Wrong service key for data.go.kr!";
          } else {
            this.alert_type = "success";
            this.err_msg = "Authenticated for data.go.kr!";
          }
        });
    },
    validate_api_nCloud() {
      axios
        .post(this.base_url + "/checkNaverAPI", {
          KEY: this.setting_form.api_ncloud,
        })
        .then((response) => {
          if (!response.data) {
            this.alert_type = "danger";
            this.err_msg = "Wrong service key for nCloud!";
          } else {
            this.alert_type = "success";
            this.err_msg = "Authenticated for nCloud!";
          }
        });
    },
  },
};
</script>
