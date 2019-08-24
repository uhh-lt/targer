# Frontend

Implemented with Flask + JQuery + Bootstrap + Displacy

To start server:

```python
python3 frontend.py
```

Parameters are set in config.ini:

```python
# host address and port to publich frontend
publish_host 
publish_port 

# host address and port of the server with running Elastic Search instance
es_host
es_port

# host address and port of the server with running Backend, used for real time labeling
backend_host 
backend_port 
```

