from src.database import database_management



if __name__ == "__main__":
    # parking_slot.init_parking_slots(size = 10)
    # database_management.clear_table("parking_slot")

    print(f"Number of rows: {database_management.n_rows("parking_slot")}") 