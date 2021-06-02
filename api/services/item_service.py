from market.models import Item


class ItemService:
    @staticmethod
    def fetch_all_items(session):
        return session.query(Item)

    @classmethod
    def fetch_item_by_id(cls, session, id):
        return cls.fetch_all_items(session).filter_by(id=id).first()

