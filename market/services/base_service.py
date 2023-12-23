# market/services/base_service.py
from abc import ABC, abstractmethod

class BaseService(ABC):
    @abstractmethod
    def register_user(self, username, email, password):
        pass

    @abstractmethod
    def login_user(self, username, password):
        pass
