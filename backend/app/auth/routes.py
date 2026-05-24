from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import requests
import os
import re
import random
from dotenv import load_dotenv
from app.core.hash import hash_password, verify_password
from fastapi import Depends
from app.core.deps import get_current_user

# ✅ MongoDB
from app.db.mongo import users_collection

load_dotenv()

router = APIRouter()


# =========================
# 🧾 MODELS
# =========================
class SignupUser(BaseModel):
    name: str
    email: str
    password: str


class LoginUser(BaseModel):
    email: str
    password: str

# =========================
# 🔹 EMAIL VALIDATION
# =========================
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# =========================
# 🔹 OTP GENERATOR
# =========================
def generate_otp():
    return str(random.randint(100000, 999999))

# =========================
# 🟢 SIGNUP
# =========================
@router.post("/signup")
def signup(user: SignupUser):

    print("Signup hit:", user.email)

    if not is_valid_email(user.email):
        return {"error": "Invalid email format ❌"}

    existing = users_collection.find_one({"email": user.email})

    if existing and not existing.get("verified"):
        otp = generate_otp()

        users_collection.update_one(
            {"email": user.email},
            {"$set": {"otp": otp}}
        )

        print("OTP (resend):", otp)

        return {"message": "OTP resent"}

    if existing:
        return {"error": "User already exists"}

    otp = generate_otp()

    safe_password = user.password[:72]  # 🔥 FIX
    hashed = hash_password(safe_password)

    users_collection.insert_one({
        "name": user.name,
        "email": user.email,
        "password": hashed,
        "otp": otp,
        "verified": False,
        "provider": "local"
    })

    print("OTP:", otp)

    return {"message": "Signup successful, verify OTP"}
# =========================
# 🔵 VERIFY OTP
# =========================
@router.post("/verify-otp")
def verify_otp(data: dict):
    email = data.get("email")
    otp = data.get("otp")

    user = users_collection.find_one({"email": email})

    if not user:
        return {"error": "User not found"}

    if user.get("otp") == otp:
        users_collection.update_one(
            {"email": email},
            {"$set": {"verified": True}}
        )
        return {"message": "Account verified ✅"}

    return {"error": "Invalid OTP ❌"}

# =========================
# 🔵 LOGIN
# =========================
@router.post("/login")
def login(user: LoginUser):

    db_user = users_collection.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")

    if not db_user.get("verified"):
        return {"error": "Please verify your email first ❌"}

    if not verify_password(user.password[:72], db_user.get("password")):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {"message": "Login successful", "token": token}

# =========================
# 🔒 PROTECTED ROUTE
# =========================
@router.get("/protected")
def protected(user=Depends(get_current_user)):
    return {
        "message": "Protected route access ✅",
        "user": user
    }

# =========================
# 🔁 FORGOT PASSWORD
# =========================
@router.post("/forgot-password")
def forgot_password(data: dict):
    email = data.get("email")

    user = users_collection.find_one({"email": email})
    if not user:
        return {"error": "User not found"}

    otp = generate_otp()

    users_collection.update_one(
    {"email": email},
    {"$set": {"verified": True}, "$unset": {"otp": ""}}
)

    print("Reset OTP:", otp)

    return {"message": "OTP sent for reset"}

# =========================
# 🔁 RESET PASSWORD
# =========================
@router.post("/reset-password")
def reset_password(data: dict):
    email = data.get("email")
    otp = data.get("otp")
    new_password = data.get("password")

    user = users_collection.find_one({"email": email})

    if not user or user.get("otp") != otp:
        return {"error": "Invalid OTP ❌"}

    hashed = hash_password(new_password[:72])

    users_collection.update_one(
        {"email": email},
        {"$set": {"password": hashed}}
    )

    return {"message": "Password reset successful ✅"}
# =========================
# 🔴 GOOGLE OAUTH (FIXED)
# =========================
from app.core.security import create_access_token  # ⚠️ top me import add karo
from fastapi.responses import RedirectResponse
import os

@router.get("/google")
def google_login():

    client_id = os.getenv("GOOGLE_CLIENT_ID")

    if not client_id:
        return {"error": "Google Client ID missing"}

    url = (
    "https://accounts.google.com/o/oauth2/v2/auth"
    f"?client_id={client_id}"
    "&response_type=code"
    "&scope=email profile"
    "&redirect_uri=http://localhost:8000/api/auth/google/callback"
    "&prompt=select_account"   # 🔥 THIS FIX
)

    return RedirectResponse(url)
@router.get("/google/callback")
def google_callback(code: str):

    print("🔥 GOOGLE CALLBACK HIT")   # ✅ YAHAN

    token_res = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "redirect_uri": "http://localhost:8000/api/auth/google/callback",
            "grant_type": "authorization_code",
        },
    )

    token = token_res.json()

    if "access_token" not in token:
        return {"error": token}

    user = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {token['access_token']}"},
    ).json()

    print("USER:", user)   # ✅ YAHAN

    # ✅ Save in MongoDB
    existing = users_collection.find_one({"email": user.get("email")})

    if not existing:
        users_collection.insert_one({
            "name": user.get("name"),
            "email": user.get("email"),
            "password": None,
            "provider": "google",
            "verified": True
        })

    # 🔥 JWT generate
    jwt_token = create_access_token({"sub": user.get("email")})

    # 🔥 Redirect with token
    return RedirectResponse(
        f"http://localhost:5173/oauth-success?token={jwt_token}"
    )
# =========================
# 🔵 FACEBOOK (FIXED)
# =========================
@router.get("/facebook")
def fb_login():
    client_id = os.getenv("FACEBOOK_CLIENT_ID")

    url = (
        "https://www.facebook.com/v19.0/dialog/oauth"
        f"?client_id={client_id}"
        "&redirect_uri=http://localhost:8000/api/auth/facebook/callback"
        "&scope=email"
    )
    return RedirectResponse(url)


@router.get("/facebook/callback")
def fb_callback(code: str):
    token = requests.get(
        "https://graph.facebook.com/v19.0/oauth/access_token",
        params={
            "client_id": os.getenv("FACEBOOK_CLIENT_ID"),
            "client_secret": os.getenv("FACEBOOK_CLIENT_SECRET"),
            "redirect_uri": "http://localhost:8000/api/auth/facebook/callback",
            "code": code,
        },
    ).json()

    if "access_token" not in token:
        return {"error": token}

    user = requests.get(
        "https://graph.facebook.com/me?fields=id,name,email",
        params={"access_token": token["access_token"]},
    ).json()

    return user


# =========================
# 🔵 LINKEDIN (FIXED)
# =========================
@router.get("/linkedin")
def linkedin_login():
    client_id = os.getenv("LINKEDIN_CLIENT_ID")

    url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        f"?response_type=code"
        f"&client_id={client_id}"
        "&redirect_uri=http://localhost:8000/api/auth/linkedin/callback"
        "&scope=r_liteprofile r_emailaddress"
    )
    return RedirectResponse(url)


@router.get("/linkedin/callback")
def linkedin_callback(code: str):
    token = requests.post(
        "https://www.linkedin.com/oauth/v2/accessToken",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:8000/api/auth/linkedin/callback",
            "client_id": os.getenv("LINKEDIN_CLIENT_ID"),
            "client_secret": os.getenv("LINKEDIN_CLIENT_SECRET"),
        },
    ).json()

    if "access_token" not in token:
        return {"error": token}

    user = requests.get(
        "https://api.linkedin.com/v2/me",
        headers={"Authorization": f"Bearer {token['access_token']}"},
    ).json()

    return user