# core/auth.py
import hashlib
import streamlit as st
from core.database import SessionLocal, User

SALT = b"enterprise_talent_suite_salt_2026"

def hash_password(password: str) -> str:
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), SALT, 100000).hex()

def verify_password(stored_hash: str, password: str) -> bool:
    return hash_password(password) == stored_hash

def authenticate_user(username_or_email: str, password: str):
    db = SessionLocal()
    user = db.query(User).filter(
        (User.username == username_or_email) | (User.email == username_or_email)
    ).first()
    db.close()
    
    if user and verify_password(user.password_hash, password):
        return user
    return None

def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_role" not in st.session_state:
        st.session_state.user_role = None
    if "username" not in st.session_state:
        st.session_state.username = None