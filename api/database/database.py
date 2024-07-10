from environment.environment import conf
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from zero_totp_db_model.model_init import init_db


engine = create_engine(
    conf.database.zero_totp_db_uri
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
db = SQLAl
init_db(db)

