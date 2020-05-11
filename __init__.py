from api.animal_api import animal_api
from api.center_api import center_api
from api.login_api import login_api
from api.species_api import species_api
from configuration import app

app.register_blueprint(center_api)
app.register_blueprint(species_api)
app.register_blueprint(animal_api)
app.register_blueprint(login_api)

if __name__ == "__main__":
    app.run()
