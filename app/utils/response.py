from fastapi import HTTPException


def success_response(message, data=None):

    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(
    status_code,
    message
):

    raise HTTPException(
        status_code=status_code,
        detail={
            "success": False,
            "message": message,
            "data": None
        }
    )