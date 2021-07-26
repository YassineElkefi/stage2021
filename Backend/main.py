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
import csv

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
#SELECT * FROM depot where DATE(date_envoi)  BETWEEN     '2021-09-07'   AND '2021-12-07'
@app.get("/selectdepot")
def search(Client :str, bp:str, service :str, date_s :str, date_e:str):
    db = mysql.connector.connect(host = "localhost" , user = "root" , password = "" , database = "stage2021")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM depot where client='{Client}' and bureau='{bp}' and service='{service}' and CAST(date_envoi AS date) BETWEEN '{date_s}' AND '{date_e}'")
    row_headers=[x[0] for x in cursor.description]
    rv = cursor.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
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
    return json_data