import sqlite3
from datetime import datetime

class ParkingAttendant:
    def __init__(self, db_name="parking_data.db", rate_per_hour=5):
        self.db_name = db_name
        self.rate_per_hour = rate_per_hour

    def connect(self):
        return sqlite3.connect(self.db_name)

    def view_available_slots(self):
      
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT slot_id FROM slots WHERE available = 1")
            available = [row[0] for row in cur.fetchall()]
        print("Available Slots:", available)
        return available

    def check_in_vehicle(self, plate_number):
        available_slots = self.view_available_slots()
        if not available_slots:
            print("No available slots right now.")
            return

        assigned_slot = available_slots[0]
        check_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE slots SET available = 0 WHERE slot_id = ?", (assigned_slot,))
            cur.execute(
                "INSERT INTO vehicles (plate_number, slot_id, check_in) VALUES (?, ?, ?)",
                (plate_number, assigned_slot, check_in_time)
            )
            conn.commit()
        print(f"Vehicle {plate_number} checked in at slot {assigned_slot}.")

    def check_out_vehicle(self, plate_number):
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT slot_id, check_in FROM vehicles WHERE plate_number = ?",
                (plate_number,)
            )
            row = cur.fetchone()
            if not row:
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

            cur.execute("UPDATE slots SET available = 1 WHERE slot_id = ?", (slot,))
            cur.execute("DELETE FROM vehicles WHERE plate_number = ?", (plate_number,))
            cur.execute(
                "INSERT INTO transactions (plate_number, slot_id, check_in, check_out, fee) VALUES (?, ?, ?, ?, ?)",
                (plate_number, slot, check_in_str, check_out_time, fee)
            )
            conn.commit()

        print(f"Vehicle {plate_number} checked out from slot {slot}.")
        print(f"Hours parked: {hours_parked}, Fee: ${fee}")

    def view_transactions(self):
        """Xem toàn bộ lịch sử giao dịch"""
        with self.connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT plate_number, slot_id, check_in, check_out, fee FROM transactions")
            transactions = cur.fetchall()

        if not transactions:
            print("No transactions found.")
            return

        print("\nTransaction History:")
        for plate, slot, check_in, check_out, fee in transactions:
            print(f"Plate: {plate} | Slot: {slot} | In: {check_in} | Out: {check_out} | Fee: ${fee}")


