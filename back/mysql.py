from pymysql import connect
from pandas import read_sql_query
from numpy import nan

class MySQL:
    def __init__(self, database):
        self._com = connect(
            user='root', 
            passwd='1234', 
            host='web_db',
            port=3306,
            db=database
        )
        
    def send(self, query):
        if query.split()[0] in ('SELECT', 'SHOW'):
            return read_sql_query(query, self._com)
        else:
            self._com.query(query)
        
    def status(self):
        print(self.send("SHOW GLOBAL STATUS LIKE 'threads_connected'"))
        print(self.send('SHOW PROCESSLIST'))
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.__del__()
        
    def __del__(self):
        if self._com.open:
            self._com.close()
        

class MyDB(MySQL):
    def __init__(self):
        super().__init__('NOTIBUS')
    
    def _createUserTb(self):
        self.send('''
        CREATE TABLE USER (
            SEQ    INT    NOT NULL AUTO_INCREMENT,
            ID    VARCHAR(16)    NOT NULL,
            PW    VARCHAR(16)    NOT NULL,
            DEL    TINYINT(1)    DEFAULT 0,
            API_DATA    VARCHAR(128),
            API_NCLOUD    VARCHAR(128),
            ALARM_MIN    INT    NOT NULL    DEFAULT 10,
            STATION_ID     VARCHAR(9),
            MOBILE_NO     VARCHAR(9),
            ROUTE     VARCHAR(9),
            REQ_TERM    INT    NOT NULL    DEFAULT 30,
        PRIMARY KEY(SEQ)
        );
        ''')
        
    def _createHistoryTb(self):
        self.send('''
        CREATE TABLE HISTORY (
            SEQ    INT    NOT NULL AUTO_INCREMENT,
            user_seq INT NOT NULL,
            mkTm    DATETIME NOT NULL,
            rtNm    VARCHAR(16) NOT NULL,
            stNm    VARCHAR(16) NOT NULL,
            stationNm1    VARCHAR(32),
            sec1    INT,
            n_st1    INT,
            stationNm2    VARCHAR(32),
            sec2    INT,
            n_st2    INT,
            is_last    TINYINT(1),
            delay    INT,
        PRIMARY KEY(SEQ)
        );
        ''')
        
    def strORnull(self, data):
        return '"%s"' % data if data else 'NULL'
        
    def checkIdExist(self, username):
        return username in set(self.send('SELECT ID FROM USER WHERE DEL=0')['ID'])
        
    def signup(self, username, pw, api_data, api_ncloud):
        self.send('START TRANSACTION;')
        self.send(f"""
            INSERT INTO USER 
            (ID, PW, API_DATA, API_NCLOUD)
            VALUES
            ('{username}', '{pw}', {api_data}, {api_ncloud});
        """)
        self.send('COMMIT;')
        
    def changeSetting(self, ID, api_data, api_ncloud, alarm_min, station, stcode, route, req_term):
        query = f'''
        UPDATE USER SET
            API_DATA={self.strORnull(api_data)}, 
            API_NCLOUD={self.strORnull(api_ncloud)}, 
            ALARM_MIN={alarm_min}, 
            STATION_ID={self.strORnull(station)}, 
            MOBILE_NO={self.strORnull(stcode)}, 
            ROUTE={self.strORnull(route)}, 
            REQ_TERM={req_term}
        WHERE ID="{ID}";
        '''
        self.send(query)
        self.send('COMMIT;')
        
    def getSetting(self, ID):
        data = self.send('SELECT * FROM USER WHERE ID="%s"' % ID).T.to_dict()[0]
        return {k.lower():v for k, v in data.items() if k not in ('SEQ', 'ID', 'PW', 'DEL')}
    
    def getMainData(self, ID):
        data = self.send('SELECT API_DATA, STATION_ID, ROUTE, ALARM_MIN, REQ_TERM FROM USER WHERE ID="%s"' % ID)
        return data.T.to_dict()[0] if len(data) > 0 else False
        
    def getUserSeq(self, ID):
        return self.send("SELECT SEQ FROM USER WHERE ID='%s' AND DEL=0" % ID)['SEQ'][0]
        
    def recordHistory(self, data):
        for i in ('1', '2'):
            if not isinstance(data['n_st'+i], int):
                data['stationNm'+i] = data['n_st'+i]
                data['n_st'+i] = 'NULL'
                data['sec'+i] = 'NULL'

        self.send('START TRANSACTION;')
        self.send(f"""
            INSERT INTO HISTORY 
            (user_seq, mkTm, rtNm, stNm, stationNm1, sec1, n_st1, stationNm2, sec2, n_st2, is_last, delay)
            VALUES
            ('{data['user_seq']}', '{data['mkTm']}', '{data['stNm']}', '{data['rtNm']}', '{data['stationNm1']}', {data['sec1']}, {data['n_st1']}, '{data['stationNm2']}', {data['sec2']}, {data['n_st2']}, {data['is_last']}, {data['delay']});
        """)
        self.send('COMMIT;')
    
    def getHistory(self, ID):
        user_seq = self.getUserSeq(ID)
        df = self.send(f"SELECT * FROM HISTORY WHERE user_seq='{user_seq}'")
        df['mkTm'] = df['mkTm'].astype(str)
        df.replace(nan, None, inplace=True)
        df.drop(columns=['user_seq', 'delay'], inplace=True)
        return list(df.T.to_dict().values())
