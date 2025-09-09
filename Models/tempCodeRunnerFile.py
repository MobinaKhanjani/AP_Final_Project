from sqlmodel import SQLModel
import bcrypt

# در فایل user.py
import bcrypt  # ✅ اینجا import بشه

class User(SQLModel):
    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(...)  # ✅ اینجا استفاده بشه
    
    #باید حذف بشه