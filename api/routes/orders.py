'''
    @author: Giovanni Junco
    @since: 07-06-2024
    @summary: create app
'''
from fastapi import APIRouter, status, Body, Response


from api.models import OrderModel

from api.controllers import OrderOperations
from api.jaeger import tracer

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_description="List all orders user", status_code=status.HTTP_200_OK)
async def get_list(page=1,limit=10,user_owner='', response=Response):
    '''
    List all of the order data in the database. The response is paginated and limited results.
    require:
            page: indicates which order list session will be returned. depends on the limit arg
            limit: indicates how many orders will each page have
            user_owner: returns only the commands of the user owner
        return:
            order_info: list with one item with order created,        
            message: confirmation of saved order,
            status: number of response (200),'''
    #add requets to Jaeger
    with tracer.start_as_current_span('get_list'):
        print('Jaeger get')
    new_student = await OrderOperations().order_list(page,limit,user_owner)
    response.status_code = new_student['status']
    return new_student

@router.get(
    "/{id}"
)
async def get_order(id='', response=Response):
    '''
    Get the record for a specific order, looked up by `id`.
    require:
            id: order indicator
        return:
            order_info: list with one item with order created,        
            message: confirmation of saved order,
            status: number of response (200),'''
    with tracer.start_as_current_span('get_order'):
        pass
    new_student = await OrderOperations().show_order(id)
    response.status_code = new_student['status']
    return new_student

@router.post(
    "/",
    response_description="Add new order",
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_order(order: OrderModel = Body(...), response=Response):
    ''' connect post request with add order function
        require:
            order: order data to save
        return:
            order_info: list with one item with order created,        
            message: confirmation of saved order,
            status: number of response (201),''' 
    #add requets to Jaeger
    with tracer.start_as_current_span('create_order'):
        pass
    order=order.model_dump()
    new_student = await OrderOperations().add_order(order)
    response.status_code = new_student['status']
    return new_student

@router.put(
    "/{id}",
    response_description="Update a order",
    response_model=OrderModel,
    response_model_by_alias=False,
)
async def put_order(id: str, order: OrderModel = Body(...), response=Response):
    ''' Update individual fields of an existing order record.
        require:
            id: order indicator to update
            order: order data to save
        return:
            order_info: list with one item with order created,        
            message: confirmation of saved order,
            status: number of response (200),''' 
    #add requets to Jaeger
    with tracer.start_as_current_span('put_order'):
        pass
    order=order.model_dump()
    new_student = await OrderOperations().update_order(order,id)
    response.status_code = new_student['status']
    return new_student


@router.delete("/{id}", response_description="Delete a order")
async def remove_order(id: str, response=Response):
    '''
    Remove a single order record from the database.
    require:
            id: order indicator to delete
        return:
            order_info: list with one item with order created,        
            message: confirmation of saved order,
            status: number of response (200),'''
    #add requets to Jaeger
    with tracer.start_as_current_span('remove_order'):
        pass
    new_student = await OrderOperations().delete_order(id)
    response.status_code = new_student['status']
    return new_student