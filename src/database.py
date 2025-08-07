import mysql.connector

from src.utils.helpers import settings

class Database_management():
    def __init__(self) -> None:
         pass
    
    def connect(self):
        print("Attempting to connect to MySQL...")
        conn = mysql.connector.connect(
            host = settings.database_host,
            port= settings.public_port,
            user = "root",
            password = "XKahsWDvEBIvWvijLrQVcSxgPMSmgBAh",
            database = settings.database
        )
        print("Connected successfully!")
        return conn

    def n_rows(self, table_name: str) -> int:
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            sql = f"SELECT COUNT(*) AS row_count FROM {table_name};"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                return int(result[0]) # type: ignore
            return 0
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 0
        except Exception as err:
            print(f"Unexpected error: {err}")
            return 0
        finally:
            cursor.close()
            conn.close()
        
        
    def clear_table(self, table_name: str) -> None:
        conn = self.connect()
        cursor = conn.cursor()
        try:
            sql = f"TRUNCATE TABLE {table_name};"
            cursor.execute(sql)
            conn.commit()
            print(f"All data from {table_name} cleared successfully.")
            
        except mysql.connector.Error as err:
                print(f"Error: {err}")
        except Exception as err:
                print(f"Unexpected error: {err}")
        finally:
            cursor.close()
            conn.close()
        


class Parking_slot_table():
    def __init__(self, database_management: Database_management) -> None:
         self.database_management = database_management
     
    def init_parking_slots(self, size: int) -> None:
        conn = self.database_management.connect()
        cursor = conn.cursor()
        try:
            for _ in range(size):
                
                    sql = "INSERT INTO parking_slot (available) VALUES (%s)"
                    val = (1,)
                    cursor.execute(sql, val)
                    conn.commit()
                    print(f"{cursor.rowcount} record inserted successfully.")
                    
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        except Exception as err:
            print(f"Unexpected error: {err}")
                
        finally:
            cursor.close()
            conn.close()


database_management = Database_management()
parking_slot_table = Parking_slot_table(database_management) 