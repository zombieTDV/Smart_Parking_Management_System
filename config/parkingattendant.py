import mysql.connector
from datetime import datetime

class ParkingAttendant:
    def __init__(self, host="localhost", user="root", password="", database="parking_db", rate_per_hour=5):
        self.db_config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }
        self.rate_per_hour = rate_per_hour

    def connect(self):
        return mysql.connector.connect(**self.db_config)

    def view_available_slots(self):
        """Hiển thị các chỗ trống"""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT slot_id FROM slots WHERE available = 1")
        available = [row[0] for row in cur.fetchall()]
        conn.close()
        print("Available Slots:", available)
        return available

    def check_in_vehicle(self, plate_number):
        """Nhận xe vào"""
        available_slots = self.view_available_slots()
        if not available_slots:
            print("No available slots right now.")
            return

        assigned_slot = available_slots[0]
        check_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = self.connect()
        cur = conn.cursor()
        cur.execute("UPDATE slots SET available = 0 WHERE slot_id = %s", (assigned_slot,))
        cur.execute(
            "INSERT INTO vehicles (plate_number, slot_id, check_in) VALUES (%s, %s, %s)",
            (plate_number, assigned_slot, check_in_time)
        )
        conn.commit()
        conn.close()
        print(f"Vehicle {plate_number} checked in at slot {assigned_slot}.")

    def check_out_vehicle(self, plate_number):
        """Trả xe, tính phí, lưu giao dịch"""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT slot_id, check_in FROM vehicles WHERE plate_number = %s",
            (plate_number,)
        )
        row = cur.fetchone()
        if not row:
            conn.close()
            print("Vehicle not found.")
            return

        slot, check_in_str = row
        check_in_time = datetime.strptime(check_in_str, "%Y-%m-%d %H:%M:%S")
        duration = datetime.now() - check_in_time
        hours_parked = int(duration.total_seconds() // 3600)
        if duration.total_seconds() % 3600 > 0:
            hours_parked += 1

        fee = hours_parked * self.rate_per_hour
        check_out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Giải phóng chỗ, xóa xe, lưu giao dịch
        cur.execute("UPDATE slots SET available = 1 WHERE slot_id = %s", (slot,))
        cur.execute("DELETE FROM vehicles WHERE plate_number = %s", (plate_number,))
        cur.execute(
            "INSERT INTO transactions (plate_number, slot_id, check_in, check_out, fee) VALUES (%s, %s, %s, %s, %s)",
            (plate_number, slot, check_in_str, check_out_time, fee)
        )
        conn.commit()
        conn.close()

        print(f"Vehicle {plate_number} checked out from slot {slot}.")
        print(f"Hours parked: {hours_parked}, Fee: ${fee}")

    def view_transactions(self):
        """Xem toàn bộ lịch sử giao dịch"""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("SELECT plate_number, slot_id, check_in, check_out, fee FROM transactions")
        transactions = cur.fetchall()
        conn.close()

        if not transactions:
            print("No transactions found.")
            return

        print("\nTransaction History:")
        for plate, slot, check_in, check_out, fee in transactions:
            print(f"Plate: {plate} | Slot: {slot} | In: {check_in} | Out: {check_out} | Fee: ${fee}")

