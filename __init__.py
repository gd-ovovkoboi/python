from settings import app
from controller.CenterController import center_api
from controller.SpeciesController import  species_api
from controller.AnimalController import animal_api

app.register_blueprint(center_api)
app.register_blueprint(species_api)
app.register_blueprint(animal_api)

if __name__ == "__main__":
    app.run()
