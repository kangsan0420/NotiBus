from fastapi import FastAPI, Request, Cookie, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse 
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import requests
import xmltodict
import json
import re
from datetime import datetime
from pytz import timezone
import os

from back import mysql

class Utils:
    @staticmethod
    def recursive_getter(data, getter):
        if len(getter) == 0:
            return data
        else:
            return Utils.recursive_getter(data[getter[0]], getter[1:])
    
    @staticmethod
    def request_get(url, params, includes, interface, debug=False):
        res = requests.get(url, params=params)
        response = res.content.decode('U8')

        if res.status_code != 200:
            return {'success': False, 'data': f'{res.status_code} Error'}
        for key, msg in includes.items():
            if key in response:
                return {'success': False, 'data': msg}

        data = json.loads(json.dumps(xmltodict.parse(response), ensure_ascii=False))
        
        if debug: print('\n', data, '\n')
        
        if Utils.recursive_getter(data, interface['err_code']) != '0':
            return {'success': False, 'data': Utils.recursive_getter(data, interface['err_res'])}
        else:
            return {'success': True, 'data': Utils.recursive_getter(data, interface['response'])}        


class Login(BaseModel):
    ID: str
    PW: str
    
class Signup(BaseModel):
    ID: str
    PW: str
    API_DATA: str | None
    API_NCLOUD: str | None

class API(BaseModel):
    KEY: str
    ITEM: str | None 
    
class API2(BaseModel):
    KEY: str
    ITEM1: str | None 
    ITEM2: str | None 
    
class Arrival(BaseModel):
    ID: str
    
class Setting(BaseModel):
    ID: str
    API_DATA: str | None
    API_NCLOUD: str | None
    ALARM_MIN: int
    STATION_ID: str | None
    MOBILE_NO: str | None
    ROUTE: str | None
    REQ_TERM: int

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f"{os.environ.get('HOST_ADDR')}:{os.environ.get('PORT_FRONT')}",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/login/")
async def login(data: Login):
    logon = False
    with mysql.MyDB() as COM:
        df = COM.send("SELECT pw FROM USER WHERE ID='%s';" % data.ID)
    if len(df) == 0:
        body = {'msg': 'Wrong ID.'}
    elif df.iloc[0,0] != data.PW:
        body = {'msg': 'Wrong password.'}
    else:
        body = {'msg': None}
        logon = True
        
    response = JSONResponse(body)
    if logon:
        response.set_cookie(key='logon', value=data.ID)
    return response

@app.post("/signup/")
async def create_account(data: Signup):
    with mysql.MyDB() as com:
        res = com.signup(data.ID, data.PW, data.API_DATA or 'NULL', data.API_NCLOUD or 'NULL')
        return len(com.send("SELECT * FROM USER WHERE ID='%s';" % data.ID)) == 1

@app.post("/checkId/")
async def check_account(data: Signup):
    with mysql.MyDB() as com:
        res = com.checkIdExist(data.ID)
    return res

@app.post("/checkDataAPI/")
async def check_api_from_data_go_kr(data: API):
    url = 'http://apis.data.go.kr/6410000/busstationservice/getBusStationList'
    params ={'serviceKey' : data.KEY, 'keyword' : '뱅뱅'}
    res = requests.get(url, params=params)
    is_valid = 'SERVICE_KEY_IS_NOT_REGISTERED_ERROR' not in res.content.decode('U8')
    return is_valid

@app.post("/checkNaverAPI/")
async def check_api_from_ncloud(data: API):
    url = 'https://naveropenapi.apigw.ntruss.com/map-static/v2/raster-cors'
    querystring = f'?w=300&h=300&center=127.1054221,37.3591614&level=16&X-NCP-APIGW-API-KEY-ID={data.KEY}'

    res = requests.get(url+querystring, headers={ 
      'Referer': os.environ.get('HOST_ADDR')
    })
    return res.status_code == 200
        
@app.get("/getSetting/")
async def get_setting(ID: str):
    with mysql.MyDB() as com:
        res = com.getSetting(ID)
        return res
    
@app.put("/changeSetting/")
async def change_setting(data: Setting):
    with mysql.MyDB() as com:
        res = com.changeSetting(data.ID, data.API_DATA, data.API_NCLOUD, data.ALARM_MIN, 
                                data.STATION_ID, data.MOBILE_NO, data.ROUTE, data.REQ_TERM)
        return res
    
@app.post("/searchByStationName/")
async def search_station(data: API):
    res = Utils.request_get(
        url='http://apis.data.go.kr/6410000/busstationservice/getBusStationList',
        params={'serviceKey' : data.KEY, 'keyword' : data.ITEM},
        includes={'SERVICE_KEY_IS_NOT_REGISTERED_ERROR': "등록되지 않은 service key."},
        interface={
            'err_code': ('response', 'msgHeader', 'resultCode'),
            'err_res': ('response', 'msgHeader', 'resultMessage'),
            'response': ('response', 'msgBody', 'busStationList')
        }
    )
    return res
    
@app.post("/searchRoute/")
async def search_route(data: API2):
    # 경기도
    res1 = Utils.request_get(
        url='http://apis.data.go.kr/6410000/busstationservice/getBusStationViaRouteList',
        params={'serviceKey' : data.KEY, 'stationId' : data.ITEM1},
        includes={'SERVICE_KEY_IS_NOT_REGISTERED_ERROR': "등록되지 않은 service key."},
        interface={
            'err_code': ('response', 'msgHeader', 'resultCode'),
            'err_res': ('response', 'msgHeader', 'resultMessage'),
            'response': ('response', 'msgBody', 'busRouteList')
        }
        # , debug=True
    )
    
    #서울
    res2 = Utils.request_get(
        url='http://ws.bus.go.kr/api/rest/stationinfo/getRouteByStation',
        params={'serviceKey' : data.KEY, 'arsId' : data.ITEM2},
        includes={'SERVICE KEY IS NOT REGISTERED ERROR': "등록되지 않은 service key."},
        interface={
            'err_code': ('ServiceResult', 'msgHeader', 'headerCd'),
            'err_res': ('ServiceResult', 'msgHeader', 'headerMsg'),
            'response': ('ServiceResult', 'msgBody', 'itemList')
        }
        # , debug=True
    )
    if res2['success']:
        cvt = {'regionName': None, 'routeName': 'busRouteNm', 'routeTypeName': None, 'routeId': 'busRouteId'}
        for i in range(len(res2['data'])):
            res2['data'][i] = {k: v if v is None else res2['data'][i][v] for k ,v in cvt.items()}
            
    #결합
    res = {
        'success': any([res1['success'], res2['success']]), 
        'data': (res1['data'] if res1['success'] else []) + (res2['data'] if res2['success'] else [])
    }
    return res
    
    
@app.post("/mainRequest/")
async def get_arrival(data: Arrival):
    def getSecond_NumStation(msg, rule='^(?P<min>\d+)분((?P<sec>\d+)초)?후\[(?P<num>\d+)번째 전\]$'):
        if msg in ('출발대기', '운행종료', '곧 도착'):
            return (None, msg)
        group = re.search(rule, msg)
        second = 60*int(group['min']) + int(group['sec']) if group['sec'] else 0
        n_station = int(group['num'])
        return second, n_station

    with mysql.MyDB() as COM:
        res = COM.getMainData(data.ID)
        user_seq = COM.getUserSeq(data.ID)
    
    items = Utils.request_get(
        url='http://ws.bus.go.kr/api/rest/arrive/getArrInfoByRouteAll',
        params={'serviceKey' : res['API_DATA'], 'busRouteId' : res['ROUTE']},
        includes={
            'SERVICE KEY IS NOT REGISTERED ERROR': '등록되지 않은 service key.',
            'LIMITED NUMBER OF SERVICE REQUESTS EXCEEDS ERROR': 'API 사용횟수 소진.'
        },
        interface={
            'err_code': ('ServiceResult', 'msgHeader', 'headerCd'),
            'err_res': ('ServiceResult', 'msgHeader', 'headerMsg'),
            'response': ('ServiceResult', 'msgBody', 'itemList')
        }
        # , debug=True
    )
    if not items['success']:
        return items
    
    user_id = data.ID
    data = [item for item in items['data'] if item['stId'] == res['STATION_ID']]

    if len(data) != 1: return {'success': False, 'data': f"Multiple items found. {station_id: {res['STATION_ID']}}"}

    data = data[0]
    data['sec1'], data['n_st1'] = getSecond_NumStation(data['arrmsg1'])
    data['sec2'], data['n_st2'] = getSecond_NumStation(data['arrmsg2'])

    data['is_last'] = data['arrmsg2'] == '운행종료'
    data['lastTm'] = f"{int(data['lastTm'][8:10])}시 {int(data['lastTm'][10:12])}분"
    data['term'] = data['term'] + "분"
    data['alarm'] = res['ALARM_MIN']
    data['req_term'] = res['REQ_TERM']
    
    tz = timezone('Asia/Seoul')
    dt_rule = '%Y-%m-%d %H:%M:%S.%f'
    data['delay'] = int((datetime.now(tz=tz).replace(tzinfo=None) - datetime.strptime(data['mkTm'], dt_rule)).total_seconds())
    if data['arrmsg1'] in ('출발대기', '운행종료'): data['stationNm1'] = None
    if data['arrmsg2'] in ('출발대기', '운행종료'): data['stationNm2'] = None
    with mysql.MyDB() as COM:
        data['user_seq'] = user_seq
        COM.recordHistory(data)
    items = ('mkTm', 'delay', 'stationNm1', 'stationNm2', 'sec1', 'n_st1', 'stNm', 'rtNm',
             'sec2', 'n_st2', 'lastTm', 'term', 'is_last', 'alarm', 'req_term')
    data = {k: data[k] for k in items}
    return {'success': True, 'data': data}

@app.get("/test/")
async def test(logon: str | None = Cookie(None)):
    return logon

@app.get("/getHistory/")
async def get_history(ID: str):
    with mysql.MyDB() as COM:
        res = COM.getHistory(ID)
        return res
    
