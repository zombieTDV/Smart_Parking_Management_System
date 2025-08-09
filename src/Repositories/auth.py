
# src/Repositories/auth.py

import os
import json
import hashlib

# File JSON để lưu trữ dữ liệu (tự tạo khi chạy lần đầu)
DATA_FILE = os.path.join(os.path.dirname(__file__), 'auth_data.json')


def _load_data():
    """
    Đọc dữ liệu từ DATA_FILE. Nếu chưa tồn tại, khởi tạo cấu trúc rỗng.
    """
    if not os.path.exists(DATA_FILE):
        initial = {"owners": [], "attendants": []}
        _save_data(initial)
        return initial

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_data(data: dict):
    """
    Ghi dict data xuống DATA_FILE.
    """
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def _hash_password(password: str) -> str:
    """
    Trả về chuỗi hex của SHA-256 băm mật khẩu.
    """
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def owner_exists(username: str) -> bool:
    """
    Kiểm tra xem chủ xe với username đã tồn tại chưa.
    """
    data = _load_data()
    return any(u['username'] == username for u in data['owners'])


def attendant_exists(username: str) -> bool:
    """
    Kiểm tra xem nhân viên giữ xe với username đã tồn tại chưa.
    """
    data = _load_data()
    return any(u['username'] == username for u in data['attendants'])


def register_owner(username: str, password: str):
    """
    Đăng ký chủ xe mới.
    """
    data = _load_data()
    data['owners'].append({
        "username": username,
        "password": _hash_password(password)
    })
    _save_data(data)


def register_attendant(username: str, password: str):
    """
    Đăng ký nhân viên giữ xe mới.
    """
    data = _load_data()
    data['attendants'].append({
        "username": username,
        "password": _hash_password(password)
    })
    _save_data(data)


def validate_owner(username: str, password: str) -> bool:
    """
    Xác thực chủ xe.
    """
    data = _load_data()
    hashed = _hash_password(password)
    return any(u['username'] == username and u['password'] == hashed
               for u in data['owners'])


def validate_attendant(username: str, password: str) -> bool:
    """
    Xác thực nhân viên giữ xe.
    """
    data = _load_data()
    hashed = _hash_password(password)
    return any(u['username'] == username and u['password'] == hashed
               for u in data['attendants'])