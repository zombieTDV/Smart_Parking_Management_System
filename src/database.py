from pyclbr import Class
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
        self.pk_map = {
            "parking_service": ["ID_user", "ID_parking_slot"],
            # Bạn có thể thêm bảng khác ở đây nếu cần
        }

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


#bảng dịch theo dõi dịch vụ để xe " ID_user | check_in (yes/no) | check_out (yes/no) | ID_parking_slot | parking_time(tính theo giây) | Pay? (yes/no)"
def validate_pay(value):
    if not isinstance(value, bool):
        raise ValueError(f"Trường 'Pay' chỉ nhận kiểu bool True/False, nhận: {value}")

def validate_yes_no(value, field_name):
    if value not in ("yes", "no"):
        raise ValueError(f"Trường '{field_name}' chỉ nhận giá trị 'yes' hoặc 'no', nhận: {value}")

class ParkingService(Table):
    def __init__(self, db: Database):
        super().__init__("parking_service", db)
        schema = """ """
        self.create(schema)

    def insert(self, columns: list, values: tuple):
        yes_no_fields = ["check_in", "check_out", "Pay"]
        values = list(values)
        for field in yes_no_fields:
            if field in columns:
                idx = columns.index(field)
                # Convert boolean to "yes"/"no" for Pay field
                if field == "Pay" and isinstance(values[idx], bool):
                    values[idx] = "yes" if values[idx] else "no"
                validate_yes_no(values[idx], field)
        super().insert(columns, tuple(values))

    def update(self, ID_user: int, ID_parking_slot: int, data: dict):
        yes_no_fields = ["check_in", "check_out", "Pay"]
        for field in yes_no_fields:
            if field in data:
                validate_yes_no(data[field], field)

        set_clause = ", ".join(f"`{k}` = %s" for k in data.keys())
        values = tuple(data.values()) + (ID_user, ID_parking_slot)
        sql = f"""
        UPDATE `{self.name}` 
        SET {set_clause} 
        WHERE ID_user = %s AND ID_parking_slot = %s;
        """
        self.db.execute(sql, params=values, commit=True)
        print(f"Record with ID_user={ID_user} and ID_parking_slot={ID_parking_slot} updated.")

    def delete(self, ID_user: int, ID_parking_slot: int):
        sql = f"DELETE FROM `{self.name}` WHERE ID_user = %s AND ID_parking_slot = %s;"
        self.db.execute(sql, params=(ID_user, ID_parking_slot), commit=True)
        print(f"Record with ID_user={ID_user} and ID_parking_slot={ID_parking_slot} deleted.")

parking_service = ParkingService(db=Database())
parking_slot = Table("parking_slot", db=Database())
account = Table("account", db=Database())

db = Database()

# parking_slot.insert(["available"], (True,))

# rows = parking_slot.select_all()

# count = parking_slot.count()

# parking_slot.delete_all()
