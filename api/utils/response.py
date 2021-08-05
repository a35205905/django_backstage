from rest_framework import status
from rest_framework.response import Response

def custom_response(code=status.HTTP_200_OK, message='', data=None, **kwargs):
    return Response(
        data={
            'status': code,
            'message': message,
            'data': data
        },
        **kwargs
    )