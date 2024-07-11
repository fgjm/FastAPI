'''
    @author: Giovanni Junco
    @since: 07-06-2024
    @summary: create app
'''
import sys
from fastapi import APIRouter, Depends, status, Body, HTTPException, Response, Path
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from logs import get_error
from ..model import OrderModel, order_collection, ResponseModel
from typing import List

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

def order_helper(order) -> dict:
    order["id"]= str(order["_id"]),
    return order

@router.post(
    "/",
    response_description="Add new order",
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_order(order: OrderModel = Body(...)):
    """
    Insert a new order record.

    A unique `id` will be created and provided in the response.
    """
    try:        
        new_order = order_collection.insert_one(order.model_dump(by_alias=True, exclude=["id"]))
        print('POST:',new_order.inserted_id)
        created_order = order_collection.find_one(
            {"_id": new_order.inserted_id}
        )
        return created_order
    except:
        return get_error('create_order, api route',sys.exc_info())

@router.get("/", response_description="List all orders user")
async def list_orders():
    """
    List all of the order data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    try:
        orders_found=[]
        async for order in order_collection.find():
            orders_found.append(order_helper(order))
        return orders_found
    except:
        return get_error('list_orders, api route',sys.exc_info())

@router.get(
    "/{id}"
)
async def show_order(id:str=Path(...,min_length=3)):
    """
    Get the record for a specific order, looked up by `id`.
    """
    try:
        if (
            order := order_collection.find_one({"id": id})
        ) is not None:
            return order

        raise HTTPException(status_code=404, detail=f"order {id} not found")
    except:
        return get_error('get_order, api route',sys.exc_info())


@router.put(
    "/{id}",
    response_description="Update a order",
    response_model=OrderModel,
    response_model_by_alias=False,
)
async def update_order(id: str, order: OrderModel = Body(...)):
    """
    Update individual fields of an existing order record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    order = {
        k: v for k, v in order.model_dump(by_alias=True).items() if v is not None
    }

    if len(order) >= 1:
        update_result = order_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": order}
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"order {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_order := order_collection.find_one({"_id": id})) is not None:
        return existing_order

    raise HTTPException(status_code=404, detail=f"order {id} not found")


@router.delete("/{id}", response_description="Delete a order")
async def delete_order(id: str):
    """
    Remove a single order record from the database.
    """
    delete_result = order_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"order {id} not found")