<template>
  <b-col>
    <b-card
      class="card m-2"
      :class="{ selected: isSelected, unselected: !isSelected }"
      header-tag="header"
      footer-tag="footer"
      :style="{ width: String(size + 4) + 'px' }"
      @click="onClick"
    >
      <b-card-header class="text-center">
        {{ stationName }}
      </b-card-header>

      <b-card-body>
        <div
          :id="item_id"
          :style="{ width: size + 'px', height: size + 'px' }"
        ></div>
      </b-card-body>

      <b-card-footer>
        <b-container>
          <b-row>
            <b-col cols="4" class="text-right">stId:</b-col>
            <b-col cols="8">{{ stationId }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="4" class="text-right">mbNo:</b-col>
            <b-col cols="8">{{ mobileNo }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="4" class="text-right">지역:</b-col>
            <b-col cols="8">{{ regionName }}</b-col>
          </b-row>
          <b-row>
            <b-col cols="4" class="text-right">좌표:</b-col>
            <b-col cols="8">{{ coords }}</b-col>
          </b-row>
          <b-row v-if="isSelected" align-h="center"
            ><b-button
              class="select_button"
              variant="success"
              @click="$emit('selected', item_id, mobileNo)"
              >Select</b-button
            ></b-row
          >
        </b-container>
      </b-card-footer>
    </b-card>
  </b-col>
</template>

<script>
export default {
  name: "DynamicMap",
  props: ["service_key", "obj", "item_id", "size"],
  emits: ["click", "selected"],
  data() {
    return {
      mobileNo: "",
      regionName: "",
      stationId: "",
      stationName: "",
      coords: [0, 0],
      isSelected: false,
    };
  },
  mounted() {
    this.mobileNo = this.obj.mobileNo;
    this.regionName = this.obj.regionName;
    this.stationId = this.obj.stationId;
    this.stationName = this.obj.stationName;
    this.coords = [parseFloat(this.obj.y), parseFloat(this.obj.x)];
    this.loadScript();
  },
  methods: {
    onClick() {
      this.$emit("click", this.item_id);
    },
    select() {
      this.isSelected = true;
    },
    deSelect() {
      this.isSelected = false;
    },
    loadScript() {
      this.$loadScript(
        `https://openapi.map.naver.com/openapi/v3/maps.js?ncpClientId=${this.service_key}`
      )
        .then(() => {
          this.loadMap();
        })
        .catch(() => {
          console.log("Fail");
        });
    },
    loadMap() {
      /* eslint-disable */
      let map = new naver.maps.Map(this.item_id, {
        center: new naver.maps.LatLng(this.coords[0], this.coords[1]),
        zoom: 15,
        zoomControl: true,
        zoomControlOptions: {
            position: naver.maps.Position.TOP_RIGHT
        },
        scrollWheel: false,
        mapTypes: new naver.maps.MapTypeRegistry({
          'normal': naver.maps.NaverStyleMapTypeOptions.getNormalMap(
            {
              overlayType: 'bg.ol.bs.lko',
            }
          ),
        }),
      });
      new naver.maps.Marker({
        position: new naver.maps.LatLng(this.coords[0], this.coords[1]),
        map: map,
      });
    },
  },
};
</script>

<style lang="scss" scoped>
@import "node_modules/bootstrap/scss/bootstrap";

.card-body {
  padding: 1px;
}
.selected {
  border-color: $success;
}
.unselected {
  &:hover {
    border-color: $primary;
  }
}
.select_button {
  margin-top: 10px;
}
</style>
