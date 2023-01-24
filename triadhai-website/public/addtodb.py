'''
import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
'''
import os
import json
import sys
import logging
#import rds_config
import pymysql 
#rds settings
RDS_ENDPOINT  = "sirius-mariadb.cwikov3ydirs.us-east-1.rds.amazonaws.com"
USER_NAME = "lambdauser"
USER_PASSWORD = "welcome123"
DATABASE_NAME = "siriusprocess"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=os.environ['RDS_ENDPOINT'], 
                            user=os.environ['USER_NAME'], 
                            passwd=os.environ['USER_PASSWORD'], 
                            db=os.environ['DATABASE_NAME'], 
                            connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def create_step_template(step_tuple):
    with conn.cursor() as cursor:
        try:
            query = "INSERT INTO StepTemplates (name, description, icon) VALUES (%s,%s,%s)"
            cursor.execute(query,step_tuple)
            conn.commit()
            return "Success"
        except pymysql.Error as e:
            return "Failed"      
def get_step_template(id):
    with conn.cursor() as cursor:
        query = "SELECT JSON_ARRAYAGG(JSON_OBJECT('steptemplateid',id,'name', name,'description',description, 'icon', icon)) from StepTemplates WHERE id = %s"
        cursor.execute(query,(id,))
        return cursor.fetchone()[0]
def get_step_templates():
    with conn.cursor() as cursor:
        query = "SELECT JSON_ARRAYAGG(JSON_OBJECT('steptemplateid',id,'name', name,'description',description, 'icon', icon)) from `StepTemplates`"
        cursor.execute(query)
        return  cursor.fetchall()[0][0]
 
def get_process_templates():
    with conn.cursor() as cursor:
        query = "SELECT JSON_ARRAYAGG(JSON_OBJECT('processtemplateid',id,'name', name,'icon', icon)) from `ProcessTemplates`"
        cursor.execute(query)
        return  cursor.fetchall()[0][0]

def create_pipeline_record(pipeline):
    with conn.cursor() as cursor:
        query = "INSERT INTO Pipelines (name) VALUES (%s)"
        cursor.execute(query,(pipeline['name']))
        conn.commit()
    with conn.cursor() as cursor:
        query = "SELECT LAST_INSERT_ID()"
        cursor.execute(query)
        res = cursor.fetchone()[0] #this returns a tuple...so get the first item
        return res
def create_process_record(process_tuple):
    with conn.cursor() as cursor:
        query = "INSERT INTO Processes (status, processtemplateid, sequenceid, pipelineid) VALUES (%s,%s,%s,%s)"
        cursor.execute(query,process_tuple)
        conn.commit()
    with conn.cursor() as cursor:
        query = "SELECT LAST_INSERT_ID()"
        cursor.execute(query)
        res = cursor.fetchone()[0] #this returns a tuple...so get the first item
        return res
        
def create_process_steps_record(step_tuple):
    with conn.cursor() as cursor:
        query = "INSERT INTO Steps (processid, steptemplateid, sequenceid, status) VALUES (%s,%s,%s,%s)"
        cursor.execute(query,step_tuple)
        conn.commit()

def create_pipeline(pipeline):
    pipelineid = create_pipeline_record(pipeline)
    for processidx,process in enumerate(pipeline['processes']):
        process_tuple = (process['status'],process['processtemplateid'],processidx+1,pipelineid)
        processid = create_process_record(process_tuple)
        for stepidx,step in enumerate(process['steps']):
            step_tuple = (processid,step['steptemplateid'],stepidx+1,step['status'])
            create_process_steps_record(step_tuple)
    return

def delete_child_processes(pipelineid):
    #delete all child elements
    with conn.cursor() as cursor:
        query = "DELETE FROM Processes WHERE pipelineid = %s;"
        cursor.execute(query,(pipelineid,))
        conn.commit()
        
def update_pipeline(pipeline)    :
    #delete all child processes, it will inturn delete all steps too as we have 'ON DELETE CASCADE
    pipelineid = pipeline['id']
    name = pipeline['name']
    #update the pipelinename
    with conn.cursor() as cursor:
        query = "UPDATE Pipelines SET name = %s WHERE id = %s;"
        cursor.execute(query,(name,pipelineid,))
        conn.commit()
        
    delete_child_processes(pipelineid)
    #now create child processes and steps
    #below code is exactly similar to create_pipeline() as above...
    #may refactor later if needed to use same function
    for processidx,process in enumerate(pipeline['processes']):
        process_tuple = (process['status'],process['processtemplateid'],processidx+1,pipelineid)
        processid = create_process_record(process_tuple)
        for stepidx,step in enumerate(process['steps']):
            step_tuple = (processid,step['steptemplateid'],stepidx+1,step['status'])
            create_process_steps_record(step_tuple)
    return

def delete_pipeline(pipelineid):
    #first confirm if pipeline exists
    with conn.cursor() as cursor:
        #query = "SELECT * FROM Pipelines WHERE id = %s;"
        query = "SELECT JSON_ARRAYAGG(JSON_OBJECT('id',id,'name', name)) from Pipelines WHERE id = %s;"
        cursor.execute(query,(pipelineid,))
        res =  cursor.fetchall()
        if res[0][0] == None: #no such pipeline exists
            return False
            
    #delete all child elements
    with conn.cursor() as cursor:
        query = "DELETE FROM Pipelines WHERE id = %s;"
        cursor.execute(query,(pipelineid,))
        conn.commit()
        return True
def get_pipeline(pipelineid):
    #first confirm if pipeline exists
    with conn.cursor() as cursor:
        #query = "SELECT * FROM Pipelines WHERE id = %s;"
        query = "SELECT JSON_ARRAYAGG(JSON_OBJECT('id',id,'name', name)) from Pipelines WHERE id = %s;"
        cursor.execute(query,(pipelineid,))
        res =  cursor.fetchall()
        if res[0][0] == None:
            print("returning none")
            return None
        res =  json.loads(res)[0] # todo validation later
    print("pipeline record ", res)
    pipelinedata = {}
    pipelinedata["id"] = str(pipelineid) #convert to string for serializing json
    pipelinedata["name"] = res['name']
    
    #note - to make a field json serializeable convert to string; below is the hack for the same
    #SELECT concat(id, '') FROM some_table;
    with conn.cursor() as cursor:
        '''
        query = """SELECT JSON_ARRAYAGG(JSON_OBJECT('id',concat(Processes.id,''),
                            'status',status,
                            'icon',ProcessTemplates.icon,
                            'name',ProcessTemplates.name,
                            'sequenceid',concat(sequenceid,''),
                            'pipelineid',concat(pipelineid,''))) 
                            FROM Processes INNER JOIN ProcessTemplates ON Processes.processtemplateid = ProcessTemplates.id WHERE pipelineid = %s ORDER BY sequenceid;"""
        '''
        query = """SELECT JSON_ARRAYAGG(JSON_OBJECT('processtemplateid',concat(Processes.processtemplateid,''),
                            'id',concat(Processes.id,''),
                            'status',status,
                            'icon',ProcessTemplates.icon,
                            'name',ProcessTemplates.name,
                            'sequenceid',concat(sequenceid,''),
                            'pipelineid',concat(pipelineid,''))) 
                            FROM Processes INNER JOIN ProcessTemplates ON Processes.processtemplateid = ProcessTemplates.id WHERE pipelineid = %s ORDER BY sequenceid;"""        
        cursor.execute(query,(pipelineid,))
        processes =  json.loads(cursor.fetchall()[0][0])
        #print(processes)
    with conn.cursor() as cursor:
        out_processes = []
        for process in processes:
            '''
            query = """SELECT JSON_ARRAYAGG(JSON_OBJECT('id',concat(Steps.id,''), 
                            'name',StepTemplates.name, 
                            'description',StepTemplates.description, 
                            'icon',StepTemplates.icon, 
                            'status',Steps.status ))
                            FROM Steps INNER JOIN StepTemplates ON Steps.steptemplateid = StepTemplates.id WHERE processid = %s;"""
            '''
            query = """SELECT JSON_ARRAYAGG(JSON_OBJECT('id',concat(Steps.id,''), 
                            'steptemplateid',concat(Steps.steptemplateid,''), 
                            'name',StepTemplates.name, 
                            'description',StepTemplates.description, 
                            'icon',StepTemplates.icon, 
                            'status',Steps.status,
                            'sequenceid',concat(sequenceid,'')))
                            FROM Steps INNER JOIN StepTemplates ON Steps.steptemplateid = StepTemplates.id WHERE processid = %s;"""            
            cursor.execute(query,(process['id'],))
            steps =  cursor.fetchall()[0][0]
            process['steps'] = json.loads(steps) #convert json formatted string to json object
            out_processes.append(process)

        pipelinedata['processes'] = out_processes
        pipelinedata = json.dumps(pipelinedata) #serialize json object to string
        pipelinedata = pipelinedata.replace("'", '"') 
        return pipelinedata

def get_all_pipelines():
    #first confirm if pipeline exists
    with conn.cursor() as cursor:
        query = "SELECT * FROM Pipelines;"
        cursor.execute(query)
        res =  cursor.fetchall() # todo validation later
    pipelineids = []
    for pipelineid in res:
        pipelineids.append(pipelineid[0])
    print(pipelineids)
    pipelines = "["
    for index, id in enumerate(pipelineids):
        pipeline = get_pipeline(id)
        pipelines = pipelines+pipeline
        if index != len(pipelineids)-1:
            pipelines += ","
    pipelines += "]"
    return pipelines
    
def lambda_handler(event, context):
    #res = get_all_pipelines()
    #res = get_pipeline("1")
    #print(res)
    #return
    #res = get_step_templates()
    #print(res)
    #return
    #res = get_all_pipelines()
    #print(res)
    #return
    if event["path"] == "/create-pipeline":
        if event['body'] is not None :
            print(event['body'])
            pipelinedata = json.loads(event['body'])
        else:
            status_code = 400
            return {
                'statusCode': status_code,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps("pipeline data not supplied")
            }
        create_pipeline(pipelinedata)
        return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },            
                'body': json.dumps("success")
            }
    if event["path"] == "/update-pipeline":
        if event['body'] is not None :
            print(event['body'])
            pipelinedata = json.loads(event['body'])
        else:
            status_code = 400
            return {
                'statusCode': status_code,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps("pipeline data not supplied")
            }
        update_pipeline(pipelinedata)
        return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },            
                'body': json.dumps("success")
            }            
    if event["path"] == "/delete-pipeline":
        if event['body'] is not None :
            print(event['body'])
            pipelinedata = json.loads(event['body'])
        else:
            status_code = 400
            return {
                'statusCode': status_code,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps("pipeline data not supplied")
            }
        if delete_pipeline(pipelinedata['id']) == True:
            return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                    },            
                    'body': json.dumps("success")
                }
        else:
            status_code = 404
            return {
                'statusCode': status_code,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps("No pipeline with supplied id found")
            }
    if event["path"] == "/get-pipeline":
        if event['body'] is not None :
            print(event['body'])
            pipelinedata = json.loads(event['body'])
        else:
            status_code = 400
            return {
                'statusCode': status_code,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps("pipeline data not supplied")
            }
        pipeline = get_pipeline(pipelinedata['id'])
        if pipeline is not None:
            return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                    },            
                    'body': pipeline
                }            
        else:
            status_code = 404
            return {
                'statusCode': status_code,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps("No pipeline with supplied id found")
            }
    if event["path"] == "/get-all-pipelines":
        pipelines = get_all_pipelines()
        return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },            
                'body': pipelines
            }            
    elif event["path"] == "/get-step-templates":
        res = get_step_templates()
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },            
            'body': res
        }
    elif event["path"] == "/get-steptemplate":
        if event['body'] is not None :
            print(event['body'])
            stepdata = json.loads(event['body'])
        else:
            status_code = 400
            return {
                'statusCode': status_code,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps("step id not supplied")
            }
        pipeline = get_step_template(stepdata['id'])
        if pipeline is not None:
            return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                    },            
                    'body': pipeline
                }            
        else:
            status_code = 404
            return {
                'statusCode': status_code,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps("No step with supplied id found")
            }
            
    elif event["path"] == "/create-step-template":
        if event['body'] is not None :
            stepdata = json.loads(event['body'])
        else:
            status_code = 400
            return {
                'statusCode': status_code,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps("step data not supplied")
            }
        if stepdata.keys() != {"name","description","icon"}:
            status_code = 400
            return {
                'statusCode': status_code,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },
                'body': json.dumps("step data not supplied")
            }
            
        res = create_step_template((stepdata['name'],stepdata['description'],stepdata['icon']))
        if res == "Success":
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },            
                'body': res
            }        
        else:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                },            
                'body': json.dumps("failed to create step template")
            }        
    elif event["path"] == "/get-process-templates":
        res = get_process_templates()
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            },            
            'body': res
        }        
    #no api's were called return exception (bad request)
    status_code = 400
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
        },
        'body': json.dumps("Bad request")
    }