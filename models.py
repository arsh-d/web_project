from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

providerDB = []

class provider_base(BaseModel):
    name: str
    qualification: List[str] = []
    speciality: List[str] = []
    phone: List[str] = []
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