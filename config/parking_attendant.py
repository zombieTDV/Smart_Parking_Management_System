import json
from datetime import datetime, timedelta


class ParkingAttendant:
    def __init__(self, data_file="parking_data.json", rate_per_hour=5):
        self.data_file = data_file
        self.rate_per_hour = rate_per_hour
        self.slots = {}
        self.vehicles = {}
        self.load_data()

    def load_data(self):
        """Load slot and vehicle data from file."""
        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.slots = data.get("slots", {})
                self.vehicles = data.get("vehicles", {})
        except FileNotFoundError:
            self.slots = {f"S{i+1}": {"available": True} for i in range(10)}
            self.vehicles = {}
            self.save_data()

    def save_data(self):
        """Save slot and vehicle data to file."""
        with open(self.data_file, "w") as f:
            json.dump({"slots": self.slots, "vehicles": self.vehicles}, f, indent=4)

    def check_in_vehicle(self, plate_number):
        """Assigns an available slot to the vehicle."""
        available_slots = [slot for slot, info in self.slots.items() if info["available"]]
        if not available_slots:
            print("No available slots right now.")
            return

        assigned_slot = available_slots[0]
        self.slots[assigned_slot]["available"] = False
        self.vehicles[plate_number] = {
            "slot": assigned_slot,
            "check_in": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_data()
        print(f"Vehicle {plate_number} checked in at slot {assigned_slot}.")

    def check_out_vehicle(self, plate_number):
        """Releases slot, calculates fee, and removes vehicle record."""
        vehicle_info = self.vehicles.get(plate_number)
        if not vehicle_info:
            print("Vehicle not found.")
            return

        check_in_time = datetime.strptime(vehicle_info["check_in"], "%Y-%m-%d %H:%M:%S")
        duration = datetime.now() - check_in_time
        hours_parked = int(duration.total_seconds() // 3600)
        if duration.total_seconds() % 3600 > 0:
            hours_parked += 1  # round up to next hour

        fee = hours_parked * self.rate_per_hour
        slot = vehicle_info["slot"]

        # Free the slot and remove vehicle record
        self.slots[slot]["available"] = True
        del self.vehicles[plate_number]
        self.save_data()

        print(f"Vehicle {plate_number} checked out from slot {slot}.")
        print(f"Hours parked: {hours_parked}, Fee: ${fee}")

    def view_available_slots(self):
        """Displays all available parking slots."""
        available = [slot for slot, info in self.slots.items() if info["available"]]
        print("Available Slots:", available)


# # Example usage
# if __name__ == "__main__":
#     attendant = ParkingAttendant(rate_per_hour=5)

#     while True:
#         print("\n--- Parking Attendant Menu ---")
#         print("1. View available slots")
#         print("2. Check-in vehicle")
#         print("3. Check-out vehicle")
#         print("4. Exit")
#         choice = input("Enter choice: ")

#         if choice == "1":
#             attendant.view_available_slots()
#         elif choice == "2":
#             plate = input("Enter vehicle plate number: ")
#             attendant.check_in_vehicle(plate)
#         elif choice == "3":
#             plate = input("Enter vehicle plate number: ")
#             attendant.check_out_vehicle(plate)
#         elif choice == "4":
#             break
#         else:
#             print("Invalid choice.")
