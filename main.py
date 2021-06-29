from models import create_provider, update_provider, Provider, open_for_writing, open_for_reading
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
import pickle

app = FastAPI()



@app.get("/providers")
def read_root() -> list:
    """
        returns the entire database.
    """
    provider_data = open_for_reading()
    return provider_data

@app.get("/providers/{provider_id}")
def get_by_ID(provider_id: int) -> dict:
    """ 
        returns provider by passed provider index in the list.
    """
    provider_data = open_for_reading()
    return provider_data[provider_id]


@app.post("/post_provider")
def push_data(provider: create_provider) -> dict:
    """
        inserts new provider into the database.
    """
    
    provider_data = open_for_reading()
    provider_data.append(provider.dict())
    
    open_for_writing(data=provider_data)
    
    return {"provider": provider.dict()}


@app.delete("/provider/{provider_id}")
def delete_provider(provider_id: int) -> dict:
    """
        delete the provider at the given index.
    """
    
    provider_data = open_for_reading()
    del_data = provider_data.pop(provider_id)
    
    open_for_writing(data=provider_data)
    return {"msg": "post has been deleted",
            "provider": del_data}


@app.put("/providers/update/{provider_id}")
def put_provider(provider_id: int, provider: update_provider) -> dict:
    """
        updates the provider of given index.
    """
    provider_data = open_for_reading()
    encoded_provider = jsonable_encoder(provider)
    provider_data[provider_id] = encoded_provider
    open_for_writing(data=provider_data)
    return encoded_provider