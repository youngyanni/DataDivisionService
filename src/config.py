from request_handlers import split_data
class RabbitConfig:
    # RabbitMQ Main Configuration
    HOST = 'rabbit'
    PORT = 5672
    USER = 'quest2'
    PASSWORD = 'quest2'


class MainTopic:
    # RabbitMQ Main Topic Names
    MAIN = 'manager_in'
    ERROR = 'error-message'


class ServiceConfig:
    # RabbitMQ Provider Configuration
    NAME = 'data_division_service'
    TOPIC_NAME = 'data_division_service_topic'

class RequestStatus:
    SPLIT = 'SPLIT'
def ERROR_MESSAGE(errorType, errorMessage, datetime):
    return {
        "errorType": errorType,
        "errorMessage": errorMessage,
        "localDateTime": datetime
    }

REQUEST_HANDLER_MAP = {
    RequestStatus.SPLIT: {
        'request_handler': split_data,
        'comp_request_keys': {
            'model_name': 'classifier',
            'raw_params': 'options'
        },
        'comp_response_keys': {
            'serialized_model': {'serializedModelData': ['model']}
        },
        'topic_name': MainTopic.MAIN
    }
}