from typing import Optional
from uuid import UUID
from fastapi import Request
from fastapi import Form
from fastapi.routing import run_endpoint_function
from starlette.responses import RedirectResponse
from models import open_for_reading, open_for_writing
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from routers import providers
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"), name="static")

app.include_router(providers.router)

@app.get("/")
def home(request: Request):
    message = "hello"
    return templates.TemplateResponse("index.html", {'request': request,
                                                     'message': message})


@app.get("/providers")
def read_root(request: Request) -> list:
    """
        returns the entire dictionary.
    """
    provider_data = open_for_reading()
    if provider_data:
        return templates.TemplateResponse("display_provider.html", {"request": request, 
                                                                    "provider_data": provider_data})
    else:
        return {"message": "database empty"}

@app.get("/provider_search_form")
def search(request: Request):
    return templates.TemplateResponse("search_form.html", {"request": request})

@app.get("/search_provider")
def search_provider(provider_id: UUID):
    url = f'/api/providers/{provider_id}'
    return RedirectResponse(url=url)

@app.get("/create_provider_form")
def render_creation_form(request: Request):
    return templates.TemplateResponse("creation_form.html",{'request': request})

# {
#   "name": "string",
#   "qualification": "string",
#   "speciality": "string",
#   "phone": "string",
#   "department": "string",
#   "organization": "string",
#   "location": "string",
#   "address": "string",
#   "providerID": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#   "active": true
# }

@app.post("/create_provider_form")
def create_provider(provider_id:UUID = Form(...),
                    name:str = Form(...),
                    qualification:str = Form(...),
                    speciality:str = Form(...),
                    phone:str = Form(...),
                    department:Optional[str] = Form("N/A"),
                    organization:str = Form(...),
                    location:Optional[str] = Form("N/A"),
                    address:str = Form(...),
                    active:bool = Form(...)):
    
    post_data = {
        "name": name,
        "qualification": qualification,
        "speciality": speciality,
        "phone": phone,
        "department": department,
        "organization": organization,
        "location": location,
        "address": address,
        "active": active
        }
    provider_data = open_for_reading()
    provider_data[str(provider_id)] = post_data
    open_for_writing(data=provider_data)

    return {'msg': 'updated'}


@app.get("/delete_provider_form")
def render_deletion_form(request: Request):
    provider_data = open_for_reading()
    return templates.TemplateResponse("deletion_form.html", {'request': request, "provider_data": provider_data})

@app.post("/delete_provider")
def delete_provider(provider_id:UUID = Form(...)):
    provider_data = open_for_reading()
    if provider_data:
        del_data = provider_data.pop(str(provider_id))
        open_for_writing(data=provider_data)
        return {"data": del_data}
    return {'data': provider_id}



@app.get("/update_provider_form")
def render_selection_menu(request: Request):
    provider_data = open_for_reading()
    return templates.TemplateResponse("update_provider_form.html", {"request": request, "provider_data": provider_data})


@app.post("/select_update_provider")
def render_update_form(request: Request, provider_id:UUID = Form(...)):

    provider_data = open_for_reading()
    print(type(provider_id))
    data_to_update = provider_data[str(provider_id)]

    return templates.TemplateResponse("updation_form.html", {"request": request, "provider_id": provider_id, "provider_data": data_to_update})



@app.post("/update_provider")
def update_provider(provider_id:UUID = Form(...),
                    name:str = Form(...),
                    qualification:str = Form(...),
                    speciality:str = Form(...),
                    phone:str = Form(...),
                    department:Optional[str] = Form("N/A"),
                    organization:str = Form(...),
                    location:Optional[str] = Form("N/A"),
                    address:str = Form(...),
                    active:bool = Form(...)):

    post_data = {
        "name": name,
        "qualification": qualification,
        "speciality": speciality,
        "phone": phone,
        "department": department,
        "organization": organization,
        "location": location,
        "address": address,
        "active": active
        }
    provider_data = open_for_reading()
    provider_data[str(provider_id)] = post_data
    open_for_writing(data=provider_data)
    return {"msg": "updated"}

# @app.post("update_provider")
# def update_provider(provider_id:UUID = Form(...)):
#     provider_data = 

# @app.put("/provider/update/{provider_id}")
# def put_provider(provider_id: str, provider: update_provider) -> dict:
#     """
#         updates the provider of given ID.
#     """
#     provider_data = open_for_reading()
#     if provider_data:
#         encoded_provider = jsonable_encoder(provider)
#         provider_data[provider_id] = encoded_provider
#         open_for_writing(data=provider_data)
#         return encoded_provider
#     else:
#         return {"message": "data not updated"}


