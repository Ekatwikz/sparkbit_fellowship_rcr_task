"""Robotic Code Representation Module.

Generate RCR strings that try to prioritise frequently used commands,
when given a log of command history

Classes:
    * RoboticCodeRepresentationGenerator - generate rcr codes from command log
    * CommandTree - represents a tree of commands
"""

from __future__ import annotations

from typing import List, Dict
import heapq
import dataclasses


@dataclasses.dataclass(order=True)
class CommandTree:
    """Binary tree with frequency and command.

    Attributes:
        total_freq: Sum of leaves' frequencies
        left: Left subtree
        right: Right subtree
        command: Command string (leaf only)
    """
    total_freq: int
    left: CommandTree | None = dataclasses.field(default=None, compare=False)
    right: CommandTree | None = dataclasses.field(default=None, compare=False)
    command: str | None = dataclasses.field(default=None, compare=False)


class RoboticCodeRepresentationGenerator:
    """Generate RCR codes of commands from a given log."""

    _command_rcr_codes: Dict[str, str]

    def __init__(self, issued_commands: List[str]):
        """
        Args:
            issued_commands: A list of commands; represents the command log
        """
        self._command_rcr_codes = {}

        command_frequencies: Dict[str, int] = {}
        for command in issued_commands:
            command_frequencies[command] = \
                    command_frequencies.get(command, 0) + 1

        # Generate full tree using heap
        command_tree: List[CommandTree] = []
        for command, freq in command_frequencies.items():
            heapq.heappush(command_tree, CommandTree(freq, command=command))

        while len(command_tree) > 1:
            left = heapq.heappop(command_tree)
            right = heapq.heappop(command_tree)
            heapq.heappush(command_tree,
                           CommandTree(left.total_freq + right.total_freq,
                                       left,
                                       right)
                           )

        # DFS traversal to generate codes
        # Here the command tree heap is now used as a stack
        rcr_stack = [""]
        while command_tree:
            command_node = command_tree.pop()
            rcr_code = rcr_stack.pop()

            if command_node.left is None:
                self._command_rcr_codes[command_node.command] = rcr_code
            else:
                command_tree.append(command_node.right)
                rcr_stack.append(rcr_code + "1")
                command_tree.append(command_node.left)
                rcr_stack.append(rcr_code + "0")

    def get_rcr(self, command: str) -> str:
        """
        Args:
            command: The command to retrieve RCR for

        Returns:
            The RCR string that encodes the given command
        """
        return self._command_rcr_codes[command]
