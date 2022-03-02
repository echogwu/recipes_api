from flask import request
from typing import Tuple, Any

from marshmallow import Schema


def get_request_args(schema: Schema) -> Tuple[dict, Any]:
    """
    Returns a Tuple of the form (data, errors)
    """
    data = {}  # type: dict

    if request.json:
        data.update(**request.json)

    if request.values:
        data.update(**request.values.to_dict())

    print(f"request.json: {request.json}")
    print(f"request.values: {request.values.to_dict()}")
    return schema.load(data)