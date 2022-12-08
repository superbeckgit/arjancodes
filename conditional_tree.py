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


@dataclass
class Trail:
    path: list = field(default_factory=list)


def create_nodes() -> list[Node]:
    one: Node = Node("one", {})
    two: Node = Node("two", {"one": State.FAIL})
    # three: Node = Node("three", {"one": State.PASS, "two": State.FAIL})
    four: Node = Node("four", {"one": State.FAIL, "two": State.PASS})
    # nodes: list[Node] = [one, two, three, four]
    nodes: list[Node] = [one, two, four]
    return nodes


def node_by_name(target_name: str, nodes: list[Node]) -> Node:
    names = [node.name for node in nodes]
    if target_name in names:
        return nodes[names.index(target_name)]
    raise ValueError(f"No node named '{target_name}' in {nodes}")


def backward_inspect(nodes: list[Node]) -> None:
    """Start at last node and work backward building constraints list,
    Look for contradictions in the constraints list
    Error if found
    """
    for node in nodes[::-1]:
        path_constraints: dict[str, State] = node.constraints
        parent_names: list[str] = list(path_constraints.keys())
        while parent_names:
            parent_nodes: list[Node] = [
                node_by_name(parent, nodes) for parent in parent_names
            ]
            parent_constraints: list[dict[str, State]] = [
                node.constraints for node in parent_nodes if node.constraints
            ]
            parent_names = []
            for constraint in parent_constraints:
                for node_name in constraint.keys():
                    parent_names.append(node_name)
                    if node_name in path_constraints:
                        if constraint[node_name] != path_constraints[node_name]:
                            raise ValueError(
                                f"Node '{node.name}' cannot be reached because it depends on multiple states of '{node_name}': {constraint} + {path_constraints}"
                            )


def forward_paths(nodes: list[Node]):
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


if __name__ == "__main__":
    forward_nodes = create_nodes()
    forward_paths(forward_nodes)
    backward_nodes: list[Node] = create_nodes()
    backward_inspect(backward_nodes)
