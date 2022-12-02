from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

# Protocols aren't really a good fit here, there's little point in this limited problem in defining
# a Protocol that's basically identical to the base HTML class (Div).
# And breaking the compute_screen function out of the class is also silly since it access class members
# which could clearly be self references as a method.


@dataclass
class HTMLElement(Protocol):
    parent: HTMLElement | None
    x: int
    y: int


@dataclass
class Div:
    parent: HTMLElement | None = None
    x: int = 0
    y: int = 0


@dataclass
class Button(Div):
    def click(self) -> None:
        print("Click!")


@dataclass
class Span(Div):
    text: str = ""


def compute_screen_position(element: HTMLElement) -> tuple[int, int]:
    if not element.parent:
        return (element.x, element.y)
    parent_x, parent_y = compute_screen_position(element.parent)
    return (parent_x + element.x, parent_y + element.y)


def main() -> None:
    root = Div(None, 25, 25)
    button = Button(root, 0, 0)
    sub_div = Div(root, 100, 100)
    span = Span(sub_div, 40, 40, "Hello")
    button.click()
    print(compute_screen_position(sub_div))
    print(compute_screen_position(span))


if __name__ == "__main__":
    main()
