from genericpath import exists
from threading import current_thread
import nice_math
from appp import data_collector
from datetime import datetime


class Driver:
    truck_id: str
    raw: dict

    def __init__(self, stupid_format_dict, key):
        self.truck_id = key
        self.raw = stupid_format_dict

    def get_number_plate(self):
        if len(self.raw["NAME1"].split(sep=" ", maxsplit=1)[0]) < 3:
            return "".join(self.raw["NAME1"].split(sep=" ", maxsplit=1))
        else:
            return self.raw["NAME1"].split(sep=" ", maxsplit=1)[0]


class Truck:
    truck_id: str
    lat: float
    lon: float
    current_driver: Driver = None
    gps_time: int
    last_fetch_time: int
    last_update_time: int

    def __init__(self, stupid_format_array, time):
        self.truck_id = str(stupid_format_array[0])
        self.lat, self.lon = nice_math.get_position(
            stupid_format_array[4], stupid_format_array[3])
        self.gps_time = stupid_format_array[2]
        self.last_fetch_time = time
        self.last_update_time = time

    def update(self, stupid_format_array, time):
        new_lat, new_lon = nice_math.get_position(
            stupid_format_array[4], stupid_format_array[3])
        if new_lat != self.lat and new_lon != self.lon:
            self.last_update_time = time
            self.lat, self.lon = new_lat, new_lon
        self.last_fetch_time = time

    def __str__(self):
        return "{}, {}".format(self.get_number_plate(), self.truck_id)

    def as_dict(self):
        if self.current_driver != None:
            return {"truck_id": self.truck_id, "lat": self.lat, "lon": self.lon, "NAME1": self.current_driver.raw["NAME1"], "NAME2": self.current_driver.raw["NAME2"]}
        else: 
            return {"truck_id": self.truck_id, "lat": self.lat, "lon": self.lon, "current_driver": "No driver"}

    def get_position(self):
        return (self.lat, self.lon)

    def get_current_driver(self):
        return self.current_driver

    def set_current_driver(self, driver):
        self.current_driver = driver

    def get_number_plate(self):
        if self.current_driver != {}:
            return self.current_driver.get_number_plate()
        else:
            return "No number plate!"


def all_data_reader(current_trucks: dict):

    current_time = int(round(datetime.now().timestamp()))
    trucks_info, gps_tail, drivers_info = data_collector()

    drivers: list[Driver] = {}

    some_keys = drivers_info.keys()

    for key in some_keys:
        drivers[key] = Driver(drivers_info[key], key)

    for truck_info in trucks_info:
        key = truck_info[0]
        if key in current_trucks:
            current_trucks[key].update(truck_info, current_time)
        else:
            current_trucks[key] = Truck(truck_info, current_time)
            if str(key) in drivers:
                current_trucks[key].set_current_driver(drivers[str(key)])

    return drivers, current_trucks, current_time
