'''
    @author: Giovanni Junco
    @since: 07-03-2024
    @summary: connection with mongodb
''''''
    @author: Giovanni Junco
    @since: 07-03-2024
    @summary: connection with mongodb
'''
from typing import Optional, List
from pydantic import ConfigDict, BaseModel, Field, EmailStr

class FormsModel(BaseModel):
    """ Container for a single form. """    
    type_id: int          
    content: dict
    percentage_completed: dict

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "type": 1,  
                "data": {},
                "percentage_completed": 0.5
            }
        },
    )

class FormsTypes(BaseModel):
    """ Container for a single form. """    
    id: int          
    title: str
    items: dict

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "id": 1,  
                "title": ""
            }
        },
    )
