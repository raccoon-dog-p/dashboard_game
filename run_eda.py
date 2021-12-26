import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector.errors import Error
# 1. db에 연결
def sql_insert(name):
    try :
        connection = mysql.connector.connect(
            host = 'my-db.cfbeyhqoz6o8.ap-northeast-2.rds.amazonaws.com',
            database = 'streamlit_db',
            user = 'python user',
            password = '1234')

        
        # date = '2021-12-15'
        # 2. 쿼리문 만들고
        query = ''' insert into history
                    (title)
                    values
                    (%s);
        '''
        # 파이썬에서 튜플만들때 데이터가 1개인 경우는 , 를 넣고 써주자
        record = (name,)


        # 3. 커넥션으로 부터 커서를 가져온다.
        cursor = connection.cursor()

        # 4. 쿼리문을 커서에 넣어서 실행한다.
        cursor.execute(query,record)

        # 5. 커넥션을 커밋한다. db에 영구적으로 반영하라는 뜻
        connection.commit()
    except Error as e:
        print('Error ', e)

    finally :
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def sql_selcet():
        try :
            connection = mysql.connector.connect(
            host = 'my-db.cfbeyhqoz6o8.ap-northeast-2.rds.amazonaws.com',
            database = 'streamlit_db',
            user = 'python user',
            password = '1234')


            query= ''' select * 
                    from history;
            '''

            cursor = connection.cursor(dictionary=True)

            cursor.execute(query)

            # select 문은 아래 내용이 필요하다
            record_list = cursor.fetchall()
            history=[]
            for row in record_list:
                history.append(row['title'])
        # 위의 코드를 실행하다가, 문제가 생기면, except를 실행하라는 뜻.     
        except Error as e :
            print('Error while connecting to MySQL',e)
        # finally는 try에서 에러가 나든 안나든, 무조건 실행하라는 뜻.
        finally :
            if connection.is_connected():
                cursor.close()
                connection.close()
                print('MySQL connection is closed')
            else :
                print('connection does not exist')
            return history