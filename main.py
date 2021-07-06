from typing import Optional
from uuid import UUID
from fastapi import  FastAPI, Request, Form
from models import open_for_reading, open_for_writing
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
    """renders the page for entering providerID"""
    return templates.TemplateResponse("search_form.html", {"request": request})

@app.post("/search_provider")
def search_provider(request: Request, provider_id:UUID = Form(...)):
    """renders details of the given provider with it ID"""
    provider_data = open_for_reading()
    try :
        data = provider_data[str(provider_id)]
    except KeyError:
        return {"message": "invalid provider ID"}
    return templates.TemplateResponse("provider_details.html", {"request": request,
                                                                "provider_id": provider_id,
                                                                "provider_data": data})

@app.get("/create_provider_form")
def render_creation_form(request: Request):
    return templates.TemplateResponse("creation_form.html",{'request': request})


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
    return {'data': f'invalid ID : {provider_id}'}



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




