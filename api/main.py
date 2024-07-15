import connexion
from flask_cors import CORS
from environment.configuration import conf
from database.db import db
from zero_totp_db_model.model_init import init_db
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from connexion.middleware import MiddlewarePosition
from environment.configuration import logging
from datetime import datetime
from flask import request, redirect, make_response


def create_app():
    app_instance = connexion.FlaskApp(__name__, specification_dir="./routes/")
    #app_instance.add_middleware(
    #CORSMiddleware,
    #position=MiddlewarePosition.BEFORE_ROUTING,
    #allow_credentials=True,
    #allow_methods=["*"],
    #allow_headers=["*"]
    #)
    app_instance.add_api("swagger.yml")

    app = app_instance.app

    app.config["SQLALCHEMY_DATABASE_URI"] = conf.database.zero_totp_db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    

    
    db.init_app(app)
    init_db(db)    

    return app_instance, app
app, flask = create_app()




@flask.errorhandler(404)
def not_found(error):
    logging.warning(f"❌  404 error at {datetime.now()} {request.remote_addr} {request.url}")
    return {"message": "Not found"}, 404
            




if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=conf.api.port, reload=True)
   