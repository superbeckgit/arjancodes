from __future__ import annotations

import copy
from dataclasses import dataclass, field
from enum import Enum
from pprint import pprint as pp


class State(Enum):
    FAIL: int = 0
    PASS: int = 1


@dataclass
class Node:
    name: str
    constraints: dict[str, State]
    reached: bool = False


one: Node = Node("one", {})
two: Node = Node("two", {"one": State.FAIL})
three: Node = Node("three", {"one": State.PASS, "two": State.FAIL})
four: Node = Node("four", {"one": State.FAIL, "two": State.PASS})
nodes: list[Node] = [one, two, three, four]


@dataclass
class Trail:
    path: list = field(default_factory=list)


trails: list[Trail] = []
node: Node = nodes[0]
assert node.constraints == {}
node.reached = True
for state in State.__members__.keys():
    path: tuple[str, str] = (node.name, state)
    trails.append(Trail([path]))

node_ix: int = 1
trail_ix: int = 0
while trail_ix < len(trails) and node_ix < len(nodes):
    node = nodes[node_ix]
    trail: Trail = trails[trail_ix]
    reached: bool = all(
        [
            (parent_name, state.name) in trail.path
            for parent_name, state in node.constraints.items()
        ]
    )
    if reached:
        node.reached = True
        print(f"Node '{node.name}' is reachable via {trail.path}")
        trail_copy: Trail = copy.deepcopy(trail)
        trail.path.append((node.name, State.FAIL.name))
        trail_copy.path.append((node.name, State.PASS.name))
        trails.append(trail_copy)
        node_ix += 1
        # continue
    else:
        print(
            f"Trail {trail.path} does not satisfy {node.constraints} constraint for node {node.name}"
        )
        if trail_ix + 1 == len(trails):
            node_ix += 1
        else:
            trail_ix += 1

    # breakpoint()
pp(nodes)
