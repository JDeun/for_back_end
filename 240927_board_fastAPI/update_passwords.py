from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import User
from auth import get_password_hash

def update_user_passwords():
    db = SessionLocal()
    users = db.query(User).all()
    for user in users:
        if not user.hashed_password.startswith('$2b$'):  # bcrypt 해시 접두사 확인
            hashed_password = get_password_hash(user.hashed_password)
            user.hashed_password = hashed_password
    db.commit()
    db.close()

if __name__ == "__main__":
    update_user_passwords()
    print("All user passwords have been updated.")