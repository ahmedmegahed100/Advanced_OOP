# market/services/item_service.py
from market.services.item_service import ItemService
from market.models import Item, User
from market import db

class ItemServiceImpl(ItemService):
    def get_all_items(self):
        return Item.query.filter_by(owner=None).all()

    def get_owned_items(self, user_id):
        return Item.query.filter_by(owner=user_id).all()

    def purchase_item(self, item_name, user_id):
        item = Item.query.filter_by(name=item_name).first()
        user = User.query.get(user_id)
        if item and user.can_purchase(item):
            item.buy(user)
            return True
        return False

    def sell_item(self, item_name, user_id):
        item = Item.query.filter_by(name=item_name).first()
        user = User.query.get(user_id)
        if item and user.can_sell(item):
            item.sell(user)
            return True
        return False
