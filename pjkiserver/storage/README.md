Storage
=======

## Interface

### How to connect to the storage module
```python
from .storage.storage import storage
```

### How to save something
```python
team = {
    'yourdata': 'here'
}
storage['teams'] = team
```

### How to read something
```python
team = storage['teams']
```

### How to iterate over all entries
```python
for key in storage:
    value = storage[key]
```

## Important Information
- The module only accepts String keys, if not a type error will be raised!
- The values must be convertable to json if its not there will occur errors
	which are not handled yet!
