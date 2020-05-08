import json

from flask_sqlalchemy import SQLAlchemy

from settings import app

db = SQLAlchemy(app)


class Center(db.Model):
    __tablename__ = 'centers'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def json(self):
        return {'id': self.id, 'login': self.login, 'password': self.password, 'address': self.address}

    def add_center(self):
        new_center = Center(login=self.login, password=self.password, address=self.address)
        db.session.add(new_center)
        db.session.commit()

    def get_all_centers(self):
        return [Center.json(centers) for centers in Center.query.all()]

    def get_center(self, id):
        return Center.query.filter_by(id=id).first()

    def __repr__(self):
        center_object = {
            'id': self.id,
            'login': self.login,
            'password': self.password,
            'price': self.price,
        }
        return json.dumps(center_object)
