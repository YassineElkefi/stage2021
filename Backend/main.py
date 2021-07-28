from typing import Optional
from fastapi import FastAPI , Request
from fastapi.params import Body
import mysql.connector
import json
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from reportlab.pdfgen import canvas
from starlette.responses import FileResponse
from fastapi.responses import StreamingResponse
from datetime import datetime as dt
from datetime import date as d
app = FastAPI()

origins = [
"http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/signup")
async def add(request:Request):
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "stage2021")
    mycursor = mydb.cursor()
    body = json.loads(await request.body())
    mycursor.execute(f"SELECT * FROM agent WHERE mail_ag = '{body['mail']}'")
    rv = mycursor.fetchone()
    if (rv):
        return '{"Email already exists!"}'
    else:
        mycursor.execute(f"INSERT INTO `agent`(`nom`, `prenom`, `tel_ag`, `mail_ag`, `password`) VALUES('{body['nom']}', '{body['prenom']}','{body['tel']}','{body['mail']}','{body['pwd']}');")
        mydb.commit()
        return {"OK"}
####################################################################################################################
@app.post("/add")
async def add(request:Request):
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "stage2021")
    mycursor = mydb.cursor()
    body = json.loads(await request.body())
    mycursor.execute(f"INSERT INTO `client`(`libelle`, `telephone`, `fax`, `adresse`, `mail`) VALUES('{body['client']}', '{body['tel']}', '{body['fax']}','{body['adresse']}','{body['mail']}');")
    mydb.commit()
    return {"OK"}
####################################################################################################################
@app.get("/selectc")
def gets():
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "stage2021")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM client")
    row_headers=[x[0] for x in mycursor.description] 
    rv = mycursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json_data
####################################################################################################################
@app.get("/selectr")
def gets():
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "stage2021")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM region")
    row_headers=[x[0] for x in mycursor.description] 
    rv = mycursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json_data
####################################################################################################################
@app.get("/selectbp")
def gets(id:str):
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "stage2021")
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM bureau_poste bp,region r where bp.region = r.id_region and id_region={id}")
    row_headers=[x[0] for x in mycursor.description] 
    rv = mycursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json_data
####################################################################################################################
@app.get("/selects")
def gets():
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "stage2021")
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM service")
    row_headers=[x[0] for x in mycursor.description] 
    rv = mycursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json_data
####################################################################################################################
@app.post("/addepot")
async def add(request:Request):
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "stage2021")
    mycursor = mydb.cursor()
    body = json.loads(await request.body())
    mycursor.execute(f"INSERT INTO `depot`(`id_depot`,`service`, `bureau`, `client`,`date_envoi`, `montant`, `nombre`) VALUES(NULL, '{body['service']}', '{body['bureau']}', '{body['client']}',current_timestamp(),'{body['montant']}','{body['nombre']}');")
    mydb.commit()
    return {"OK"}
####################################################################################################################
@app.delete("/delcli")
async def supp(request:Request):
    mydb = mysql.connector.connect(host = "localhost", user = "root" , password = "" , database = "stage2021")
    mycursor = mydb.cursor()
    body = json.loads(await request.body())
    mycursor.execute(f"SET FOREIGN_KEY_CHECKS =0;")
    mycursor.execute(f"delete from `client` where `id_client`= {body['client']};") 
    mycursor.execute(f"ALTER TABLE `client` AUTO_INCREMENT=1;")
    mydb.commit()
    return {"OK"}
####################################################################################################################
@app.post("/login")
async def db_test(request : Request):
    mydb = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "stage2021")
    mycursor = mydb.cursor()
    body = json.loads(await request.body())
    print (body)
    mycursor.execute(f"select * from agent  where (mail_ag = '{body['user']}') and (password = '{body['pwd']}')")
    row_headers=[x[0] for x in mycursor.description] 
    rv = mycursor.fetchall()
    json_data=[]
    for result in rv:
            json_data.append(dict(zip(row_headers,result)))
    return json_data

####################################################################################################################
@app.get("/selectdepot")
def search(Client :str, bp:str, service :str, date_s :str, date_e:str):
    if date_e =="":
        date_e = d.today().strftime("%Y-%m-%d")
    db = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "stage2021")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM depot")
    row_headers=[x[0] for x in cursor.description]
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    if(Client=="" and  bp=="" and service=="" and date_s!=""):
        json_data = [data for data in json_data if ((data["date_envoi"])>dt.strptime(date_s, "%Y-%m-%d")) and (date_e!="") and ((data["date_envoi"])<=dt.strptime(date_e, "%Y-%m-%d"))]
    if(Client!="" and  bp=="" and service=="" and date_s==""):
        json_data = [data for data in json_data if (data['client']==int(Client))]
    if(Client=="" and bp!="" and service=="" and date_s=="" ):
        json_data = [data for data in json_data if (data['bureau']==int(bp))]
    if(Client=="" and bp=="" and service!="" and date_s=="" ):
        json_data = [data for data in json_data if (data['service']==int(service))]
    if(Client!="" and  bp!="" and service=="" and date_s==""):
        json_data = [data for data in json_data if (data['client']==int(Client)) and (data['bureau']==int(bp))]
    if(Client!="" and  bp=="" and service!="" and date_s==""):
        json_data = [data for data in json_data if (data['client']==int(Client)) and (data['service']==int(service))]
    if(Client!="" and  bp=="" and service=="" and date_s!=""):
        json_data = [data for data in json_data if (data['client']==int(Client)) and ((data["date_envoi"])>dt.strptime(date_s, "%Y-%m-%d")) and (date_e!="") and ((data["date_envoi"])<=dt.strptime(date_e, "%Y-%m-%d"))]
    if(Client=="" and bp!="" and service!="" and date_s=="" ):
        json_data = [data for data in json_data if (data['bureau']==int(bp)) and (data['service']==int(service))]  
    if(Client=="" and bp!="" and service=="" and date_s!="" ):
        json_data = [data for data in json_data if (data['bureau']==int(bp)) and ((data["date_envoi"])>dt.strptime(date_s, "%Y-%m-%d")) and (date_e!="") and ((data["date_envoi"])<=dt.strptime(date_e, "%Y-%m-%d"))]  
    if(Client=="" and bp=="" and service!="" and date_s!="" ):
        json_data = [data for data in json_data if (data['service']==int(service)) and ((data["date_envoi"])>dt.strptime(date_s, "%Y-%m-%d")) and (date_e!="") and ((data["date_envoi"])<=dt.strptime(date_e, "%Y-%m-%d")) ]
    if(Client!="" and bp!="" and service!="" and date_s=="" ):
        json_data = [data for data in json_data if (data['client']==int(Client)) and (data['bureau']==int(bp)) and (data['service']==int(service))]
    if(Client!="" and bp!="" and service=="" and date_s!="" ):
        json_data = [data for data in json_data if (data['client']==int(Client)) and (data['bureau']==int(bp)) and ((data["date_envoi"])>dt.strptime(date_s, "%Y-%m-%d")) and (date_e!="") and ((data["date_envoi"])<=dt.strptime(date_e, "%Y-%m-%d")) ]
    if(Client!="" and bp=="" and service!="" and date_s!="" ):
        json_data = [data for data in json_data if (data['client']==int(Client)) and (data['service']==int(service)) and ((data["date_envoi"])>dt.strptime(date_s, "%Y-%m-%d")) and (date_e!="") and ((data["date_envoi"])<=dt.strptime(date_e, "%Y-%m-%d"))]
    if(Client=="" and bp!="" and service!="" and date_s!=""):
        json_data = [data for data in json_data if (data['bureau']==int(bp)) and (data['service']==int(service)) and ((data["date_envoi"])>dt.strptime(date_s, "%Y-%m-%d")) and (date_e!="") and ((data["date_envoi"])<=dt.strptime(date_e, "%Y-%m-%d")) ]
    """
    json_data = [data for data in json_data if (Client!="") and (data['client']==Client)]
if(Client="" and )
    json_data = [data for data in json_data if (bp!="") and (data['bureau']==bp)]
    json_data = [data for data in json_data if (service!="") and (data['service']==service)]
    json_data = [data for data in json_data if (date_s!="") and (dt.strpstime(data["date_envoi"], "%y/%m/%d")<dt.strpstime(date_s, "%d/%m/%y")) and (date_e!="") and (dt.strpstime(data["date_envoi"], "%y/%m/%d")>dt.strpstime(date_e, "%d/%m/%y"))]"""
    """for data in json_data:
        if (Client!="") and (data['client']!= Client):
            if (bp!="") and (data['bp'] != bp):
                if (service!="") and (data['service']!=service):"""
    for data in json_data:
        cursor.execute(f"SELECT libelle FROM client where id_client = {data['client']}")
        nom = cursor.fetchone()[0]
        data['client'] = nom

        cursor.execute(f"SELECT libelle_service FROM service where id_service = {data['service']}")
        srv = cursor.fetchone()[0]
        data['service'] = srv

        cursor.execute(f"SELECT nom_bp FROM bureau_poste where id_bp = {data['bureau']}")
        bp = cursor.fetchone()[0]
        data['bureau'] = bp
    return json_data
#####################################################################################################################
@app.get("/selectall")
def search():
    db = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "stage2021")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM depot")
    row_headers=[x[0] for x in cursor.description]
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    for data in json_data:
        cursor.execute(f"SELECT libelle FROM client where id_client = {data['client']}")
        nom = cursor.fetchone()[0]
        data['client'] = nom

        cursor.execute(f"SELECT libelle_service FROM service where id_service = {data['service']}")
        srv = cursor.fetchone()[0]
        data['service'] = srv

        cursor.execute(f"SELECT nom_bp FROM bureau_poste where id_bp = {data['bureau']}")
        bp = cursor.fetchone()[0]
        data['bureau'] = bp
    return json_data