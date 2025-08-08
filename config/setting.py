import yaml

class Settings:
    def __init__(self, path: str = "config/config.yaml"):
        self.path = path
        with open(self.path, "r") as file:
            self.cfg = yaml.safe_load(file)
            
            #Database settings
            self.database_host = self.cfg["database_info"]["host"]
            self.public_port = self.cfg["database_info"]["public_port"]
            self.database = self.cfg["database_info"]["database"]
            self.user = self.cfg["database_info"]["user"]
            self.password = self.cfg["database_info"]["password"]
            
            #Parking slots settings
            self.total_slots = self.cfg["parking_slot"]["total_slots"]
            self.hourly_rates = self.cfg["parking_slot"]["hourly_rates"]
            
    def save(self) -> None:
        with open(self.path, "w") as file:
            yaml.safe_dump(self.cfg, file, sort_keys=False)
        

settings = Settings()