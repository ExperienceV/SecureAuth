from pydantic import BaseModel

class UserLogin(BaseModel):
    """
    Modelo para validar los datos de inicio de sesión.
    """
    username: str
    password: str