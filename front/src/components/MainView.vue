<template>
  <div>
    <b-alert dismissible variant="danger" :show="err_msg !== ''">
      {{ err_msg }}
    </b-alert>
    <b-card class="card m-2" header-tag="header" footer-tag="footer">
      <template #header>
        <b-container>
          <b-row align-v="baseline">
            <b-col class="sec2">{{ str_sec2 }}</b-col>
            <b-col class="text-center sec1">{{ str_sec1 }}</b-col>
            <b-col class="text-right update">
              <b-progress
                :value="update_sec"
                :max="info.req_term"
                show-value
                animated
                height="25px"
                class="w-25 float-right"
              />
              업데이트: {{ str_sec_update }}&nbsp;&nbsp;
            </b-col>
          </b-row>
        </b-container>
      </template>
      <b-container>
        <b-row>
          <b-col>
            <img id="bus2" src="../../public/bus.svg" />
          </b-col>
          <b-col>
            <img
              id="bus1"
              src="../../public/bus.svg"
              :style="'transform: translateX(' + pos + 'vw);'"
            />
          </b-col>
          <b-col class="text-right">
            <img class="stop" src="../../public/station.svg" />
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="3" class="text-left">{{ str_st2 }}</b-col>
          <b-col cols="1" class="text-center">→</b-col>
          <b-col cols="4" class="text-center">{{ str_st1 }}</b-col>
          <b-col cols="1" class="text-center">→</b-col>
          <b-col cols="3" class="text-right">{{ info.stNm }}</b-col>
        </b-row>
      </b-container>
      <template #footer>
        <b-container>
          <b-row>
            <b-col class="exp">{{ exp_tra }}</b-col>
            <b-col class="text-center">
              {{ info.rtNm }} (배차: {{ info.term }})
            </b-col>
            <b-col class="text-right last">막차: {{ info.lastTm }}</b-col>
          </b-row>
        </b-container>
      </template>
    </b-card>
    <b-container>
      <b-row>
        <b-col class="text-center"
          ><b-button @click="stopAll()">Stop</b-button></b-col
        >
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";
import VueCookies from "vue-cookies";

export default {
  name: "MainView",
  computed: {
    str_sec1() {
      if (this.info.sec1 === 0) {
        return this.info.n_st1;
      }
      let min = Math.floor(this.info.sec1 / 60);
      let sec = this.info.sec1 % 60;
      let hour = Math.floor(min / 60);
      min = min % 60;
      return (
        (hour ? hour + "시간 " : "") +
        (min ? min + "분 " : "") +
        (hour ? "" : sec ? sec + "초" : "")
      );
    },
    str_sec2() {
      if (this.info.sec2 === 0) {
        return this.info.n_st2;
      }
      let min = Math.floor(this.info.sec2 / 60);
      let sec = this.info.sec2 % 60;
      let hour = Math.floor(min / 60);
      min = min % 60;
      return (
        (hour ? hour + "시간 " : "") +
        (min ? min + "분 " : "") +
        (hour ? "" : sec ? sec + "초" : "")
      );
    },
    str_sec_update() {
      let min = Math.floor(this.info.delay / 60);
      let sec = this.info.delay % 60;
      return (min ? min + "분 " : "") + (sec ? sec + "초" : "") + " 전";
    },
    str_st1() {
      return (
        `${this.info.stationNm1}` +
        (Number.isInteger(this.info.n_st1)
          ? ` [${this.info.n_st1} 번째 전]`
          : "")
      );
    },
    str_st2() {
      return (
        `${this.info.stationNm2}` +
        (Number.isInteger(this.info.n_st2)
          ? ` [${this.info.n_st2} 번째 전]`
          : "")
      );
    },
    sec1() {
      return this.info.sec1;
    },
    is_last() {
      return this.info.is_last;
    },
    req_term() {
      return this.info.req_term;
    },
    pos() {
      const p2 = this.info.sec2 || 5400; // 90 min default
      const p1 = this.info.sec1 || 0; // if none, display none
      const p_norm = Math.max(p2 - p1, 0) / p2; // 0. ~ 1.
      return -20 + p_norm * 55; // -20 ~ 35
    },
  },
  data() {
    return {
      info: {
        delay: 0,
        stationNm1: "무지개",
        stationNm2: "벡터공간",
        sec1: 0,
        sec2: 0,
        n_st1: 0,
        n_st2: 0,
        rtNm: "호떡",
        stNm: "카레",
        lastTm: "0시 0분",
        term: "0분",
        is_last: false,
        alarm: 0,
        req_term: 0,
        mkTm: "2022-04-16 18:21:52.0",
      },
      exp_tra: "0분",
      err_msg: "",
      update_sec: 0,
    };
  },
  inject: ["base_url"],
  watch: {
    is_last(val) {
      if (val) {
        this.err_msg = "이번 차가 막차입니다!";
      }
    },
    req_term(val) {
      this.initTimer(val);
    },
    sec1(val) {
      if (val < 60 * this.info.alarm) {
        this.err_msg = `도착 ${Math.floor(val / 60)} 분 전입니다!`;
      }
    },
  },
  mounted() {
    this.mainRequest();
    this.initTimerSec();
  },
  methods: {
    stopAll() {
      clearInterval(this.main_callback);
      clearInterval(this.second_callback);
    },
    updateSecond() {
      this.info.delay += 1;
      this.info.sec1 = Math.max(0, this.info.sec1 - 1);
      this.info.sec2 = Math.max(0, this.info.sec2 - 1);
      this.update_sec -= 1;
      console.log("timer working");
    },
    initTimer(sec) {
      if (this.main_callback) {
        clearInterval(this.main_callback);
      }
      this.main_callback = setInterval(this.mainRequest, sec * 1000);
    },
    initTimerSec() {
      if (this.second_callback) {
        clearInterval(this.second_callback);
      }
      this.second_callback = setInterval(this.updateSecond, 1000);
    },
    mainRequest() {
      axios
        .post(this.base_url + "/mainRequest", {
          ID: VueCookies.get("logon"),
        })
        .catch((error) => {
          console.log("Error on mainRequest:", error.request);
          console.log(error.message);
        })
        .then((response) => {
          if (!response.data.success) {
            this.err_msg = response.data.data;
            this.stopAll();
          } else {
            this.err_msg = "";
            console.log(JSON.stringify(response.data.data));
            this.info = response.data.data;
          }
          this.update_sec = this.info.req_term;
        });
    },
  },
};
</script>

<style lang="scss" scoped>
.sec1 {
  font-size: larger;
}
#bus1 {
  width: 20vw;
}
#bus2 {
  width: 15vw;
  clip-path: polygon(50% 0, 50% 100%, 100% 100%, 100% 0);
  transform: translate(-10vw, 3vw);
}
.stop {
  width: 10vw;
  transform: scaleX(-1) translateY(3vw);
}
</style>
