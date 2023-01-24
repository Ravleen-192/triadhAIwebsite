'''
import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
'''
import json
import sys
import logging
#import rds_config
from urllib.parse import unquote
import pymysql 
#rds settings
#RDS_ENDPOINT = "database-wp.cluster-cd1l5n7j8dlb.us-west-2.rds.amazonaws.com"
#USER_NAME = "admin"
#USER_PASSWORD = "dbwp1234"
#DATABASE_NAME = "database-wp"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=RDS_ENDPOINT, 
                            user=USER_NAME, 
                            passwd=USER_PASSWORD,
                            database = DATABASE_NAME,
                            connect_timeout=5)
    """ with conn.cursor() as cur:
        cur.execute("CREATE DATABASE IF NOT EXISTS `database-wp`")
        cur.execute("SHOW DATABASES")

        ## 'fetchall()' method fetches all the rows from the last executed statement
        databases = cur.fetchall() ## it returns a list of all databases present

        ## printing the list of databases
        print(databases)

        ## showing one by one database
        for database in databases:
            print(database)"""
       
        
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


def handler(event, context):
    
    """
    This function fetches content from MySQL RDS instance
    """
   
    email = str(event['queryStringParameters']['email'])
    name =  unquote(str(event['queryStringParameters']['name']))
    title =  unquote(str(event['queryStringParameters']['title']))
    company =  unquote(str(event['queryStringParameters']['company']))
    phone =  unquote(str(event['queryStringParameters']['phone']))
    DonotSolicit= 'n'
    Comments = "Recommended"
    item_count = 0
    trow=""
    with conn.cursor() as cur:
        cur.execute("create table if not exists WPSubscriber ( ID INT NOT NULL AUTO_INCREMENT, Name varchar(255) NOT NULL,Email varchar(255) NOT NULL, Company varchar(255) NOT NULL, JobTitle varchar(255) NOT NULL,Phone varchar(255) NOT NULL, DoNotSolicit varchar(1) NOT NULL, Comments varchar(255) NOT NULL, PRIMARY KEY (ID))")
        sql = "INSERT INTO `WPSubscriber` (`Name`,  `Email`, `Company`,`JobTitle`, `Phone`, `DoNotSolicit`, `Comments`) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        val = (name,email,company,title, phone, DonotSolicit,Comments)
        cur.execute(sql,val)
        conn.commit()
        cur.execute("select * from WPSubscriber")
        for row in cur:
            item_count += 1
            logger.info(row)
            trow = row
            print("row")
            print(trow)
    conn.commit()

    return {
        'statusCode': 200,
        'body': json.dumps(trow)
    }