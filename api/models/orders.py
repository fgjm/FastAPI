'''
    @author: Giovanni Junco
    @since: 07-03-2024
    @summary: connection with mongodb
'''
from typing import Optional, List
from datetime import datetime
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from .forms import FormsModel

class BasicData(BaseModel):
    """ Container order basic data. """    
    company_name: str
    nit: str
    Legal_representative: str
    office_address: str
    city: str
    web_site: str
    mail: EmailStr
    phone: int
    taxable_year: int

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "company_name": "company abc",
                "nit": "90.425.258",
                "Legal_representative": "John Doe",
                "office_address": "25th street  # 49 - 44",
                "web_site": "abc.com",
                "mail": "jdoe@x.edu.ng",
                "phone": 3114368975,
                "taxable_year": 2023
            }
        },
    )

class AuditTeam(BaseModel):   
    """ Container staff order. """     
    partner: str
    audit_manager: str
    auditor_charge_1: str
    auditor_charge_2: str

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "partner": "John Smith",
                "audit_manager": "Li Abc",
                "auditor_charge_1": "Jane Doe",
                "auditor_charge_2": "Abc Dfg"
            }
        },
    )


class OrderModel(BaseModel):
    """ Update a single order record. """
    user_owner: int
    order_license: int       
    basic_data: BasicData = Field(default=None)
    audit_team: Optional[AuditTeam] = Field(default=None)
    forms: Optional[List[FormsModel]] = Field(default=None)
    created: datetime = Field(default=datetime.utcnow().strftime('%y-%m-%dT%H:%M:%S.%fZ'))
    modificated: Optional[datetime] = Field(default=None)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "user_owner": 1,
                "order_license": 2,        
                "basic_data": {},
                "audit_team": {},
                "forms": [],
                "created": "2021-12-03T18:26:00.777Z",
                "modificated": "2021-12-05T19:20:00.777Z"
            }
        },
    )
