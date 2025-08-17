#!/usr/bin/env python3
"""
Simple test script for AI Search API
"""

import requests
import json

# Sample products for testing
sample_products = [
    {
        "id": "1",
        "sku": "iphone-15-pro",
        "name": "iPhone 15 Pro",
        "description": "Latest iPhone with A17 Pro chip, titanium design, and advanced camera system. Perfect for photography and professional use.",
        "price": "999.00",
        "category": "Electronics, Smartphones",
        "brand": "Apple",
        "url": "http://localhost/iphone-15-pro",
        "image": "http://localhost/media/iphone-15-pro.jpg"
    },
    {
        "id": "2", 
        "sku": "macbook-air-m3",
        "name": "MacBook Air M3",
        "description": "Ultra-thin laptop with M3 chip, 13-inch Liquid Retina display, and all-day battery life. Great for students and professionals.",
        "price": "1299.00",
        "category": "Electronics, Laptops",
        "brand": "Apple",
        "url": "http://localhost/macbook-air-m3",
        "image": "http://localhost/media/macbook-air.jpg"
    },
    {
        "id": "3",
        "sku": "nike-air-max-90",
        "name": "Nike Air Max 90",
        "description": "Classic running shoes with visible Air cushioning, durable design, and comfortable fit. Perfect for daily wear and light exercise.",
        "price": "120.00",
        "category": "Footwear, Sneakers",
        "brand": "Nike",
        "url": "http://localhost/nike-air-max-90",
        "image": "http://localhost/media/nike-air-max-90.jpg"
    },
    {
        "id": "4",
        "sku": "samsung-galaxy-s24",
        "name": "Samsung Galaxy S24",
        "description": "Premium Android smartphone with AI features, excellent camera, and bright AMOLED display. Great for photography and gaming.",
        "price": "899.00",
        "category": "Electronics, Smartphones",
        "brand": "Samsung",
        "url": "http://localhost/samsung-galaxy-s24",
        "image": "http://localhost/media/galaxy-s24.jpg"
    },
    {
        "id": "5",
        "sku": "sony-wh1000xm5",
        "name": "Sony WH-1000XM5 Headphones",
        "description": "Industry-leading noise canceling wireless headphones with exceptional sound quality and 30-hour battery life.",
        "price": "399.00",
        "category": "Electronics, Audio",
        "brand": "Sony",
        "url": "http://localhost/sony-wh1000xm5",
        "image": "http://localhost/media/sony-headphones.jpg"
    }
]

def check_api_health():
    """Check if the AI Search API is healthy"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=10)
        
        if response.status_code == 200:
            health = response.json()
            print("API Health Check:")
            print(f"   Status: {health.get('status', 'unknown')}")
            print(f"   ChromaDB Connected: {health.get('chroma_connected', False)}")
            print(f"   OpenAI Configured: {health.get('openai_configured', False)}")
            return True
        else:
            print(f"API health check failed: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("Cannot connect to AI Search API. Make sure Docker services are running.")
        return False
    except Exception as e:
        print(f"Health check error: {e}")
        return False

def add_sample_products():
    """Add sample products to the AI Search API"""
    api_url = "http://localhost:5000/add_products"
    
    try:
        response = requests.post(
            api_url,
            json={"products": sample_products},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Successfully added {result.get('count', len(sample_products))} sample products")
            return True
        else:
            print(f"Error: API returned status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to AI Search API at http://localhost:5000")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_search():
    """Test the search functionality"""
    api_url = "http://localhost:5000/search"
    
    test_queries = ["smartphone", "laptop", "headphones"]
    
    print("\nTesting search functionality...")
    
    for query in test_queries:
        try:
            response = requests.post(
                api_url,
                json={"query": query, "limit": 3},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"\nQuery: '{query}'")
                print(f"AI Response: {result.get('ai_response', 'No response')}")
                print(f"Found {len(result.get('products', []))} products")
                
                for product in result.get('products', [])[:2]:
                    print(f"   - {product.get('name')} - ${product.get('price')}")
            else:
                print(f"Search failed for '{query}': {response.status_code}")
                
        except Exception as e:
            print(f"Search error for '{query}': {e}")

if __name__ == "__main__":
    print("AI Search Setup & Testing")
    print("=" * 40)
    
    # Check API health first
    if check_api_health():
        print("\nAdding sample products...")
        if add_sample_products():
            print("\nWaiting for indexing...")
            import time
            time.sleep(2)
            
            # Test search functionality
            test_search()
            
            print("\nSetup complete! Test the AI search widget on your Magento store.")
        else:
            print("Failed to add products.")
    else:
        print("Setup failed. Please check that Docker services are running.")