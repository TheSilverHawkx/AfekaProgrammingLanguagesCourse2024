import pytest
from src.interpreter.stack import ActivationRecord,ARType,CallStack

def test_activation_record_create():
    ar_details = {
        'name': 'main',
        'type':ARType.PROGRAM,
        'nesting_level': 1
    }
    ar = ActivationRecord(**ar_details)

    assert ar.name == ar_details['name']
    assert ar.type == ar_details['type']
    assert ar.nesting_level == ar_details['nesting_level']

def test_activation_record_members():
    ar_details = {
        'name': 'main',
        'type':ARType.PROGRAM,
        'nesting_level': 1
    }
    ar = ActivationRecord(**ar_details)

    ar['x'] = 1

    ar['y'] = 20

    assert ar['x'] == 1
    assert ar['y'] == 20
    ar['x'] = 2
    assert ar['x'] == 2
    assert ar['z'] is None

def test_activation_record_update():
    ar_details = {
        'name': 'main',
        'type':ARType.PROGRAM,
        'nesting_level': 1
    }
    ar = ActivationRecord(**ar_details)

    ar['x'] = 1
    ar['y'] = 2

    ar2 = ActivationRecord(
        name='nested',
        nesting_level= ar.nesting_level +1,
        type= ARType.FUNCTION
    )

    ar2.update(ar.members)

    assert ar2['x'] == 1
    assert ar2['y'] == 2

    ar2['y'] = 3
    assert ar2['y'] == 3

def test_call_stack_push_pop():
    stack = CallStack()

    ar1 = ActivationRecord(name='main', type=ARType.PROGRAM, nesting_level=1)
    ar2 = ActivationRecord(name='foo', type=ARType.FUNCTION, nesting_level=2)

    stack.push(ar1)
    stack.push(ar2)

    assert stack.pop() == ar2
    assert stack.pop() == ar1

def test_call_stack_peek():
    stack = CallStack()
    ar1 = ActivationRecord(name='main', type=ARType.PROGRAM, nesting_level=1)
    ar2 = ActivationRecord(name='foo', type=ARType.FUNCTION, nesting_level=2)

    stack.push(ar1)
    stack.push(ar2)

    assert stack.peek() == ar2
    assert stack.pop() == ar2
    assert stack.peek() == ar1

def test_call_stack_pop_empty():
    stack = CallStack()
    with pytest.raises(IndexError):
        stack.pop()