# eMAG Marketplace API Client

The unofficial eMAG Marketplace API Client.
Service available on: https://marketplace.emag.pl/

# Requires
- requests
- python 3.5+

# Example
```python
from emag_marketplace import EMAGClient

client = EMAGClient('user', 'secret')

# Read only one page
print(client.read('category', data={'name': '"Dyski twarde"'}, per_page=10))

# Read many (lazy pagination) 
# - start page = 5,
# - results per page = 5
for category in client.read_many('category', page=5, per_page=5):
    print(category)
```
