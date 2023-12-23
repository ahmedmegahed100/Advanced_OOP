# market/services/user_service.py
from market import db, bcrypt
from market.models import User
from market.services.base_service import BaseService


class UserService(BaseService):
    def register_user(self, username, email, password):
        user = User.query.filter_by(username=username).first()
        if user:
            return False  # Username already exists

        user = User.query.filter_by(email_address=email).first()
        if user:
            return False  # Email address already exists

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email_address=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return True  # Registration successful

    def login_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user  # Successful login
        return None  # Login failed
