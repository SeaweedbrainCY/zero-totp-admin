import os
import logging
import yaml 
from .env_requirements_check import test_conf


class EnvironmentConfig:
    required_keys = ["frontend_domain", "config_version", "frontend_URI"]
    def __init__(self, data) -> None:
        for key in self.required_keys:
            if key not in data:
                logging.error(f"[FATAL] Load config fail. Was expecting the key environment.{key}")
                exit(1)
        self.config_version = data["config_version"]
        self.frontend_domain = data["frontend_domain"]
        self.frontend_URI = data["frontend_URI"]
        self.config_version = data["config_version"]
        if data["type"] == "local":
            self.type = "local"
            logging.basicConfig(
                format='%(asctime)s %(levelname)-8s %(message)s',
                level=logging.DEBUG,
                datefmt='%d-%m-%Y %H:%M:%S')
            logging.debug("Environment set to development")
        elif data["type"] == "development":
            self.type = "development"
            logging.basicConfig(
                format='%(asctime)s %(levelname)-8s %(message)s',
                level=logging.INFO,
                datefmt='%d-%m-%Y %H:%M:%S')
            logging.info("Environment set to development")
        else:
            self.type = "production"
            logging.basicConfig(
                filename="/var/log/api/api.log",
                filemode='a',
                format='%(asctime)s %(levelname)-8s %(message)s',
                level=logging.INFO,
                datefmt='%d-%m-%Y %H:%M:%S')
        
class APIConfig:
    required_keys = [ "jwt_secret"]

    def __init__(self, data):
        for key in self.required_keys:
            if key not in data:
                logging.error(f"[FATAL] Load config fail. Was expecting the key api.{key}")
                exit(1)
        for key in self.option_config:
            if key not in data:
                logging.warning(f"api.{key} is not set. Ignoring it ...")
        if "port" not in data:
            logging.warning(f"api.'port' is not set. Using default value: 8080")
            data["port"] = 8080
        
        try:
            self.port = int(data["port"]) 
        except:
            logging.warning("api.port is not valid. Ignoring it. Setting default value: 8080")
            self.port = 8080
        
        self.jwt_secret = data["jwt_secret"]          

class DatabaseConfig:
    required_keys = ["zero_totp_db_uri", "zero_totp_admin_uri"]
    def __init__(self, data):
        for key in self.required_keys:
            if key not in data:
                logging.error(f"[FATAL] Load config fail. Was expecting the key database.{key}")
                exit(1)
        self.zero_totp_db_uri = data["zero_totp_db_uri"] 
        self.zero_totp_admin_uri = data["zero_totp_admin_uri"] 
        
class EnvironmentConfig:
    required_keys = ["type"]
    def __init__(self, data):
        for key in self.required_keys:
            if key not in data:
                logging.error(f"[FATAL] Load config fail. Was expecting the key environment.{key}")
                exit(1)
        self.type = data["type"] 
        self.config_version = data.get("config_version", "1.0.0")

class Config:
    required_keys = ["api", "database"]
    def __init__(self, data):
        for key in self.required_keys:
            if key not in data:
                exit(1)
        self.environment = EnvironmentConfig(data["environment"] if data["environment"] != None else {})
        self.api = APIConfig(data["api"] if data["api"] != None else [], self.environment.config_version)
        self.database = DatabaseConfig(data["database"] if data["database"] != None else [])




try:
    with open("./config/config.yml") as config_yml:
        try:
            raw_conf = yaml.safe_load(config_yml)
            conf = Config(raw_conf)
        
        except yaml.YAMLError as exc:
            raise Exception(exc)
except:
    logging.error("[FATAL] Load config fail. Could not open config file. Mount the config file to /api/config/config.yml")
    exit(1)


test_conf(conf) 