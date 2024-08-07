from enum import Enum

class ARType(Enum):
    PROGRAM     = 'PROGRAM'
    FUNCTION    = 'FUNCTION'
    LAMBDA      = 'LAMBDA'

class ActivationRecord:
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
    def __init__(self) -> None:
        self._records: list[ActivationRecord] = []

    def push(self, item: ActivationRecord) -> None:
        self._records.append(item)

    def pop(self) -> ActivationRecord:
        return self._records.pop()
    
    def peek(self) -> ActivationRecord:
        return self._records[-1]
    
    def __str__(self):
        return 'CALL STACK\n{records}\n'.format(
            records = '\n'.join(repr(ar) for ar in reversed(self._records))
        )
    
    def __repr__(self) -> str:
        return self.__str__()