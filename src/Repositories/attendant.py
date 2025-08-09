
# src/repositories/attendant.py
from database import SessionLocal
from src.models.parking_slot import ParkingSlot
from src.models.transaction import Transaction

class AttendantRepo:
    def __init__(self):
        self.db = SessionLocal()

    def get_free_slot(self):
        return (
            self.db.query(ParkingSlot)
            .filter_by(is_occupied=False)
            .order_by(ParkingSlot.id)
            .first()
        )

    def occupy_slot(self, slot):
        slot.is_occupied = True
        self.db.commit()
        return slot.id

    def release_slot(self, slot_id: int):
        slot = self.db.query(ParkingSlot).get(slot_id)
        if slot:
            slot.is_occupied = False
            self.db.commit()
            return True
        return False

    def create_transaction(self, plate: str, slot_id: int):
        tx = Transaction(plate=plate, slot_id=slot_id)
        self.db.add(tx)
        self.db.commit()
        self.db.refresh(tx)
        return tx

    def close_transaction(self, tx):
        self.db.commit()