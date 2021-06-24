from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

providerDB = []

class Provider(BaseModel):
    providerID: UUID
    active: Optional[bool] = True
    name: str
    qualification: List[str] = []
    speciality: List[str] = []
    phone: List[str] = []
    department: Optional[str]
    organization: str
    location: Optional[str]
    address: str
