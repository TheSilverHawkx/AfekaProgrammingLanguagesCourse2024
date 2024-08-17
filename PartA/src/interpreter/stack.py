from enum import Enum
from typing import Self

class ARType(Enum):
    """
    Enumeration for Activation Record types.

    This Enum defines the types of activation records that can be created,
    corresponding to different constructs within a program.
    """
    PROGRAM     = 'PROGRAM'
    FUNCTION    = 'FUNCTION'
    LAMBDA      = 'LAMBDA'

class ActivationRecord:
    """Represents an activation record in a call stack.

    An activation record stores the context for a function or block, including
    its name, type, nesting level, and members (variables and their values).

    Attributes:
        name (str): The name of the activation record.
        type (ARType): The type of the activation record (PROGRAM, FUNCTION, LAMBDA).
        nesting_level (int): The nesting level of the activation record.
        members (dict): A dictionary holding the variables and their values.

    Usage:
        ar = ActivationRecord(name='main', type=ARType.PROGRAM, nesting_level=1)
        ar['var1'] = 10
    """
    def __init__(
            self,
            name: str,
            type: ARType,
            nesting_level: int,
            old_ar: Self = None
        ) -> None:
        self.name = name
        self.type = type
        self.nesting_level = nesting_level
        self.members = {}

        if old_ar is not None:
            self.members.update(old_ar.members)
    
    def __setitem__(self,key: str,value):
        self.members[key] = value

    def __getitem__(self, key: str):
        return self.members.get(key)
    
    def update(self, kvp: dict):
        self.members.update(kvp)

    def __str__(self):
        s  = [f'{"Activation Record":=^30}']
        for header_name, header_value in (
            ('Record name:', self.name),
            ('Nesting level', self.nesting_level),
            ('Record type:', self.type),
        ):
            s.append(f'{header_name:<15}: {header_value}')
        
        if len(self.members) > 0:
            longest_key = max(len(x) for x in self.members.keys())
            s.append('Members:')
            s.extend([f'{k:>{longest_key}}: {str(v)}' for k,v in self.members.items() ])
        s.append('-'*30)
        return '\n'.join(s)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, level={self.nesting_level}, type={self.type.value})"
    
class CallStack:
    """Represents a call stack for managing activation records.

    The call stack stores a stack of activation records, allowing functions
    and blocks to manage their scopes and contexts during execution.

    Attributes:
        _records (list[ActivationRecord]): A list storing the activation records in the stack.

    Usage:
        ar = ActivationRecord(name='main', type=ARType.PROGRAM, nesting_level=1)
        stack = CallStack()
        stack.push(ar)
        current_ar = stack.peek()
        stack.pop()
    """
    def __init__(self) -> None:
        self._records: list[ActivationRecord] = []

    def push(self, item: ActivationRecord) -> None:
        """Pushes an activation record onto the call stack.

        Args:
            item (ActivationRecord): The activation record to push onto the stack.

        Usage:
            ar = ActivationRecord(name='main', type=ARType.PROGRAM, nesting_level=1)
            stack = CallStack()
            stack.push(ar)
        """
        self._records.append(item)

    def pop(self) -> ActivationRecord:
        """Pops the top activation record from the call stack.

        Returns:
            ActivationRecord: The activation record that was removed from the stack.
        """
        return self._records.pop()
    
    def peek(self) -> ActivationRecord:
        """Returns the top activation record from the call stack without removing it.

        Returns:
            ActivationRecord: The activation record at the top of the stack.
        """
        return self._records[-1]
    
    def __str__(self):
        stack_width=25

        s = [
            f'{"Call Stack": ^{stack_width+2}}\n',
            f"|{" " * stack_width}|",
            f"+{"─" * stack_width}+",
        ]

        for ar in reversed(self._records):
            truncated_name = f"{ar.name[:stack_width - 11] + '...' if len(ar.name) > stack_width else ar.name}"
            s.extend([
                f"|{f"{truncated_name}":^{stack_width}}|",
                f"|{f"{ar.type.value}":^{stack_width}}|",
                f"+{"─" * stack_width}+",
            ])
        return "\n".join(s)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(depth={len(self._records)})"