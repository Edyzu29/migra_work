import requests
from routs import *

def post_data(body):
    return requests.post(url= URL_SERVICE,
                         json= body)