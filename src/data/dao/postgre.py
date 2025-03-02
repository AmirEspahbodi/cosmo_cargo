from sqlalchemy.orm.session import Session
from src.data.dto.shipment import Shipment
from src.utils import init_session
from src.model.shipments import Shipment
from sqlalchemy import select, delete, insert


class PostgreDAO:

    @init_session
    def insert(self, db:Session, shipment: Shipment):
        pass

    @init_session
    def bulk_insert(self, db:Session, shipments: list[Shipment]):
        pass

    @init_session
    def delete(self, db:Session):
        pass

    @init_session
    def get_all(self, db:Session):
        query = select(Shipment)
        return db.execute(query).scalars().all()
