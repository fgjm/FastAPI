'''
    @author: Giovanni Junco
    @since: 07-03-2024
    @summary: database connection
'''

import motor.motor_asyncio

from config import config
from .orders import OrderModel

MONGO_DETAILS = f"mongodb://{config["USERNAME"]}:{config["PASSWORD"]}@{config["HOST"]}"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.auditandodb

order_collection = database.get_collection("order")


def ResponseModel(data, message, status):
    return {
        "order_info": [data],        
        "message": message,
        "status": status,
    }

def ErrorResponseModel(error, message, status):
    return {
        "error": error, 
        "message": message,
        "status": status,
    }