'''
    @author: Giovanni Junco
    @since: 07-03-2024
    @summary: curl functions
'''
import sys
from fastapi import status
from bson.objectid import ObjectId
from api.models import order_collection, ResponseModel, ErrorResponseModel
from logs import get_error

class OrderOperations:

    def order_helper(self, order) -> dict:
        """ rename the key dictionary response: _id with id. """
        try:
            order["id"]= str(order["_id"])
            order.pop("_id",None)
            return order
        except:
            return get_error('order_helper, api route',sys.exc_info())

    async def order_list(self, page,limit,user_owner):
        """
        List all of the order data in the database.
            The response is unpaginated and limited to 100 results.
        """
        try:
            
            orders_found=[]
            async for order in order_collection.find():
                orders_found.append(self.order_helper(order))
            return  ResponseModel(
                        orders_found, 
                        'orders_found' if orders_found else 'orders_empty', 
                        status.HTTP_200_OK if orders_found else status.HTTP_204_NO_CONTENT
                    )
        except:
            return get_error('list_orders, api route',sys.exc_info())

    async def show_order(self, id):
        """
        Get the record for a specific order, looked up by `id`.
        """
        try:
            if (
                order := order_collection.find_one({"id": ObjectId(id)})
            ) is not None:
                return ResponseModel(
                        order, 
                        'order_found', 
                        status.HTTP_200_OK
                    )
            return ErrorResponseModel(
                        f"order {id} not found", 
                        f"not_found", 
                        status.HTTP_404_NOT_FOUND
                    )
        except:
            return get_error('get_order, api route',sys.exc_info())
    
    async def add_order(self, order: dict) -> dict:
        """ Insert a new order record. """
        try:
            order = await order_collection.insert_one(order)
            new_order = await order_collection.find_one({"_id": ObjectId(order.inserted_id)})
            return ResponseModel(
                    self.order_helper(new_order), 
                    'order_created', 
                    status.HTTP_201_CREATED
                )
        except:
            return get_error('create_order, api route',sys.exc_info())

    async def update_order(self, id, order):
        """
        Update individual fields of an existing order record.

        Only the provided fields will be updated.
        Any missing or `null` fields will be ignored.
        """
        order = {
            k: v for k, v in order.items() if v is not None
        }

        if len(order) >= 1:
            update_result = order_collection.find_one_and_update(
                {"_id": id},
                {"$set": order}
            )
            if update_result is not None:
                return ResponseModel(
                        update_result, 
                        'order_update', 
                        status.HTTP_200_OK
                    )
            else:
                return ErrorResponseModel(
                        f"order {id} not found", 
                        f"not_found", 
                        status.HTTP_404_NOT_FOUND
                    )

        # The update is empty, but we should still return the matching document:
        if (existing_order := order_collection.find_one({"_id": id})) is not None:
            return existing_order

        return ErrorResponseModel(
                        f"order {id} not found", 
                        f"not_found", 
                        status.HTTP_404_NOT_FOUND
                    )

    async def delete_order(self, id):
        """
        Remove a single order record from the database.
        """
        delete_result = order_collection.delete_one({"_id": id})

        if delete_result.deleted_count == 1:
            return ResponseModel(
                    '', 
                    'order_deleted', 
                    status.HTTP_204_NO_CONTENT
                )
        return ErrorResponseModel(
                        f"order {id} not found", 
                        f"not_found", 
                        status.HTTP_404_NOT_FOUND
                    )
