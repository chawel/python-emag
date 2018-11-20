import requests
from functools import wraps
import inspect

def paginate(func):
    @wraps(func)
    def func_wrapper(*args, **kwargs):
        # Get default parameters
        default_params = inspect.signature(func).bind(*args, **kwargs)
        default_params.apply_defaults()

        # Set new kwargs based on default and passed params
        _kwargs = dict(default_params.arguments)

        first_time = True
        while True:
            # For the first time, don't increment page
            if first_time:
                first_time = False
            else:
                _kwargs['page'] = _kwargs['page'] + 1

            response = func(**_kwargs)
            if not response:
                break

            yield response
    return func_wrapper
            

class EMAGException(Exception):
    pass


class EMAGClient(object):
    API_URL = "https://marketplace-api.emag.pl/api-3"

    def __init__(self, user, secret):
        self.user = user
        self.secret = secret

    def call(self, resource, action, data=None):
        result = requests.post(
            self.API_URL + "/{}/{}".format(resource, action),
            json={'data': data},
            auth=(self.user, self.secret)
        )

        if result.json().get('isError', True) != False:
            _err = "Error code: {http_code} Response: {response_text}".format(http_code=result.status_code, response_text=result.text)
            raise EMAGException(_err)

        return result.json().get('results')

    def read(self, resource, data={}, page=1, per_page=1):
        _action = 'read'

        _data = {
            'status': 1,
            'currentPage': page, 
            'itemsPerPage': per_page
        }

        _data.update(data)

        return self.call(resource, _action, _data)

    @paginate
    def read_many(self, resource, data={}, page=1, per_page=100):
        _action = 'read'

        _data = {
            'status': 1,
            'currentPage': page, 
            'itemsPerPage': per_page
        }
        
        _data.update(data)

        return self.call(resource, _action, _data)

    def save(self, resource, data):
        _action = 'save'
        _data = data

        return self.call(resource, _action)

    def count(self, resource):
        _action = 'count'

        return self.call(resource, _action)

