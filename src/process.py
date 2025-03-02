from time import sleep
from typing import List, Set, Dict, Tuple
from src.config import AppConfig
from .data import FetchDao, RedisDao
from .data.dto.shipment import Shipment


class CosmoCargoProcess:
    def __init__(self):
        self.fetch_dao = FetchDao("https://censibal.github.io/txr-technical-hiring/")
        self.redis_dao = RedisDao()

    def start(self):
        while True:
            if self.if_end():
                break
            self.do()
            sleep(AppConfig.FETCH_INTERVAL)

    def do(self):
        # get new data from web source
        new_shipments = self.get_new_shipments()
        print(f"new_shipments = {new_shipments}")
        
        # insert new data to db
        
        # insert new data to redis

    def get_new_shipments(self) -> List[Shipment]:

        source_data: List[Shipment] = self.fetch_dao.get_data()
        existing_data: List[Shipment] = self.redis_dao.get_all_shipments()
        
        existing_shipment_keys: Set[str] = set()
        for shipment in existing_data:
            key = self._create_shipment_key(shipment)
            existing_shipment_keys.add(key)
        
        new_shipments: List[Shipment] = []
        for shipment in source_data:
            key = self._create_shipment_key(shipment)
            if key not in existing_shipment_keys:
                new_shipments.append(shipment)
        
        return new_shipments

    def _create_shipment_key(self, shipment: Shipment) -> str:
        fields = [
            "time",
            "weight_kg",
            "volume_m3",
            "eta_min",
            "status",
            "forecast_origin_wind_velocity_mph",
            "forecast_origin_wind_direction",
            "forecast_origin_precipitation_chance",
            "forecast_origin_precipitation_kind",
            "origin_solar_system",
            "origin_planet",
            "origin_country",
            "origin_address",
            "destination_solar_system",
            "destination_planet",
            "destination_country",
            "destination_address",
        ]
        
        return ",".join([str(getattr(shipment, f)) for f in fields])

    def if_end(self):
        return False