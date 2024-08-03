from enum import Enum


class ARType(Enum):
    PROGRAM = 'PROGRAM'
    PROCEDURE = 'PROCEDURE'

class ActivationRecord:
    def __init__(self, name: str, type: ARType, nesting_level: int) -> None:
        self.name = name
        self.type = type
        self.nesting_level = nesting_level
        self.members = {}

    def __setitem__(self,key,value):
        self.members[key] = value

    def __getitem__(self,key):
        return self.members.get(key)
    
    def __str__(self) -> str:
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
    def __init__(self) -> None:
        self._records: list[ActivationRecord] = []

    def push(self,item) -> None:
        self._records.append(item)

    def pop (self) -> ActivationRecord:
        return self._records.pop()
    
    def peek(self) -> ActivationRecord:
        return self._records[-1]
    
    def __str__(self):
        s = '\n'.join(repr(ar) for ar in reversed(self._records))
        s = f'CALL STACK\n{s}\n'

        return s
    
    def __repr__(self) -> str:
        return self.__str__()
    