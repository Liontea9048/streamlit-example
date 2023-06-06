import pandas as pd
import psycopg2
import datetime
import numpy as np
from collections import defaultdict

# PostgreSQL 연결
def closeConn(conn):
    conn.close()

def readSQL(connInfo, query = "select * from extracted_keywords"):
    conn = psycopg2.connect(connInfo)
    try:
        # 테이블을 Pandas.Dataframe으로 추출
        df = pd.read_sql(query, conn)
        return df

    except psycopg2.Error as e:
        # 데이터베이스 에러 처리
        print("DB error: ", e)
        return None
    
    finally:
        conn.close()

def executeSQL(connInfo, query, option=None):    
    conn = psycopg2.connect(connInfo)
    try:
        # 커서(Cursor) 생성
        # 커서: 명령문(SQL) 실행, 결과의 현재 위치 표시
        cursor = conn.cursor()
        
        # 값 변경 쿼리
        if option:
            cursor.execute(query, option)
        else:
            cursor.execute(query)
        
        # 트랜잭션 커밋 - 데이터베이스에 업데이트를 반영
        conn.commit()

    except psycopg2.Error as e:
        # 데이터베이스 에러 처리
        print("DB error: ", e)
        # 롤백- 최근 커밋 이후의 transaction들을 모두 취소
        conn.rollback()
    
    finally:
        conn.close()

def convertStrDatetime(strDateTime):
    tmp = datetime.datetime.strptime(strDateTime, "%Y-%m-%d %H:%M:%S")
    return datetime.datetime(*list(tmp))

def pushDataToEK(connInfo, data):
    for index, row in data.iterrows():
        # executeSQL(connInfo, """
        # INSERT INTO extracted_keywords (id, video_id, keywords)
        # VALUES (%(id)s, %(video_id)s, %(kwrds)s);
        # """,
        # {'id': 'default', 'video_id': int(row.id), 'kwrds': row.keywords})

        executeSQL(connInfo, """
        INSERT INTO extracted_keywords (video_id, keywords)
        VALUES (%(video_id)s, %(kwrds)s);
        """,
        {'video_id': int(row.id), 'kwrds': row.keywords})

def combineKeywords(*args):
    for arg in args:
        arg['keywords']

def readYT(connInfo):
    return readSQL(connInfo, """
            SELECT * FROM youtube_trending_video
            """)
            # where collect_datetime = (select max(collect_datetime) from youtube_trending_video)

def readTK(connInfo):
    return readSQL(connInfo, """
    SELECT video_id, keyword, rank 
    FROM top_keywords
    where timestamp = (select max(timestamp) from top_keywords)
    """)

def makeKwrdsAndVideoBundles(keywordSet):
    indexMap       = dict()
    keywordBundles = defaultdict(list)
    videoBundles   = defaultdict()
    keywords       = list()
    video_ids      = list()
    for index, row in keywordSet.iterrows():
        video_id = int(row['video_id'])
        keywords.append(row['keyword'])
        video_ids.append(video_id) # 1 1 1 5 15

    order = 0
    for idx in video_ids:
        try:
            if indexMap[idx]:
                pass
    
        except:
            indexMap[idx] = order
            order += 1

    order = 0
    # for (video_id, order, kwrd) in zip(indexMap.items(), keywords):
    for video_id, kwrd in zip(video_ids, keywords):
        # print(k)
        order = indexMap[video_id]
        # print(kwrd)
        keywordBundles[video_id].append(kwrd)
        videoBundles[order] = video_id
        order += 1
        # print(order, kwrd)
        # video_ids[video_ids].append(row.video_id)

    return (keywordBundles, videoBundles)



