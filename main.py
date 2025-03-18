from fastapi import FastAPI, Response, Depends, HTTPException, Request, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from auth import create_access_token, create_refresh_token, verify_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from models import UserLogin
from jose import JWTError
from icecream import ic

app = FastAPI()
app.mount('/static', StaticFiles(directory='frontend'), name='static')

# Configuración de CORS (para desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Origen del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Página de inicio de sesión
@app.get("/", response_class=HTMLResponse)
def login_page():
    with open("frontend/index.html", "r") as file:
        return HTMLResponse(content=file.read())

# Endpoint de login
@app.post("/login")
def login(user_data: UserLogin, response: Response):
    try:
        if user_data.username != "admin" or user_data.password != "password":
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        ic(user_data.username)
        ic(user_data.password)

        access_token = create_access_token(data={"sub": user_data.username})
        refresh_token = create_refresh_token(data={"sub": user_data.username})

        ic(access_token)
        ic(refresh_token)

        # Configurar cookies
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=True,  
            samesite="strict",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # 15 minutos
        )
        response.set_cookie(
            key="refresh_token",
            value=f"Bearer {refresh_token}",
            httponly=True,
            secure=True,  
            samesite="strict",
            max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60  # 7 días
        )

        return RedirectResponse(url="/home", status_code=303)
    except Exception as e:
        print(e)

# Endpoint para refrescar el access token
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
            secure=True, 
            samesite="strict",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # 15 minutos
        )
        return {"message": "Token actualizado"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token inválido o expirado")

# Página home
@app.get("/home", response_class=HTMLResponse)
def home_page(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        return RedirectResponse(url="/", status_code=303)

   