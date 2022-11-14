import json
import string
import random

STRING = 'string'
ARRAY = 'array'
OBJECT = 'object'
NUMBER = 'number'
TYPE = 'type'
FILENAME = 'fieldName'


def getRandomString():
    N = 20
    res = ''.join(random.choices(string.ascii_uppercase +
                                string.ascii_lowercase, k=N))
    return str(res)
def getRandomNumber():
    return random.randrange(100, 1000)

def getBody(event):
    if 'body' in event:
        return json.loads(event['body'])
    return False
def returnErrorResponse(msg):
    return {"statusCode": 400, "body": {"msg": msg}}

def handleStrInt(type,array=False,fieldName='',resObj=None):
    if array:
        return getRandomString() if type == STRING else getRandomNumber()
    if type == STRING:
        resObj[fieldName] = handleStrInt(STRING,array=True)
    if type == NUMBER:
         resObj[fieldName]  = handleStrInt(NUMBER,array=True)
def handleArray(type,fieldName='',resObj=None,inner=None,quantity=1):
    arrayData = []
    inner = [inner]
    for j in range(quantity+1):
        for i in inner:
            if i[TYPE] == STRING or i[TYPE] == NUMBER:
                arrayData.append(handleStrInt(i[TYPE],array=True))
            elif i[TYPE] == OBJECT:
                arrayData.append( handleObject(i['inner']))
            elif i[TYPE] == ARRAY:
                arrayData.append(handleArray(i[TYPE],fieldName='',resObj=None,inner=i['ínner']))
    if not fieldName:
        return arrayData
    print(inner)
    resObj[fieldName] = arrayData    
def handleObject(inner):
    objectData = {}
    for i in inner:
        if i[TYPE] == STRING or i[TYPE] == NUMBER:
            handleStrInt(i[TYPE],array=False,fieldName=i[FILENAME],resObj=objectData)
        elif i[TYPE] == ARRAY:
            handleArray(i[TYPE],fieldName=i[FILENAME],resObj=objectData,inner=i["inner"],quantity=i['length'])
        else:
            handleObject(i['inner'])
    print(objectData)
    return objectData
        
def dummy(event, context):
    body = getBody(event)
    if not body:
       return returnErrorResponse('bad request')
    
    responseObject = {}
    for objects in body:
        print(objects[TYPE])

        if objects['type'] == STRING or objects['type'] == NUMBER:
            handleStrInt(objects['type'],array=False,fieldName=objects[FILENAME],resObj=responseObject)
        elif objects[TYPE] == OBJECT:
            handleObject(objects['inner'])
        elif objects[TYPE] == ARRAY:
            handleArray(objects[TYPE],fieldName=objects[FILENAME],resObj=responseObject,inner=objects['inner'],quantity=objects['length'])
        
    print(responseObject)
    response = {"statusCode": 200, "body": json.dumps(responseObject)}

    return response
