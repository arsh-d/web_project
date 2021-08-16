from typing import Optional
from uuid import UUID
from fastapi import  FastAPI, Request, Form
from models import open_for_reading, open_for_writing
from fastapi.templating import Jinja2Templates
from routers import providers
from fastapi.staticfiles import StaticFiles
import uvicorn
from prometheus_client import start_http_server, Summary
import random
import time
from starlette_exporter import PrometheusMiddleware, handle_metrics


#REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"), name="static")
app.include_router(providers.router)
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})

# @REQUEST_TIME.time()
# def process_request(t):
#     """A dummy function that takes some time."""
#     time.sleep(t)

@app.get("/providers")
def read_root(request: Request) -> list:
    """
    returns the entire dictionary
    """
    provider_data = open_for_reading()
    if provider_data:
        return templates.TemplateResponse("display_provider.html", {
            "request": request, 
            "provider_data": provider_data
            })
    else:
        return {"message": "database empty"}


@app.get("/provider_search_form")
def render_search_form(request: Request):
    """
    renders the page for entering providerID
    """
    return templates.TemplateResponse("search_form.html", {"request": request})


@app.post("/search_provider")
def search_provider(request: Request, provider_id:UUID = Form(...)):
    """
    renders details of the given provider with it ID
    """
    provider_data = open_for_reading()
    if provider_data:
        try :
            data = provider_data[str(provider_id)]
        except KeyError:
            return {"message": "invalid provider ID"}
        return templates.TemplateResponse("provider_details.html", {
            "request": request,
            "provider_id": provider_id,
            "provider_data": data
            })
    else: 
        return {"message": "database error"}



@app.get("/create_provider_form")
def render_creation_form(request: Request):
    """
    displays form for entering provider data
    """
    return templates.TemplateResponse("creation_form.html",{'request': request})


@app.post("/create_provider_form")
def create_provider(
    provider_id:UUID = Form(...),
    name:str = Form(...),
    qualification:str = Form(...),
    speciality:str = Form(...),
    phone:str = Form(...),
    department:Optional[str] = Form("N/A"),
    organization:str = Form(...),
    location:Optional[str] = Form("N/A"),
    address:str = Form(...),
    active:bool = Form(...)
    ):
    """
    creating new user and saving the data
    """

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
    if str(provider_id) in provider_data.keys():
        response = {"message": "ID already exists"}
    else:
        provider_data[str(provider_id)] = post_data
        open_for_writing(data=provider_data)
        response = {"message": "provider created"}

    return response



@app.get("/delete_provider_form")
def render_deletion_form(request: Request):
    """
    displays the dropdown list for seleting user to delete
    """
    provider_data = open_for_reading()
    return templates.TemplateResponse("deletion_form.html", {
        "request": request,
        "provider_data": provider_data
        })


@app.post("/delete_provider")
def delete_provider(provider_id:UUID = Form(...)):
    """
    deleting the provider
    """
    provider_data = open_for_reading()
    if provider_data and str(provider_id) in provider_data.keys():
        del_data = provider_data.pop(str(provider_id))
        open_for_writing(data=provider_data)
        return {"message": del_data}
    return {"message": f'invalid ID : {provider_id}'}



@app.get("/update_provider_form")
def render_selection_menu(request: Request):
    """
    displays dropdown to select provider to update
    """
    provider_data = open_for_reading()
    return templates.TemplateResponse("update_provider_form.html", {
        "request": request,
        "provider_data": provider_data
        })


@app.post("/select_update_provider")
def render_update_form(request: Request, provider_id:UUID = Form(...)):
    """
    renders the updation form
    """
    provider_data = open_for_reading()
    if str(provider_id) in provider_data.keys():
        data_to_update = provider_data[str(provider_id)]

    return templates.TemplateResponse("updation_form.html", {
        "request": request,
        "provider_id": provider_id,
        "provider_data": data_to_update})


@app.post("/update_provider")
def update_provider(
    provider_id:UUID = Form(...),
    name:str = Form(...),
    qualification:str = Form(...),
    speciality:str = Form(...),
    phone:str = Form(...),
    department:Optional[str] = Form("N/A"),
    organization:str = Form(...),
    location:Optional[str] = Form("N/A"),
    address:str = Form(...),
    active:bool = Form(...)
    ):
    """
    updates the provider details filled in the form
    """

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



if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=False, root_path="/")
    # start_http_server(8000)

    # while True:
    #     process_request(random.random())


