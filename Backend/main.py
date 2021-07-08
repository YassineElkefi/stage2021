from typing import Optional
from fastapi import FastAPI , Request
from fastapi.params import Body
import mysql.connector
import json
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
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