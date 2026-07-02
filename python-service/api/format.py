from rest_framework.response import Response
from rest_framework import status

def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    """
    Returns a standardized JSON success response.
    """
    return Response({
        "status": "success",
        "message": message,
        "data": data
    }, status=status_code)

def error_response(error_message, details=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Returns a standardized JSON error response.
    """
    payload = {
        "status": "error",
        "message": error_message
    }
    if details:
        payload["details"] = details
        
    return Response(payload, status=status_code)
