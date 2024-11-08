import json
from datetime import datetime, date
from werkzeug.wrappers import Response


class DateTimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


def ApiResponse(status_code: int, message: str, data=None, error=None):
    if data is None:
        data = []

    if error is None:
        error = []

    response = {
        'meta': {
            'status_code': status_code,
            'message': message,
        },
        'data': data,
        'error': error
    }

    api_response = Response(json.dumps(response, cls=DateTimeEncoder),
                            content_type="application/json")
    api_response.status_code = status_code

    return api_response
