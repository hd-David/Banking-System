from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


Base = declarative_base()


class Customer(Base, UserMixin):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    phone = Column(String)
    email = Column(String)
    username = Column(String)
    password = Column(String)
    accounts = relationship('Account', back_populates='customer')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    account_number = Column(String, unique=True)
    account_type = Column(String)
    balance = Column(Float)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='account')

    def deposit(self, amount):
        self.balance += amount
        transaction = Transaction(date=datetime.now(), amount=amount, description='Deposit', account=self)
        session.add(transaction)
        session.commit()

    def withdraw(self, amount):
        if self.balance < amount:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        transaction = Transaction(date=datetime.now(), amount=amount, description='Withdraw', account=self)
        session.add(transaction)
        session.commit()


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    amount = Column(Float)
    description = Column(String)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship('Account', back_populates='transactions')

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    job_title = Column(String)
    employee_id = Column(String)

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    manager_name = Column(String)
    manager_id = Column(Integer, ForeignKey('employees.id'))
    manager = relationship('Employee')

class Loan(Base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True)
    amount = Column(Float)
    interest_rate = Column(Float)
    payment_schedule = Column(String)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer')

class LoanPayment(Base):
    __tablename__ = 'loan_payments'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    amount = Column(Float)
    loan_id = Column(Integer, ForeignKey('loans.id'))
    loan = relationship('Loan')

# database connection
def dbconnect():
    engine = create_engine("sqlite:///banking.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    print("love you")
    return Session()