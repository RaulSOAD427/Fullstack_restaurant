''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Necessary Imports
from fastapi import FastAPI, Request, Form             # The main FastAPI import and Request object
from fastapi.responses import Response
from fastapi.responses import HTMLResponse, JSONResponse     
from fastapi.templating import Jinja2Templates    # Used for generating HTML from templatized files
from fastapi.staticfiles import StaticFiles       # Used for making static resources available to server
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from urllib.request import urlopen
import json
import uvicorn                                    # Used for running the app directly through Python
import mysql.connector as mysql                   # Used for interacting with the MySQL database
import os                                         # Used for interacting with the system environment
from dotenv import load_dotenv                    # Used to read the credentials
from fastapi.encoders import jsonable_encoder
''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Configuration
load_dotenv('credentials.env')                 # Read in the environment variables for MySQL
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

app = FastAPI()                                   # Specify the "app" that will run the routing
views = Jinja2Templates(directory="views")        # Specify where the HTML files are located
app.mount("/public", StaticFiles(directory="public"), name="public")

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Define helper functions for CRUD operations
''''''''''''''''''''''''''''''
# MENU #

# CREATE SQL menu item
def db_add_menu(name:str, price:int):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  query = f"insert into Menu_Items (name, price) VALUES (%s, %s)"
  values = (name,price)
  cursor.execute(query,values)

  db.commit()
  db.close()
  id = cursor.lastrowid
  return id

# SELECT SQL query menu
def db_select_menu(item_id:int=None):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  if item_id ==None:
    cursor.execute("select * from menu_items;")
    response = cursor.fetchall()
  else:
    cursor.execute(f"select * from menu_items where item_id={item_id};")
    response = cursor.fetchall()
  cursor.close() 
  return response

# UPDATE SQL query menu
def db_edit_menu(item_id:int, new_name: str, new_price:int):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  length = cursor.lastrowid
  cursor.execute(f"update Menu_Items set name='{new_name}', price={new_price} WHERE item_id={item_id};")
  db.commit()
  db.close()
  new_length = cursor.lastrowid
  return {"success":length==new_length}

# DELETE SQL query menu
def db_delete_menu(item_id:int):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  length = cursor.lastrowid
  cursor.execute(f"DELETE FROM Menu_Items WHERE item_id={item_id};")
  db.commit()
  db.close()
  new_length = cursor.lastrowid
  return {"success":length!=new_length}

  
# ORDERS #

# CREATE SQL order item
# use on /order
def db_add_orders(item_id:int,name:str,quantity:int, status:int):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  query = f"insert into Orders (item_id, name, quantity, status) values ({item_id}, '{name}',{quantity}, '{status}');"
  cursor.execute(query)
  db.commit()
  db.close()
  id = cursor.lastrowid
  return id
#TOGGLE
def db_edit_orders(item_id:int,status:int):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  length = cursor.lastrowid
  cursor.execute(f"update Orders set status={status} WHERE order_id={item_id};")
  db.commit()
  db.close()
  new_length = cursor.lastrowid
  return {"success":length==new_length}

# SELECT SQL orders
def db_select_orders(user_id:int=None):
  #TODO: dont know if to retrieve via order_id or item_id yet
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  if user_id ==None:
    cursor.execute("select * from Orders;")
    response = cursor.fetchall()
  else:
    cursor.execute(f"select * from orders where order_id={user_id};")
    response = cursor.fetchall()
  cursor.close() 
  return response


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Home route to load the main page in a templatized fashion

# GET /
@app.get("/", response_class=HTMLResponse)
def get_html() -> HTMLResponse:
    with open("index.html") as html:
        return HTMLResponse(content=html.read())

@app.get('/order', response_class=HTMLResponse)
def get_home(request:Request) -> HTMLResponse:
  return views.TemplateResponse('order.html', {'request':request, 'menu':db_select_menu()})

# GET /
@app.get('/admin', response_class=HTMLResponse)
def get_home(request:Request) -> HTMLResponse:
  return views.TemplateResponse('admin.html', {'request':request, 'orders':db_select_orders() ,'menu':db_select_menu()})

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# RESTful User Routes

# GET /orders
# get orders
@app.get('/orders',response_class=JSONResponse)
def get_orders() -> JSONResponse:
#TODO: maybe not in right json order
  response = db_select_orders()
  ans = {}

  for index, row in enumerate(response):
    ans[index] = {
        "order_id": str(row[0]),
        "item_id": str(row[1]),
        "name": row[2],
        "quantity": str(row[3]),
        "status": row[4]
    }

  return JSONResponse(ans)

@app.get('/menu',response_class=JSONResponse)
def get_menus() -> JSONResponse:
  response = db_select_menu()
  ans = {}

  for index, row in enumerate(response):
    ans[index] = {
        "item_id": str(row[0]),
        "name": (row[1]),
        "price": str(row[2])
    }
  return JSONResponse(ans)
# get specific menu
@app.get('/menu/{item_id}',response_class=JSONResponse)
def get_menu(item_id: int) -> JSONResponse:
  response = db_select_menu(item_id)
  ans = {}
  for index, row in enumerate(response):
    ans[index] = {
        "item_id": str(row[0]),
        "name": (row[1]),
        "price": str(row[2])
    }
  return JSONResponse(ans)

# POST /users
@app.post("/postmenu")
async def post_menu(request:Request) -> dict:
  data = await request.json()
  item_id = db_add_menu(data['name'],data['price'])
  print(data['name'])
  return {"id":item_id,"name":data['name'],"price":data['price'] }

@app.post("/addorder")
async def post_order(request:Request) -> dict:
  data = await request.json()
  order_id = db_add_orders(data['item'],data['name'],data['quantity'],data['status'])
  # print(item+name+quantity)
  return {'success': 'true'}
# PUT /users/{user_id}
@app.put('/editmenu/{item_id}')
async def put_menu(item_id:int, request:Request) -> dict:
  data = await request.json()
  name, price = data['name'], data['price']
  return {'success': db_edit_menu(item_id, name,  price)}

@app.put('/editorder/{item_id}')
async def put_menu(item_id:int, request:Request) -> dict:
  data = await request.json()
  db_edit_orders(item_id,data['status'])
  return {'success':'done'}


@app.delete('/deletemenu/{item_id}')
async def delete_user(item_id:int) -> dict:
  return {'success': db_delete_menu(item_id)}


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# If running the server directly from Python as a module
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=6543)