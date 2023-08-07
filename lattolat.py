import nice_math
from appp import data_collector


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
    current_driver: Driver = {}

    def __init__(self, stupid_format_array):
        self.truck_id = str(stupid_format_array[0])
        self.lat, self.lon = nice_math.get_position(
            stupid_format_array[4], stupid_format_array[3])

    def __str__(self):
        return "{}, {}".format(self.get_number_plate(), self.truck_id)

    def as_dict(self):
        return {"truck_id": self.truck_id, "lat": self.lat, "lon": self.lon, "current_driver": self.current_driver.__dict__}

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


def all_data_reader():

    trucks_info, gps_tail, some_another_info = data_collector()

    drivers: list[Driver] = []

    some_keys = some_another_info.keys()

    for key in some_keys:
        drivers.append(Driver(some_another_info[key], key))

    trucks: list[Truck] = []

    for truck_info in trucks_info:
        trucks.append(Truck(truck_info))

    for driver in drivers:
        for i in range(len(trucks)):
            if trucks[i].truck_id == driver.truck_id:
                trucks[i].set_current_driver(driver)
    return drivers, trucks
