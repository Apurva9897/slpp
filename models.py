from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

signatures = db.Table(
    'signatures',
    db.Column('petition_id', db.Integer, db.ForeignKey('petitions.petition_id'), primary_key=True),
    db.Column('petitioner_email', db.String(100), db.ForeignKey('petitioners.email'), primary_key=True)
)

class BioID(db.Model):
    __tablename__ = 'bioid'
    code = db.Column(db.String(20), primary_key=True)
    used = db.Column(db.Integer, default=0)

class Petitioner(UserMixin, db.Model):
    __tablename__ = 'petitioners'
    email = db.Column(db.String(100), primary_key=True)
    fullname = db.Column(db.String(100))
    dob = db.Column(db.Date)
    password_hash = db.Column(db.Text)
    bioid = db.Column(db.String(45), db.ForeignKey('bioid.code'))
    
    petitions = db.relationship('Petition', backref='creator', lazy=True)
    
    signed_petitions = db.relationship(
        'Petition', 
        secondary=signatures, 
        back_populates='signed_by'
    )

    def get_id(self):
        return self.email

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

class Petition(db.Model):
    __tablename__ = 'petitions'
    petition_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    petitioner_email = db.Column(db.String(100), db.ForeignKey('petitioners.email'))
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    status = db.Column(db.String(45), default='open')
    response = db.Column(db.Text)
    signature_count = db.Column(db.Integer, default=0)

    signed_by = db.relationship(
        'Petitioner', 
        secondary=signatures, 
        back_populates='signed_petitions'
    )

class CommitteeMember(UserMixin, db.Model):
    __tablename__ = 'committee_members'
    email = db.Column(db.String(100), primary_key=True) 
    password_hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_id(self):
        return f"committee:{self.email}"

class AppConfig(db.Model):
    __tablename__ = 'app_config'
    id = db.Column(db.Integer, primary_key=True)
    signature_threshold = db.Column(db.Integer, nullable=False, default=100)
