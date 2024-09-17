from environment.configuration import conf
import sqlite3

def init_database():
    if conf.database.zero_totp_admin_uri:
        if not conf.database.zero_totp_admin_uri.startswith("sqlite:///"):
            print("Only sqlite databases are supported. Use sqlite:/// to specify the database URI.")
            exit(1)
        uri = conf.database.zero_totp_admin_uri.replace("sqlite:///", "")
        try:
            print(f"Initializing database: {uri}")
            sqlite3.connect(uri)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            exit(1)
    else:
        print("Database URI not found. Configure zero_totp_admin_uri.")
        exit(1)


if __name__ == "__main__":
    init_database()