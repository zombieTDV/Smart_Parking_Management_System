import yaml

class Settings:
    def __init__(self, path: str = "config/config.yaml"):
        with open(path, "r") as file:
            cfg = yaml.safe_load(file)
            
            self.database_host = cfg["database_info"]["host"]
            self.public_port = cfg["database_info"]["public_port"]
            self.database = cfg["database_info"]["database"]
            


settings = Settings()