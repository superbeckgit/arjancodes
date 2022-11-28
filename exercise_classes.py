from dataclasses import dataclass, field

# WAS
# class A:
#   def __init__(self) -> None:
#     self._length = 0

# class B:
#   def __init__(self, x: int, y: str = "hello", l: list[int] | None = None) -> None:
#     self.x = x
#     self.y = y
#     self.l = [] if not l else l

# class C:
#   def __init__(self, a: int = 3) -> None:
#     self.a = a
#     self.b = a + 3

# IS
@dataclass
class A:
    _length: int = field(init=False, default=0)


@dataclass
class B:
    x: int
    y: str = "hello"
    l: list[int] = field(default_factory=list)

    def __post_init__(self):
        if not self.l:
            self.l = []


@dataclass
class C:
    a: int = 3
    b: int = field(init=False)

    def __post_init__(self) -> None:
        self.b = self.a + 3


# PhonyPhones
import datetime


@dataclass
class Address:
    street_number: str
    street_name: str
    unit_info: str | None
    city: str
    state: str
    zip_code: int
    country: str | None


@dataclass
class Name:
    first: str
    middle: str | None
    last: str
    suffix: str | None


@dataclass
class Customer:
    name: Name
    email_address: str
    addresses: list[Address] = field(default_factory=list)


@dataclass
class Phone:
    brand: str
    model: str
    price: int
    serial_number: int


class Plan:
    customer: Customer
    phone: Phone
    start_date: datetime.datetime
    total_months: int
    monthly_price: int
    phone_included: bool
