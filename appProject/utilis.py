from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def passwordHash(password: str):
    return pwd_context.hash(password)


def passwordVerify(plainPassword: str, hashedPassword: str):
    return pwd_context.verify(plainPassword, hashedPassword)
