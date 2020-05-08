import json
import time

from flask_sqlalchemy import SQLAlchemy

from settings import app

db = SQLAlchemy(app)


class AccessLog(db.Model):
    __tablename__ = 'access_log'
    center_id = db.Column(db.Integer, nullable=False)
    time_stamp = db.Column(db.TIMESTAMP(), primary_key=True)

    def json(self):
        return {'center_id': self.center_id, 'time_stamp': self.time_stamp}

    def add_access_log(self, _center_id):
        new_access_log = AccessLog(center_id=_center_id, time_stamp=time.time())
        db.session.add(new_access_log)
        db.session.commit()

    def get_all_access_logs(self):
        return [AccessLog.json(access_logs) for access_logs in AccessLog.query.all()]

    def get_per_center_access_log(self, _center_id):
        return AccessLog.query.filter_by(id=_center_id).first()

    def __repr__(self):
        access_log_object = {
            'center_id': self.center_id,
            'time_stamp': self.time_stamp,
        }
        return json.dumps(access_log_object)
