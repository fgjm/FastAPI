'''
    @author: Giovanni Junco
    @since: 01-03-2024
    @summary: print log, send log file to save in MongoDB and Errors 500
'''
import json
import requests
import datetime
from fastapi import status
from .logs import logging
from config import config
from api.models import ErrorResponseModel

def do_log(tipo, messaje, from_log,type_log):
    ''' Print log in console depending on the type of message'''
    log=f'{tipo} : {messaje}'
    log+=f' From: {from_log}'
    if type_log=='info':
        logging.info(log)
    elif type_log=='error':
        logging.error(log)
    elif type_log=='critical':
        logging.critical(log)
    elif type_log=='warning':
        logging.warning(log)

def get_error(point,error):
    """ log and response error handling 500, provided by sys.exc_info()
        Required attributes:
            point (String): endpoint, resolve (function or class)
            error(object): data error sys.exc_info
        Return: 
            response: dict to graphql frontend
    """
    do_log(str(error),point,
            error[2].tb_lineno
            ,'error')
    return ErrorResponseModel(
                error=f'Point: {point}, Error: {str(error)}', 
                message= 'internal_error',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR )


date_send=datetime.datetime.now().strftime('%y%m%d')
def send_log():
    ''' Send the log file every day at 10:00 am'''
    try:
        global date_send
        time_now=int(datetime.datetime.now().strftime('%H%M%S'))
        time_send=100000
        date_now=datetime.datetime.now().strftime('%y%m%d')
        if time_now>time_send and date_send==date_now:
            List = []
            date_send=datetime.datetime.now() + datetime.timedelta(days=1)
            files = open('mongoGraphQL.log', 'r')
            for line in files.readlines():
                data = json.loads(line)
                List.append(data)
            response = requests.post(f"{config['IP_MONGODB_POST']}/logs/records/file", data=str(List))            
            response = 'ok'
            return response
    except Exception as error:            
        logging.error(error)
        return { 'message':"Error", "errors": [error] }
