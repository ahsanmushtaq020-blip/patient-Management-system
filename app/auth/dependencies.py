from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.database.mongodb import user_collection

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:

            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        user = user_collection.find_one(
            {"email": email}
        )

        if not user:

            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        user["_id"] = str(user["_id"])

        return user

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


# ADMIN ONLY
def admin_only(
    user = Depends(get_current_user)
):

    if user.get("role") != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin only access"
        )

    return user


# DOCTOR ONLY
def doctor_only(
    user = Depends(get_current_user)
):

    if user.get("role") != "doctor":

        raise HTTPException(
            status_code=403,
            detail="Doctor only access"
        )

    return user


# PATIENT ONLY
def patient_only(
    user = Depends(get_current_user)
):

    if user.get("role") != "patient":

        raise HTTPException(
            status_code=403,
            detail="Patient only access"
        )

    return user