import connexion
from flask_cors import CORS
from environment.configuration import conf
from database.db import db
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from connexion.middleware import MiddlewarePosition
from environment.configuration import logging
from datetime import datetime
from flask import request, redirect, make_response


def create_app():
    app_instance = connexion.FlaskApp(__name__, specification_dir="./routes/")
    app_instance.add_middleware(
    CORSMiddleware,
    position=MiddlewarePosition.BEFORE_ROUTING,
    allow_origins=conf.environment.frontend_URI,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    app_instance.add_api("swagger.yml")

    app = app_instance.app

    app.config["SQLALCHEMY_DATABASE_URI"] = conf.database.database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.secret_key = conf.api.flask_secret_key
    

    
    db.init_app(app)
    

    return app_instance, app
app, flask = create_app()
migrate = Migrate(flask, db)
scheduler = APScheduler()
scheduler.init_app(flask)
scheduler.start()



@flask.errorhandler(404)
def not_found(error):
    logging.warning(f"❌  404 error at {datetime.now()} {request.remote_addr} {request.url}")
    return make_response(redirect(conf.environment.frontend_URI[0] + "/404",  code=302))
            




if __name__ == "__main__":
   uvicorn.run("app:app", host="0.0.0.0", port=conf.api.port, reload=True)
   