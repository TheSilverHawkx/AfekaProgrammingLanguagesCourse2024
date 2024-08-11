from enum import Enum

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
    def __init__(self, name: str, type: ARType, nesting_level: int) -> None:
        self.name = name
        self.type = type
        self.nesting_level = nesting_level
        self.members = {}
    
    def __setitem__(self,key: str,value):
        self.members[key] = value

    def __getitem__(self, key: str):
        return self.members.get(key)
    
    def __str__(self):
        lines = [
            '{level}: {type} {name}'.format(
                level=self.nesting_level,
                type=self.type.value,
                name=self.name,
            )
        ]
        for name, val in self.members.items():
            lines.append(f'   {name:<20}: {val}')

        s = '\n'.join(lines)
        return s

    def __repr__(self):
        return self.__str__()
    
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
        return 'CALL STACK\n{records}\n'.format(
            records = '\n'.join(repr(ar) for ar in reversed(self._records))
        )
    
    def __repr__(self) -> str:
        return self.__str__()
