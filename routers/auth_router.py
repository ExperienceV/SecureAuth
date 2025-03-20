from fastapi import APIRouter, HTTPException, Response, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from modules.auth import create_access_token, create_refresh_token, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from modules.models import UserLogin
from modules.auth import verify_token
from jose import JWTError
from icecream import ic
from pathlib import Path

app = APIRouter()

# Set up Log in page
@app.get("/", response_class=HTMLResponse)
def login_page():
    path = Path('frontend/form.html')
    return path.read_text(encoding='utf-8')

# Log in process
@app.post("/login")
def login(user_data: UserLogin):
    try:
        if user_data.username != "admin" or user_data.password != "123":
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        ic(user_data.username)
        ic(user_data.password)

        access_token = create_access_token(data={"sub": user_data.username})
        refresh_token = create_refresh_token(data={"sub": user_data.username})

        ic(access_token)
        ic(refresh_token)

        # Crear una RedirectResponse
        response = RedirectResponse(url="/home", status_code=303)

        # Configurar cookies
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=False,  
            samesite="strict",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # 15 minutes
        )
        response.set_cookie(
            key="refresh_token",
            value=f"Bearer {refresh_token}",
            httponly=True,
            secure=False,  
            samesite="strict",
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60  # 7 days
        )

        return response
    except Exception as e:
        print(e)

# Log out process
@app.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Sesión cerrada"}

# Refresh token process
@app.post("/refresh-token")
def refresh_token(response: Response, refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token no proporcionado")

    try:
        payload = verify_token(refresh_token.replace("Bearer ", ""))
        username = payload.get("sub")
        new_access_token = create_access_token(data={"sub": username})

        # Enviar el nuevo access token en una cookie
        response.set_cookie(
            key="access_token",
            value=f"Bearer {new_access_token}",
            httponly=True,
            secure=False, 
            samesite="strict",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # 15 minutos
        )
        return {"message": "Token actualizado"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token inválido o expirado")
