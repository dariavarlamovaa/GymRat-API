from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(not_hashed_password: str) -> str:
    return pwd_context.hash(not_hashed_password)