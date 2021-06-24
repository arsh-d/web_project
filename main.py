import uuid
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List,Optional



app = FastAPI()

providerDB=[]

class Provider(BaseModel):
    providerID: uuid.UUID
    active: Optional[bool] = True
    name: str
    qualification: List[str] = []
    speciality: List[str] = []
    phone: List[str] = []
    department: Optional[str]
    organization: str
    location: Optional[str]
    address: str



@app.get("/providers")
def read_root():
    return providerDB

@app.get("/providers/{provider_id}")
def get_by_ID(provider_id: int):
    return providerDB[provider_id]

@app.post("/post_provider")
def push_data(provider: Provider):
    providerDB.append(provider.dict())
    return {"provider":providerDB[-1]}

@app.delete("/provider/{provider_id}")
def delete_provider(provider_id: int):
    provider = providerDB.pop(provider_id)
    return {"msg": "post has been deleted",
            "provider": provider}

@app.put("/providers/update/{provider_id}")
def update_provider(provider_id: int, provider: Provider):
    encoded_provider = jsonable_encoder(provider)
    providerDB[provider_id] = encoded_provider
    return encoded_provider