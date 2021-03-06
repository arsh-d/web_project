from pydantic import BaseModel
from typing import Optional
from uuid import UUID
import pickle

# cursor =  open('provider_data.pkl', 'rb')
# providerDB = pickle.load(cursor)

def open_for_reading(filename='provider_data.pkl') -> dict:

    with open(filename, 'rb') as file:
        try:
            data = pickle.load(file)
        except :
            print("reading error")
    return data

def open_for_writing(filename='provider_data.pkl', data=None):

    if data:
        try:
            with open(filename, 'wb') as file:
                pickle.dump(data, file)
        except :
            print("writting error")

# providerDB = []

class provider_base(BaseModel):
    name: str
    qualification: str
    speciality: str
    phone: str
    department: Optional[str]
    organization: str
    location: Optional[str]
    address: str

class Provider(provider_base):
    providerID: UUID
    active: Optional[bool] = True

class update_provider(provider_base):
    pass

class create_provider(Provider):
    pass