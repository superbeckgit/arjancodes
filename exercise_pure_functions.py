import random
import string
from dataclasses import dataclass
from datetime import datetime
from typing import Callable

# def generate_id(length: int) -> str:
#     return "".join(
#         random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
#     )

Picker = Callable[[], str]


def generate_id(length: int, picker: Picker) -> str:
    return "".join(picker() for _ in range(length))


# def weekday() -> str:
#     today = datetime.today()
#     return f"{today:%A}"


def weekday(date: datetime) -> str:
    return f"{date:%A}"


# def main() -> None:
#     print(f"Today is a {weekday()}")
#     print(f"Your id = {generate_id(10)}")


def main() -> None:
    today = datetime.today()
    print(f"Today is a {weekday(today)}")
    picker: Picker = lambda: random.choice(string.ascii_uppercase + string.digits)
    print(f"Your id = {generate_id(10, picker)}")


## second question
@dataclass
class Laptop:
    machine_name: str = "DULL"

    def install_os(self) -> None:
        print("Installing OS")

    def format_hd(self) -> None:
        print("Formatting the hard drive")

    def create_admin_user(self, password: str) -> None:
        print(f"Creating admin user with password {password}.")

    def reset(self) -> None:
        # new reset method
        self.machine_name = "DULL"
        self.format_hd()
        self.install_os()
        self.create_admin_user("admin")


def reset(laptop: Laptop) -> None:
    # new reset function
    laptop.machine_name = "DULL"
    laptop.format_hd()
    laptop.install_os()
    laptop.create_admin_user("admin")


if __name__ == "__main__":
    main()
    lappy = Laptop()
    lappy.reset()
    reset(lappy)
