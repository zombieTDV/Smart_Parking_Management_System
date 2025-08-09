import hashlib
from src.database import db, Table

# Khởi tạo bảng
owner_table = Table("owners", db)
attendant_table = Table("attendants", db)

def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def owner_exists(username: str) -> bool:
    result = owner_table.find_record_with_value("username", username)
    return bool(result)

def attendant_exists(username: str) -> bool:
    result = attendant_table.find_record_with_value("username", username)
    return bool(result)

def register_owner(username: str, password: str):
    hashed = _hash_password(password)
    owner_table.insert(["username", "password"], (username, hashed))

def register_attendant(username: str, password: str):
    hashed = _hash_password(password)
    attendant_table.insert(["username", "password"], (username, hashed))

def validate_owner(username: str, password: str) -> bool:
    hashed = _hash_password(password)
    result = owner_table.db.execute(
        f"SELECT 1 FROM owners WHERE username = %s AND password = %s;",
        params=(username, hashed),
        fetch=True
    )
    return bool(result)

def validate_attendant(username: str, password: str) -> bool:
    hashed = _hash_password(password)
    result = attendant_table.db.execute(
        f"SELECT 1 FROM attendants WHERE username = %s AND password = %s;",
        params=(username, hashed),
        fetch=True
    )
    return bool(result)