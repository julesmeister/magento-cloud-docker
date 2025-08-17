import requests

# Test single search
response = requests.post(
    "http://localhost:5000/search",
    json={"query": "smartphone", "limit": 3}
)

if response.status_code == 200:
    result = response.json()
    print("Query: smartphone")
    print(f"AI Response: {result.get('ai_response')}")
    print(f"Products found: {len(result.get('products', []))}")
    for p in result.get('products', []):
        print(f"  - {p.get('name')} - ${p.get('price')}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)