from flask import Flask
from routes.home import home_blueprint
from routes.kafiil import kafiil_blueprint
from routes.khamsat import khamsat_blueprint
from routes.mostaql import mostaql_blueprint
from routes.notifications import notification_blueprint
from routes.search_khamsat import searchKhamsat_blueprint
from routes.update_info import updateInfo_blueprint



app = Flask(__name__)

app.register_blueprint(home_blueprint, url_prefix="/home")
app.register_blueprint(kafiil_blueprint, url_prefix="/kafiil")
app.register_blueprint(khamsat_blueprint, url_prefix="/khamsat")
app.register_blueprint(mostaql_blueprint, url_prefix="/mostaql")
app.register_blueprint(notification_blueprint, url_prefix="/notification")
app.register_blueprint(searchKhamsat_blueprint, url_prefix="/searchKhamsat")
app.register_blueprint(updateInfo_blueprint, url_prefix="/updateInfo")



@app.route('/')
def index():
    return "<h1>Welcome to our API!</h1>"

if __name__ == "__main__":
    app.run(threaded=True, debug=True)
