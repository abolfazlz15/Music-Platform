from typing import Union

from rest_framework.response import Response


def response(
    *, data: Union[dict, list, None] = None, status: int, error: str | None = None
):
    success = status < 400

    return Response(
        data={
            "data": data,
            "success": success,
            "status": status,
            "error": error,
        },
        status=status,
    )
