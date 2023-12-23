# market/services/item_service.py
from abc import ABC, abstractmethod

class ItemService(ABC):
    @abstractmethod
    def get_all_items(self):
        pass

    @abstractmethod
    def get_owned_items(self, user_id):
        pass

    @abstractmethod
    def purchase_item(self, item_name, user_id):
        pass

    @abstractmethod
    def sell_item(self, item_name, user_id):
        pass
