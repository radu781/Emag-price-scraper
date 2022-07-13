from configparser import ConfigParser

ini_file = ConfigParser()
ini_file.read("config/data.ini")
_from = ini_file.get("email", "address")
_password = ini_file.get("email", "password")
