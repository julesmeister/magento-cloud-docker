#!/usr/bin/env python3
"""
Test script for AI Search API
"""

import requests
import json

API_BASE = 'http://localhost:5000'

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f'{API_BASE}/health')
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_add_sample_products():
    """Add sample products for testing"""
    print("\nAdding sample products...")
    
    sample_products = [
        {
            'id': 1,
            'name': 'Apple iPhone 15 Pro',
            'description': 'Latest iPhone with advanced camera system and A17 Pro chip',
            'price': 999.99,
            'sku': 'IPHONE15PRO',
            'category': 'Electronics > Smartphones',
            'brand': 'Apple',
            'url': '/iphone-15-pro',
            'image': '/images/iphone15pro.jpg'
        },
        {
            'id': 2,
            'name': 'Samsung Galaxy S24 Ultra',
            'description': 'Premium Android smartphone with S Pen and exceptional camera',
            'price': 1199.99,
            'sku': 'GALAXYS24ULTRA',
            'category': 'Electronics > Smartphones',
            'brand': 'Samsung',
            'url': '/galaxy-s24-ultra',
            'image': '/images/galaxys24.jpg'
        },
        {
            'id': 3,
            'name': 'Sony WH-1000XM5 Headphones',
            'description': 'Premium wireless noise-canceling headphones with exceptional sound quality',
            'price': 399.99,
            'sku': 'SONYWH1000XM5',
            'category': 'Electronics > Audio',
            'brand': 'Sony',
            'url': '/sony-headphones-wh1000xm5',
            'image': '/images/sony-headphones.jpg'
        },
        {
            'id': 4,
            'name': 'MacBook Pro 16-inch M3',
            'description': 'Powerful laptop for professionals with M3 chip and Liquid Retina XDR display',
            'price': 2499.99,
            'sku': 'MACBOOKPRO16M3',
            'category': 'Electronics > Computers',
            'brand': 'Apple',
            'url': '/macbook-pro-16-m3',
            'image': '/images/macbook-pro.jpg'
        },
        {
            'id': 5,
            'name': 'Nike Air Max 270',
            'description': 'Comfortable running shoes with Max Air cushioning and modern design',
            'price': 150.00,
            'sku': 'NIKEAIRMAX270',
            'category': 'Fashion > Shoes > Athletic',
            'brand': 'Nike',
            'url': '/nike-air-max-270',
            'image': '/images/nike-air-max.jpg'
        }
    ]
    
    try:
        response = requests.post(
            f'{API_BASE}/add_products',
            json={'products': sample_products}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Add products failed: {e}")
        return False

def test_search(query):
    """Test search functionality"""
    print(f"\nSearching for: '{query}'")
    
    try:
        response = requests.post(
            f'{API_BASE}/search',
            json={'query': query, 'limit': 5}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"AI Response: {data.get('ai_response', 'No response')}")
            print(f"Found {data.get('total_results', 0)} products:")
            for i, product in enumerate(data.get('products', []), 1):
                print(f"  {i}. {product['name']} - ${product['price']} (Score: {product.get('relevance_score', 0):.2f})")
        else:
            print(f"Error: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Search failed: {e}")
        return False

def test_collection_info():
    """Test collection info endpoint"""
    print("\nGetting collection info...")
    
    try:
        response = requests.get(f'{API_BASE}/collection_info')
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Collection info failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== AI Search API Test Suite ===\n")
    
    # Test health
    if not test_health():
        print("❌ API is not available. Make sure Docker containers are running.")
        return
    
    print("✅ API is healthy")
    
    # Add sample products
    if test_add_sample_products():
        print("✅ Sample products added successfully")
    else:
        print("❌ Failed to add sample products")
    
    # Test collection info
    if test_collection_info():
        print("✅ Collection info retrieved")
    else:
        print("❌ Failed to get collection info")
    
    # Test various searches
    test_queries = [
        "iPhone smartphone",
        "noise canceling headphones",
        "laptop for work",
        "running shoes",
        "Samsung phone"
    ]
    
    for query in test_queries:
        if test_search(query):
            print(f"✅ Search for '{query}' successful")
        else:
            print(f"❌ Search for '{query}' failed")
    
    print("\n=== Test Suite Complete ===")

if __name__ == '__main__':
    main()