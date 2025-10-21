import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

__data_manager = None
__data_manager_txt = os.urandom(16)

class DataManager:
    def __new__(cls, *args, **kwargs):
        global __data_manager
        if __data_manager is None:
            __data_manager = super().__new__(cls)
        return __data_manager

    def __init__(self, path: Path = None, driver: str = "sqlite", file_name_override: str = None):
        global __data_manager_txt
        if path is None:
            path = Path.cwd() / ".." / "data"
        self.path = path
        self.data_drivers = {
            "sqlite": SqliteDriver,
            "json": JsonDriver,
        }
        driver = self.data_drivers[driver](self.path, file_name=file_name_override, dtx=__data_manager_txt)
        if driver is NotImplemented or driver is None:
            raise ValueError(f"Driver {driver} is not supported.")
        self.driver = driver
        self.current_driver_name = driver

    def __getattr__(self, name):
        return getattr(self.driver, name)

class DataDriver(ABC):
    file_name: str
    __implemented = True

    def __new__(cls, dtx, *args, **kwargs):
        global __data_manager, __data_manager_txt
        if dtx != __data_manager_txt:
            raise ValueError("Driver must be initialized through DataManager.")
        if __data_manager is None:
            raise ValueError("DataManager is not initialized.")
        if not cls.__implemented:
            return NotImplemented
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, file_path: Path, file_name: str = None):
        if file_name is not None:
            self.file_name = file_name
        self.file_path = file_path / self.file_name
        if not self.file_path.exists():
            self.file_path.touch()

    @abstractmethod
    def init_data(self):
        """Initializes the data file."""
        pass

    def get_data(self, where: str = None, *args, **kwargs):
        """Returns the data."""
        pass

    def set_data(self, data, *args, **kwargs):
        """Sets the data."""
        pass

    def get_connection(self):
        """Returns a connection (e.g. a cursor for sqlite)."""
        return None

class SqliteDriver(DataDriver):
    file_name = "sqlite.db"
    __implemented = False

    def __init__(self, file_path: Path, file_name: str = None, dtx=None):
        self.cursor = self.get_connection()

        super().__init__(file_path, file_name)

    def get_data(self, where: str = None, *args, **kwargs):
        pass

    def set_data(self, data, where: str = None, *args, **kwargs):
        pass

    def init_data(self):
        if not self.file_path.exists():
            self.file_path.touch()
            self.cursor = self.get_connection()

    def create_table(self, cursor=None, fields: list | None = None, table_name: str | None = None) -> None:
        if fields is None or table_name is None:
            raise ValueError("You must specify the table name and its values.")
        cr = f"CREATE TABLE IF NOT EXISTS {table_name}("
        for field in fields:
            cr += f"{field.name} {field.type},"
        cursor.execute(cr)

    def get_connection(self):
        import sqlite3
        return sqlite3.connect(self.file_path)

class JsonDriver(DataDriver):
    file_name = "data.json"

    def get_data(self, where: str = None, *args, **kwargs):
        if where is None:
            return None
        with open(self.file_path, "r") as f:
            if where.count(".") > 0:
                for key in where.split("."):
                    data = data[key]
            else:
                data = data[where]
            return data

    def set_data(self, data, where: str = None, *args, **kwargs):
        with open(self.file_path, "w") as f:
            if where is None:
                json.dump(data, f)
            else:
                for key in where.split("."):
                    _ = _[key]
                _ = data

    def init_data(self):
        pass