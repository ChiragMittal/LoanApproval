from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(50), unique=True)

    loan_applications = relationship('LoanApplication', back_populates='user', cascade='all, delete-orphan')

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

    loan_status = relationship('LoanStatus', back_populates='loan_application', cascade='all, delete-orphan')
    user = relationship('User', back_populates='loan_applications')

    def to_dict(self):
        return {'id': self.id, 'application_name': self.application_name, 'user_id': self.user_id,
                'credit_score': self.credit_score,
                'loan_amount': self.loan_amount, 'income': self.income, 'loan_purpose': self.loan_purpose
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
