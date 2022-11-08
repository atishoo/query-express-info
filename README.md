# 查询物流信息

通过浏览器，使用百度搜索，自动查询物流信息

- 另外有一个快递100的接口：Kuaidi100

### Kuaidi100

##### __init__(customer, key)
设置customer和key

##### setNum(num)
设置物流单号，返回类

##### track()
查询物流信息，返回None或物流信息

##### detect_carrier()
检测物流运营商，返回None或可能的物流运营商列表

eg:
```python
info = Kuaidi100('customer', 'key')->setNum('express no')->track()
```

### Kuaidi100State
快递100的state对应的物流状态

eg:
```python
state = Kuaidi100State[int(info['state'])]
```