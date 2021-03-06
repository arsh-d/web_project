from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from models import open_for_reading, open_for_writing, create_provider, update_provider

router = APIRouter(
    prefix="/api/providers",
)

@router.get("/")
def read_root() -> dict:
    """
        returns the entire dictionary.
    """
    provider_data = open_for_reading()
    if provider_data:
        return provider_data
    else:
        return {"message": "database empty"}


@router.get("/{provider_id}")
def get_by_ID(provider_id: str) -> dict:
    """ 
        returns provider by passed provider id in the dictionary.
    """
    provider_data = open_for_reading()
    if provider_id in provider_data.keys():
        return provider_data[provider_id]
    else:
        return {"message": "provider does not exists"}


@router.post("/post_provider")
def push_data(provider: create_provider) -> dict:
    """
        inserts new provider into the dictionary.
    """
    provider_data = open_for_reading()
    if provider_data:
        new_id = str(provider.providerID)
        new_dict = provider.dict()
        new_dict.pop('providerID')
        provider_data[new_id] = new_dict
        open_for_writing(data=provider_data)
        return {"provider": provider.dict()}
    else:
        return {"message": "cannot push data"}


@router.delete("/{provider_id}")
def delete_provider(provider_id: str) -> dict:
    """
        delete the provider of given ID.
    """
    provider_data = open_for_reading()
    if provider_data:
        del_data = provider_data.pop(provider_id)
        open_for_writing(data=provider_data)
        return {"message": "post has been deleted",
                "provider": del_data}
    else:
        return {"message": "error in deleting"}


@router.put("/update/{provider_id}")
def put_provider(provider_id: str, provider: update_provider) -> dict:
    """
        updates the provider of given ID.
    """
    provider_data = open_for_reading()
    if provider_data:
        encoded_provider = jsonable_encoder(provider)
        provider_data[provider_id] = encoded_provider
        open_for_writing(data=provider_data)
        return encoded_provider
    else:
        return {"message": "data not updated"}
