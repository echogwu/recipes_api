from json import JSONEncoder
from decimal import Decimal


class JsonDecimalEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return JSONEncoder.default(self, obj)
