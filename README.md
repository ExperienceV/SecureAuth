# SecureAuth
In this repository I will show the correct way to create a user authentication system.

# Authentication System with FastAPI and JWT

This project demonstrates how to build a secure authentication system using **FastAPI** (a modern Python framework for APIs) and **JWT** (JSON Web Tokens). It allows users to log in, obtain access and refresh tokens, and access protected routes.

---

## What Does This Project Do?

1. **User Login**:
   - Users submit their username(admin) and password(123).
   - If valid, the backend generates two tokens:
     - **Access Token**: Short-lived (15 minutes) for accessing protected routes.
     - **Refresh Token**: Long-lived (7 days) to renew the access token when it expires.

2. **Protected Routes**:
   - Certain routes require authentication.
   - The backend verifies the access token before granting access.

3. **Token Renewal**:
   - When the access token expires, the frontend uses the refresh token to get a new one without requiring the user to log in again.

4. **Logout**:
   - Users can log out, which deletes the cookies and redirects them to the login page.

---

## How to use?

1. **Test its functionality**:
   - Enter the following link:
        https://secure-auth-ebon.vercel.app/

   - Enter the following values:
        username: admin
        password: 123

   - Verify the tokens
        Go to "Inspect" on the page or press "CTRL + SHIFT + I" and look for the Cookies section, located in the
        application section.
        There you'll find the access and refresh tokens.
     
2. **Test the code**:
   - Copy the repository locally
   - Create and activate a Python virtual environment
   - Install the dependencies with "pip install -r requirements.txt"
   - With the terminal pointing to the root directory, start the server locally with "uvicorn main:app --reload"
     and redirect to the URL provided by uvicorn.
   - The rest is up to you. 🚬🗿
   





