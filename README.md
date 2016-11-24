# python-wd40

## Why WD40 ?

WD40 is a the ultimate tool when you want to have block but should move 

It'a simple toolbox

### Dead man alarm

Dead man alarm, it's a system to execute an function when the object didn't notify since a long time
I'm using it to verify if a device is really sending me a heartbeat.
```python
dma = DeadManAlarm(5, lambda: notify_me(), )

def on_message_recieve():
    dma.i_m_alive()
    ...

def on_heartbeat_recieve():
    dma.i_m_alive()

def notify_me():
    print("I'm maybe dead, please rescue me.")    
    
```

### Dict conversion

It's a way to convert a dict to an object
```python

d = {'name': 'object', 'value': 20, 'creation_time': time.time() }

print(d['name'])

od = DictToObj(d)

print(od.name)
print(od.creation_time)

```

### Try except

I'm using it a lot, I now it's like hiding dust under the carpet.
  
```python
con_redis = redis.Redis('localhost')
val = try_except(lambda: con_redis.get('some_key').decode(), '')

a = [0, 1, 2]
val2 = try_except(lambda: a[50], -1, IndexError)

def oups()
    print('oups')
    
try_except(lambda: a[50], lambda: oups(), IndexError)

```

### Wait until

To wait until a condition become True.
It's hard to give a demo example, but it wait until predicate become True

```python
device.connect()
if not wait_until(lambda: device.is_connected(), timeout=5):
    print('oups, connection failed')
    return
print('ready to use')
```