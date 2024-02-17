from flask import Flask, request, jsonify 
from sqlalchemy import create_engine
from marshmallow import Schema, fields
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from flask_restful import Resource, Api
from sqlalchemy.orm import sessionmaker, relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

import logging

logging.basicConfig(filename='loan_system.log', level=logging.INFO)

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(50), unique=True)
    
    loan_applications = relationship('LoanApplication', back_populates='user')

    def to_dict(self):
        return {'id': self.id, 'name': self.name}


class LoanApplication(Base):
    __tablename__ = 'loan_application'

    id = Column(String, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    application_name = Column(String)
    credit_score = Column(Integer)
    loan_purpose = Column(String(100))
    loan_amount = Column(Float)
    income = Column(Float)
    employment_status = Column(String(50))

    loan_status = relationship('LoanStatus', back_populates='loan_application')
    user = relationship('User', back_populates='loan_applications')

    def to_dict(self):
        return {'id': self.id, 'application_name': self.application_name, 'user_id': self.user_id, 'credit_score': self.credit_score,
        'loan_amount': self.loan_amount, 'income':self.income, 'loan_purpose': self.loan_purpose
        , 'employment_status': self.employment_status}


class LoanStatus(Base):
    __tablename__ = 'loan_status'

    id = Column(String, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    loan_application_id = Column(Integer, ForeignKey('loan_application.id'))
    risk_score = Column(Float)
    status = Column(String(100))

    loan_application = relationship('LoanApplication', back_populates='loan_status')

    def to_dict(self):
        return {'id': self.id, 'loan_application_id': self.loan_application_id, 'risk_score': self.risk_score
        , 'status': self.status}

class RiskAssessment:

    @staticmethod
    def assess_risk(application):

        risk_score = (application.get('credit_score')/1000) * 0.7 + (application.get('loan_amount')/application.get('income')) * 0.2 
        + (1 if (application.get('employment_status')).lower() == 'employed' else 0) * 0.1

        return risk_score


db_connect = create_engine('sqlite:///loan.db')
Base.metadata.create_all(db_connect)
app = Flask(__name__)
api = Api(app)
Session = sessionmaker(bind=db_connect)
session = Session()

@app.route("/get_all_loan_applications", methods=["GET"])
def get_all_loan_applications():
    applications = session.query(LoanApplication).all()
    if applications:
        applications_list = [application.to_dict() for application in applications]
        return jsonify(applications_list)
    else:
        return jsonify({'error': 'Applications not found'}), 404

@app.route("/all_users", methods=["GET"])
def all_users():
    users = session.query(User).all()
    if users:
        user_list = [user.to_dict() for user in users]
        return jsonify(user_list)
    else:
        return jsonify({'error': 'Users not found'}), 404

@app.route("/create_new_loan_application", methods=["POST"])
def create_new_loan_application():
    data = request.get_json()

    new_application_id = str(uuid.uuid4())
    new_application = LoanApplication(
        id=new_application_id,
        application_name = data.get('application_name'), 
        user_id = data.get("user_id"),
        credit_score = data.get('credit_score'),
        loan_purpose = data.get('loan_purpose'),
        loan_amount = data.get('loan_amount'),
        income = data.get('income'),
        employment_status = data.get('employment_status')
    )

    session.add(new_application)

    risk_score = RiskAssessment.assess_risk(data)

    new_risk_score = LoanStatus(
        loan_application_id = new_application_id,
        risk_score = risk_score,
        status = ("Approved" if risk_score> 0.5 else "Denied"),
        id=str(uuid.uuid4())
    )

    session.add(new_risk_score)
    session.commit()


    return jsonify(
        data
    ), 201


@app.route("/create_new_user", methods=["POST"])
def create_new_user():
    data = request.get_json()

    new_user_id = str(uuid.uuid4())
    new_user = User(
        id=new_user_id ,
        name = data.get('name')
    )

    session.add(new_user)
    session.commit()


    return jsonify(
        data
    ), 201

@app.route("/risk_score", methods=["POST"])
def get_risk_score():
    data = request.get_json()
    application = session.query(LoanApplication).filter_by(id=data.get('id')).first()
    if application:
        single =  application.to_dict()
        risk_score = RiskAssessment.assess_risk(single)
    else:
        return jsonify({'error': 'Risk Score not found'}), 404

    return (str(risk_score)), 200

@app.route("/get_all_per_user", methods=["POST"])
def get_all_loan_applications_per_user():
    data = request.get_json()
    applications = session.query(LoanApplication).filter_by(user_id=data.get('id')).all()
    if applications:
        all =  [application.to_dict() for application in applications]
        return (all), 200
    else:
        return jsonify({'error': 'Risk Score not found'}), 404


@app.route("/update_application_name", methods=["POST"])
def update_application_name():
    data = request.get_json()

    application = session.query(LoanApplication).filter_by(id=data.get('id')).first()

    if application:
        application.application_name = data.get('application_name')

    session.commit()


    return jsonify(
        data
    ), 201


@app.route('/delete_application', methods=['POST'])
def delete_user():
    data = request.get_json()
    appplication_to_delete = session.query(LoanApplication).filter_by(id=data.get('id')).first()

    if appplication_to_delete:
        session.delete(appplication_to_delete)
        session.commit()

        return jsonify({'message': 'Application deleted successfully'})
    else:
        return jsonify({'error': 'Application not found'})


if __name__ == "__main__":
    app.run(debug=True)