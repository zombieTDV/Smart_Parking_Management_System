from src.database import Table, db
#Them moi class user        

class Acount_central:
    def __init__(self):
        self.table = Table("acount", db)
        self.table.create(
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "username VARCHAR(50) NOT NULL, "
            "role VARCHAR(20) NOT NULL, "
            "password VARCHAR(100) NOT NULL"
        )
        self.acounts = []

    def add_acount(self, acount):
        self.acounts.append(acount)
        self.table.insert(["id", "username", "role", "password"], (acount.id, acount.username, acount.role, acount.password))
        
    def get_acounts(self):
        return self.table.select_all()
    
    def view_all_accounts(self) -> None:
        """
        Hiển thị tất cả tài khoản đã đăng ký.
        """
        select = self.table.select_all()
        print("=== Acounts ===")
        for i in range(self.table.count()):
            acount = select[i] # type: ignore
            print(f"ID: {acount[0]}, Username: {acount[1]}, Role: {acount[2]}, Password: {acount[3]}") # type: ignore
        
        print("================")
        
    def delete_acount(self, acount_id: int) -> None:
        """
        Xóa tài khoản theo ID.
        """
        self.table.delete(record_name='id', record_id=acount_id)
        print(f"Acount with ID {acount_id} has been deleted.")
        
    def delete_all_acounts(self) -> None:
        """
        Xóa tất cả tài khoản.
        """
        self.table.delete_all()

class Acount:
    def __init__(self, username, role, password):
        self.username = username
        self.role = role
        self.password = password

    def __repr__(self):
        return f"User(username={self.username})"
    
    def __str__(self):
        return f"User(username={self.username}, role={self.role})"
    
    
    def create_acount(self):
        self.username = input("Nhập tên đăng nhập: ")
        self.role = input("Nhập vai trò (admin/owner/user): ")
        self.password = input("Nhập mật khẩu: ")
        
        if not self.username or not self.role or not self.password:
            print("❌ Tên đăng nhập, vai trò và mật khẩu không được để trống.")
            return
        else:
            print("✅ Tạo tài khoản thành công.")
        

    def save_to_db(self):
        columns = ["username", "role", "password"]
        values = (self.username, self.role, self.password)
        acounts_central.table.insert(columns, values)

    def display_acount(self):
        print("\n--- Thông tin người dùng ---")
        print("User details:")
        print(f"Username: {self.username}, role : {self.role}, password: {self.password}")
        print("------------------------------") 
        
    
        
        
acounts_central = Acount_central()