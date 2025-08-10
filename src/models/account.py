from src.database import Table, db
#Them moi class user        

class AccountCentral:
    def __init__(self):
        self.table = Table("account", db)
        self.table.create(
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "username VARCHAR(50) NOT NULL, "
            "role VARCHAR(20) NOT NULL, "
            "password VARCHAR(100) NOT NULL"
        )
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)
        self.table.insert(["id", "username", "role", "password"], (account.id, account.username, account.role, account.password))
        
    def get_accounts(self):
        return self.table.select_all()
    
    def view_all_accounts(self) -> None:
        """
        Hiển thị tất cả tài khoản đã đăng ký.
        """
        select = self.table.select_all()
        print("=== Accounts ===")
        for i in range(self.table.count()):
            account = select[i] # type: ignore
            print(f"ID: {account[0]}, Username: {account[1]}, Role: {account[2]}, Password: {account[3]}") # type: ignore
        
        print("================")
        
    def delete_account(self, account_id: int) -> None:
        """
        Xóa tài khoản theo ID.
        """
        self.table.delete(record_name='id', record_id=account_id)
        print(f"Account with ID {account_id} has been deleted.")
        
    def delete_all_accounts(self) -> None:
        """
        Xóa tất cả tài khoản.
        """
        self.table.delete_all()
        
    def find_record_with_value(self, column: str, value):
        """
        Tìm bản ghi theo giá trị của cột.
        """
        return self.table.find_record_with_value(column, value)

class Account:
    def __init__(self, username=None, role=None, password=None):
        self.username = username
        self.role = role
        self.password = password

    def __repr__(self):
        return f"User(username={self.username})"
    
    def __str__(self):
        return f"User(username={self.username}, role={self.role})"
    
    
    def create_account(self):
        self.username = input("Nhập tên đăng nhập: ")
        self.role = input("Nhập vai trò (admin/attendant/owner): ")
        self.password = input("Nhập mật khẩu: ")
        
        if not self.username or not self.role or not self.password:
            print("❌ Tên đăng nhập, vai trò và mật khẩu không được để trống.")
            return
        else:
            print("✅ Tạo tài khoản thành công.")
        

    def save_to_db(self):
        columns = ["username", "role", "password"]
        values = (self.username, self.role, self.password)
        accounts_central.table.insert(columns, values)

    def display_account(self):
        print("\n--- Thông tin người dùng ---")
        print("User details:")
        print(f"Username: {self.username}, role : {self.role}, password: {self.password}")
        print("------------------------------") 
        
    
        
        
accounts_central = AccountCentral()