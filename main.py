from models import create_provider, update_provider, providerDB, Provider
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

app = FastAPI()

@app.get("/providers")
def read_root() -> list:
    """
        returns the entire database.
    """
    return providerDB


@app.get("/providers/{provider_id}")
def get_by_ID(provider_id: int) -> dict:
    """ 
        returns provider by passed provider index in the list.
    """
    return providerDB[provider_id]


@app.post("/post_provider")
def push_data(provider: create_provider) -> dict:
    """
        inserts new provider into the database.
    """
    providerDB.append(provider.dict())
    return {"provider": providerDB[-1]}


@app.delete("/provider/{provider_id}")
def delete_provider(provider_id: int) -> dict:
    """
        delete the provider at the given index.
    """
    provider = providerDB.pop(provider_id)
    return {"msg": "post has been deleted",
            "provider": provider}


@app.put("/providers/update/{provider_id}")
def put_provider(provider_id: int, provider: update_provider) -> dict:
    """
        updates the provider of given index.
    """

    encoded_provider = jsonable_encoder(provider)
    providerDB[provider_id] = encoded_provider
    return encoded_provider