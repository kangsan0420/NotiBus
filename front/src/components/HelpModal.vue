/* eslint-disable prettier/prettier */
<template>
  <div>
    <b-modal ref="modal" size="xl" title="Guide">
      <h6>data.go.kr API</h6>
      <ul>
        <li>
          공공데이터 포털(https://data.go.kr) 에서 "경기도_정류소 조회",
          "서울특별시_정류소정보조회 서비스" 활용 신청
        </li>
        <li>일반 인증키 (Decoding) 에 해당하는 키 입력</li>
        <li>신청 후 사용 가능하기까지 24시간까지 소요될 수 있음</li>
      </ul>

      <h6>nCloud API</h6>
      <ul>
        <li>
          Naver Cloud
          Platform(https://www.ncloud.com/product/applicationService/maps) 에서
          이용 신청
        </li>
        <li>
          콘솔(https://console.ncloud.com/naver-service/application) 에서
          인증정보 → Client ID에 해당하는 키 입력
        </li>
      </ul>

      <h6>Alarm</h6>
      <ul>
        <li>
          첫번째 버스의 도착예정 시간이 해당 시간(분) 밑으로 내려가면 알람
        </li>
      </ul>

      <h6>Station, Code</h6>
      <ul>
        <li>버스정류소의 station_id 및 mobile_no. Search 버튼으로 검색</li>
      </ul>

      <h6>Route</h6>
      <ul>
        <li>
          해당 정류소 지나는 노선번호. Station과 Code를 입력 한 후 Search
          버튼으로 검색
        </li>
      </ul>

      <h6>Request</h6>
      <ul>
        <li>
          초단위의 도착예정시간 재요청 간격, data.go.kr의 일일 이용량은
          1,000건임에 주의
        </li>
      </ul>
      <template #modal-footer>
        <b-button @click="$refs.modal.hide()">Close</b-button>
      </template>
    </b-modal>
  </div>
</template>

<script>
export default {
  //
};
</script>

<style lang="scss" scoped>
pre {
  font-family: sans-serif;
  font-size: large;
}
</style>
