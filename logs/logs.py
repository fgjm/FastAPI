'''
    @author: Giovanni Junco
    @since: 01-03-2024
    @summary: Log settings
'''
import logging
from pythonjsonlogger import jsonlogger

logging.basicConfig( level=logging.INFO )

logHandler = logging.FileHandler('FatsAPI.log')
logHandler.setLevel(logging.DEBUG)

class CustomDebugnFormatter(jsonlogger.JsonFormatter):
    ''' Log schema default    '''
    def add_fields(self, log_record, record, message_dict):
        server = 'FatsAPI-DB'
        super(CustomDebugnFormatter, self).add_fields(
            log_record, record, message_dict)
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
            log_record['server'] = server
            
formatter = CustomDebugnFormatter(
    '%(server)s %(asctime)s %(level)s %(name)s %(message)s')

logHandler.setFormatter(formatter)
logging.getLogger('').addHandler(logHandler)
consola_handler = logging.StreamHandler()
consola_handler.setLevel(logging.INFO)

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    ''' Log schema default    '''
    def add_fields(self, log_record, record, message_dict):
        server = 'FatsAPI-DB'
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict)
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
            log_record['server'] = server
            
consola_handler_formatter = CustomJsonFormatter(
    '%(server)s %(asctime)s %(level)s %(name)s %(message)s')

consola_handler.setFormatter(consola_handler_formatter)
