from passlib.context import CryptContext

# Bcrypt setup
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    """
    Password ko hash karta hai. 
    [:72] isliye lagaya hai kyunki bcrypt 72 characters se zyada support nahi karta.
    """
    return pwd_context.hash(password[:72])


def verify_password(plain_password: str, hashed_password: str):
    """
    Plain password ko hashed password se match karta hai.
    """
    return pwd_context.verify(plain_password[:72], hashed_password)