import mysql.connector
from config.setting import settings


def handle_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        except Exception as err:
            print(f"Unexpected error: {err}")
    return wrapper


class Database:
    def __init__(self):
        pass

    def connect(self):
        conn = mysql.connector.connect(
            host=settings.database_host,
            port=settings.public_port,
            user=settings.user,
            password=settings.password,
            database=settings.database
        )
        return conn

    @handle_errors
    def execute(self, sql: str, params = None, fetch: bool = False, commit: bool = False):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params or ())
            if commit:
                conn.commit()
            if fetch:
                return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()


class Table:
    def __init__(self, name: str, db: Database):
        self.name = name
        self.db = db

    def create(self, schema: str):
        sql = f"CREATE TABLE IF NOT EXISTS `{self.name}` ({schema});"
        self.db.execute(sql, commit=True)
        print(f"Table `{self.name}` created or exists.")

    def select_all(self):
        sql = f"SELECT * FROM `{self.name}`;"
        return self.db.execute(sql, fetch=True)

    def delete_all(self):
        sql = f"TRUNCATE TABLE `{self.name}`;"
        self.db.execute(sql, commit=True)
        print(f"All records from `{self.name}` deleted.")

    def count(self):
        sql = f"SELECT COUNT(*) FROM `{self.name}`;"
        result = self.db.execute(sql, fetch=True)
        return int(result[0][0]) if result else 0 # type: ignore

    def insert(self, columns: list, values: tuple):
        cols = ", ".join(f"`{c}`" for c in columns)
        placeholder = ", ".join("%s" for _ in values)
        sql = f"INSERT INTO `{self.name}` ({cols}) VALUES ({placeholder});"
        self.db.execute(sql, params=values, commit=True)
        print(f"1 record inserted into `{self.name}`.")
### sửa lại
    def update(self, record_id: int, data: dict):
        set_clause = ", ".join(f"`{k}` = %s" for k in data.keys())
        values = tuple(data.values()) + (record_id,)
        sql = f"UPDATE `{self.name}` SET {set_clause} WHERE `id` = %s;"
        self.db.execute(sql, params=values, commit=True)
        print(f"Record with ID {record_id} updated in `{self.name}`.")
        
    def delete(self, record_name: str, record_id: int):
        sql = f"DELETE FROM `{self.name}` WHERE `{record_name}` = %s;"
        self.db.execute(sql, params=(record_id,), commit=True)
        print(f"Record with ID {record_id} deleted from `{self.name}`.")
        
    def delete_table(self):
        sql = f"DROP TABLE IF EXISTS `{self.name}`;"
        self.db.execute(sql, commit=True)
        print(f"Table `{self.name}` deleted.")

    def delete_last_n(self, n_rows: int):
        """
        Delete the last n_rows from the table, ordered by id descending.
        """
        sql = f"SELECT `id` FROM `{self.name}` ORDER BY `id` DESC LIMIT %s;"
        ids = self.db.execute(sql, params=(n_rows,), fetch=True)
        if ids:
            for row in ids:
                self.delete(row[0]) # type: ignore
        else:
            print("No rows to delete.")


#Them moi class user        
class User:
    def __init__(self, id, username, role, password):
        self.id = id
        self.username = username
        self.role = role
        self.password = password

    def __repr__(self):
        return f"User(username={self.username})"
    
    def __str__(self):
        return f"User(username={self.username}, role={self.role})"
    
    def input_user(self):
        self.username = input("Nhập tên đăng nhập: ")
        self.role = input("Nhập vai trò (admin/owner/user): ")
        self.password = input("Nhập mật khẩu: ")

    def save_to_db(self, table):
        columns = ["id", "username", "role", "password"]
        values = (self.id, self.username, self.role, self.password)
        table.insert(columns, values)

    def display_user(self):
        print("\n--- Thông tin người dùng ---")
        print("User details:")
        print(f"ID: {self.id}")
        print(f"Username: {self.username}, role : {self.role}, password: {self.password}")
        print("------------------------------") 

db = Database()

parking_slot = Table("parking_slot", db)

user_table = Table("user", db)


new_user = User(1, "", "", "")
new_user.input_user()
new_user.save_to_db(user_table)
new_user.display_user()


# parking_slot.insert(["available"], (True,))

# rows = parking_slot.select_all()

# count = parking_slot.count()

# parking_slot.delete_all()
