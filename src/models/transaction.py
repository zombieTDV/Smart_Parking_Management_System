from datetime import datetime, timedelta
from src.database import Table, db
from src.models.parking_slot import parking_slot

def seconds_to_hms(seconds: int) -> str:
    """Convert seconds -> H:MM:SS string."""
    if seconds is None:
        return "0:00:00"
    td = timedelta(seconds=int(seconds))
    hours = td.seconds // 3600 + td.days * 24
    minutes = (td.seconds % 3600) // 60
    secs = td.seconds % 60
    return f"{hours}:{minutes:02d}:{secs:02d}"

class TransactionService:
    def __init__(self):
        self.table = Table("transaction_service", db)
        # Add timestamp columns. check_in_time uses CURRENT_TIMESTAMP by default.
        self.table.create(
            "ID INT NOT NULL, "
            "ID_parking_slot INT NOT NULL, "
            "username VARCHAR(50) NOT NULL, "
            "check_in BOOL NOT NULL DEFAULT 0, "
            "check_out BOOL NOT NULL DEFAULT 0, "
            "pay BOOL NOT NULL DEFAULT 0, "
            "check_in_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, "
            "check_out_time DATETIME NULL DEFAULT NULL"
        )
        self.records = []

    def add_record(self, record):
        record.save_to_db()
        self.records.append(record)


    def get_records_with_duration(self):
        """
        Return rows with an additional 'duration_seconds' column computed as:
        - Only calculate if check_in = TRUE
        - if check_out_time is NULL -> TIMESTAMPDIFF(SECOND, check_in_time, NOW())
        - else TIMESTAMPDIFF(SECOND, check_in_time, check_out_time)
        """
        tbl = getattr(self.table, "name", "transaction_service")
        tb_db = getattr(self.table, "db", db)
        sql = f"""
        SELECT
            ID,
            ID_parking_slot,
            username,
            check_in,
            check_out,
            pay,
            check_in_time,
            check_out_time,
            CASE 
                WHEN check_in = 1 THEN 
                    IFNULL(
                        TIMESTAMPDIFF(SECOND, check_in_time, check_out_time),
                        TIMESTAMPDIFF(SECOND, check_in_time, NOW())
                    ) + 7*3600
                ELSE 0
            END AS duration_seconds
        FROM `{tbl}`;
        """
        rows = tb_db.execute(sql, fetch=True)
        return rows


    def get_duration_seconds(self, ID: int, ID_parking_slot: int) -> int:
        """
        Return the current duration (in seconds) for a given user/slot.
        Only counts if check_in=True. Adjusts by +7 hours for timezone.
        """
        tbl = getattr(self.table, "name", "transaction_service")
        tb_db = getattr(self.table, "db", db)
        sql = f"""
        SELECT 
            IF(check_in = 1,
                IFNULL(
                    TIMESTAMPDIFF(SECOND, check_in_time, check_out_time),
                    TIMESTAMPDIFF(SECOND, check_in_time, NOW())
                ),  -- adjust for UTC+7
                0
            ) AS duration_sec
        FROM `{tbl}`
        WHERE ID = %s AND ID_parking_slot = %s
        LIMIT 1;
        """
        row = tb_db.execute(sql, params=(ID, ID_parking_slot), fetch=True)
        if row and len(row) > 0:
            return int(row[0][0]) if row[0][0] is not None else 0 # type: ignore
        return 0

    def view_all_records(self) -> None:
        """Print all records with a nicely formatted duration."""
        try:
            rows = self.get_records_with_duration()
            print("=== Transaction Records ===")
            for r in rows: # type: ignore
                # r structure: (ID, ID_parking_slot, check_in, check_out, pay, check_in_time, check_out_time, duration_seconds)
                dur = r[8] # type: ignore
                print(
                    f"ID: {r[0]}, ID_parking_slot: {r[1]}, UserName: {r[2]} "  # type: ignore
                    f"check_in: {bool(r[3])}, check_out: {bool(r[4])}, pay: {bool(r[5])}, " # type: ignore
                    f"duration: {seconds_to_hms(dur)}" # type: ignore
                )
            print("===========================")
        except AttributeError:
            # If your db wrapper does not have fetch_all, fall back to select_all and compute in Python
            select = self.table.select_all()
            print("=== Transaction Records ===")
            for i in range(self.table.count()):
                r = select[i]  # type: ignore
                # r may be (ID, ID_parking_slot, check_in, check_out, pay, check_in_time, check_out_time)
                # Parse datetime if needed, otherwise assume r[5]/r[6] are datetime objects.
                ci = r[5] # type: ignore
                co = r[6] if len(r) > 6 else None # type: ignore
                if isinstance(ci, str):
                    ci = datetime.fromisoformat(ci)
                if isinstance(co, str):
                    co = datetime.fromisoformat(co)
                if co is None:
                    dur_seconds = int((datetime.now() - ci).total_seconds()) # type: ignore
                else:
                    dur_seconds = int((co - ci).total_seconds()) # type: ignore
                print(
                    f"ID: {r[0]}, ID_parking_slot: {r[1]}, " # type: ignore
                    f"check_in: {bool(r[2])}, check_out: {bool(r[3])}, pay: {bool(r[4])}, " # type: ignore
                    f"duration: {seconds_to_hms(dur_seconds)}"
                )
            print("===========================")

    def update_record(self, ID: int, ID_parking_slot: int, data: dict):
        """
        When updating, if check_out=True is provided we also set check_out_time = NOW()
        so duration becomes fixed.
        """
        if "check_out" in data and data["check_out"]:
            # set check_out_time to now
            data["check_out_time"] = datetime.now()

        set_clause = ", ".join(f"`{k}` = %s" for k in data.keys())
        values = tuple(data.values()) + (ID, ID_parking_slot)

        tbl_name = getattr(self.table, "name", "transaction_service")
        tb_db = getattr(self.table, "db", db)

        sql = f"""
        UPDATE `{tbl_name}`
        SET {set_clause}
        WHERE ID = %s AND ID_parking_slot = %s;
        """
        tb_db.execute(sql, params=values, commit=True)
        print(f"Record with ID={ID} and ID_parking_slot={ID_parking_slot} updated.")

    def delete_record(self, ID: int, ID_parking_slot: int):
        tbl_name = getattr(self.table, "name", "transaction_service")
        tb_db = getattr(self.table, "db", db)
        sql = f"DELETE FROM `{tbl_name}` WHERE ID = %s AND ID_parking_slot = %s;"
        tb_db.execute(sql, params=(ID, ID_parking_slot), commit=True)
        print(f"Record with ID={ID} and ID_parking_slot={ID_parking_slot} deleted.")

    def delete_all_records(self) -> None:
        self.table.delete_all()
        
    def check_out_vehicle(self, user_id: int, slot_id: int) -> None:
        """
        Xử lý check-out cho xe ra khỏi bãi đỗ.
        """
        transaction_service.update_record(
            ID=user_id,
            ID_parking_slot=slot_id,
            data={"check_out": True}
        )
        transaction_service.update_record(
            ID=user_id,
            ID_parking_slot=slot_id,
            data={"pay": True}
        )
        transaction_service.get_duration_seconds(user_id, slot_id)
        print(f"✅ Xe đã được check-out từ chỗ đỗ ID {slot_id}.")
        parking_slot.release_slot(slot_id)
        
    def set_record_pay(self, user_id: int, slot_id: int, status: bool) -> None:
        """
        Cập nhật trạng thái của bản ghi giao dịch.
        """
        transaction_service.update_record(
            ID=user_id,
            ID_parking_slot=slot_id,
            data={"pay": status}
        )
    
    
    def find_user_by_username(self, username: str) -> int:
        """
        Tìm ID người dùng dựa trên tên đăng nhập.
        """
        user = self.table.find_record_with_value(column='username', value=username)
        if user:
            return user[0][3] # type: ignore
        print(f"❌ Không tìm thấy người dùng với tên đăng nhập: {username}")
        return -1
        
    def find_slot_by_username(self, username: str) -> int:
        """
        Tìm ID chỗ đỗ dựa trên tên đăng nhập người dùng.
        """
        user_id = self.find_user_by_username(username)
        if user_id == -1:
            return -1 
        slot = self.table.find_record_with_value(column='ID', value=user_id)
        if slot:
            return slot[0][1] # type: ignore
        print(f"❌ Không tìm thấy chỗ đỗ cho người dùng: {username}")
        return -1
    
    def get_payment_status(self, user_id: int):
        """
        Lấy trạng thái thanh toán của người dùng.
        """
        record = self.table.get_value(
            record_name='ID',
            record_id=user_id,
            column='pay')
        
        if record == 1:
            return "Đã thanh toán"
        elif record == 0:
            return "Chưa thanh toán"
        


class TransactionRecord:
    def __init__(self, ID: int, ID_parking_slot: int, username: str):
        self.ID = ID
        self.ID_parking_slot = ID_parking_slot
        self.username = username
        
        self.check_in = False
        self.check_out = False
        
        self.pay = False
        
        self.check_in_time = None
        self.check_out_time = None

    def check_in_user(self):
        self.check_in = True
        self.check_out = False
        self.pay = False
        self.check_in_time = datetime.now()
        self.check_out_time = None
        self.save_to_db()

    def check_out_user(self):
        self.check_out = True
        self.check_out_time = datetime.now()
        sql_update = """
        UPDATE transaction_service
        SET check_out = TRUE, check_out_time = %s
        WHERE ID = %s AND ID_parking_slot = %s
        AND check_in = TRUE AND check_out = FALSE
        """
        db.execute(sql_update, params=(self.check_out_time, self.ID, self.ID_parking_slot), commit=True)

        duration_sec = transaction_service.get_duration_seconds(self.ID, self.ID_parking_slot)
        print(f"✅ User {self.ID} đã check-out. Tổng thời gian: {seconds_to_hms(duration_sec)}")

    def save_to_db(self):
        columns = ["ID", "ID_parking_slot", "username", "check_in", "check_out", "pay", "check_in_time", "check_out_time"]
        values = (self.ID, self.ID_parking_slot, self.username, self.check_in, self.check_out, self.pay, self.check_in_time, self.check_out_time)
        transaction_service.table.insert(columns, values)
        
transaction_service = TransactionService()
