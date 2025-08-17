#!/usr/bin/env python3
"""
AI Search API Service
Provides vector search and LLM integration for Magento AI Search module
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import requests
import chromadb
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
CHROMA_URL = os.getenv('CHROMA_URL', 'http://chromadb:8000')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize ChromaDB client
try:
    chroma_client = chromadb.HttpClient(host='chromadb', port=8000)
    logger.info("Connected to ChromaDB")
except Exception as e:
    logger.error(f"Failed to connect to ChromaDB: {e}")
    chroma_client = None

class AISearchService:
    def __init__(self):
        self.collection_name = "magento_products"
        self.collection = None
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize or get the product collection"""
        if not chroma_client:
            return
        
        try:
            self.collection = chroma_client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Magento product embeddings for AI search"}
            )
            logger.info(f"Collection '{self.collection_name}' initialized")
        except Exception as e:
            logger.error(f"Failed to initialize collection: {e}")
    
    def add_products(self, products: List[Dict[str, Any]]) -> bool:
        """Add products to the vector database"""
        if not self.collection:
            return False
        
        try:
            documents = []
            metadatas = []
            ids = []
            
            for product in products:
                # Create searchable text from product data
                text = f"{product.get('name', '')} {product.get('description', '')} {product.get('categories', '')} {product.get('brand', '')}"
                documents.append(text)
                
                # Store metadata
                metadatas.append({
                    'name': product.get('name', ''),
                    'price': str(product.get('price', '')),
                    'sku': product.get('sku', ''),
                    'category': product.get('category', ''),
                    'brand': product.get('brand', ''),
                    'url': product.get('url', ''),
                    'image': product.get('image', '')
                })
                
                ids.append(str(product.get('id', product.get('sku', ''))))
            
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Added {len(products)} products to collection")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add products: {e}")
            return False
    
    def search_products(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for products using vector similarity"""
        if not self.collection:
            return []
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=limit
            )
            
            products = []
            if results['metadatas'] and results['metadatas'][0]:
                for i, metadata in enumerate(results['metadatas'][0]):
                    distance = results['distances'][0][i] if results['distances'] else 0
                    products.append({
                        'id': results['ids'][0][i],
                        'name': metadata.get('name', ''),
                        'price': metadata.get('price', ''),
                        'sku': metadata.get('sku', ''),
                        'category': metadata.get('category', ''),
                        'brand': metadata.get('brand', ''),
                        'url': metadata.get('url', ''),
                        'image': metadata.get('image', ''),
                        'relevance_score': 1 - distance  # Convert distance to similarity
                    })
            
            return products
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def generate_ai_response(self, query: str, products: List[Dict[str, Any]]) -> str:
        """Generate AI response using LLM"""
        if not products:
            return "I couldn't find any products matching your query. Could you try rephrasing your search?"
        
        # Prepare context for LLM
        context = "Found products:\n"
        for product in products[:5]:  # Limit to top 5 for context
            context += f"- {product['name']} (${product['price']}) - {product['category']}\n"
        
        prompt = f"""
        You are a helpful shopping assistant for an e-commerce store. A customer asked: "{query}"
        
        Based on these products I found:
        {context}
        
        Provide a helpful, conversational response that:
        1. Acknowledges their search
        2. Highlights the most relevant products
        3. Suggests alternatives if needed
        4. Keeps the tone friendly and helpful
        
        Response:
        """
        
        # Try OpenAI first, then Gemini as fallback
        if OPENAI_API_KEY and OPENAI_API_KEY != 'your_openai_api_key_here':
            response = self._call_openai(prompt)
            if response:
                return response
        elif GEMINI_API_KEY and GEMINI_API_KEY != 'your_gemini_api_key_here':
            response = self._call_gemini(prompt)
            if response:
                return response
        
        # Fallback to enhanced template response
        return self._generate_template_response(query, products)
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API"""
        try:
            headers = {
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 200,
                'temperature': 0.7
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                logger.error(f"OpenAI API error: {response.status_code}")
                return None  # Signal to use template response
                
        except Exception as e:
            logger.error(f"OpenAI call failed: {e}")
            return None  # Signal to use template response
    
    def _call_gemini(self, prompt: str) -> str:
        """Call Google Gemini API"""
        # Implement Gemini API call here
        return self._generate_template_response("", [])
    
    def _generate_template_response(self, query: str, products: List[Dict[str, Any]]) -> str:
        """Generate a template response when AI is not available"""
        if not products:
            return "I couldn't find any products matching your search. Could you try rephrasing or using different keywords?"
        
        # Create a more intelligent template response
        query_lower = query.lower()
        
        # Determine response style based on query
        if any(word in query_lower for word in ['show', 'find', 'looking for', 'need', 'want']):
            intro = f"I found {len(products)} great options for you:"
        elif any(word in query_lower for word in ['best', 'top', 'recommend']):
            intro = f"Here are my top {min(len(products), 3)} recommendations:"
        elif any(word in query_lower for word in ['cheap', 'budget', 'affordable']):
            intro = f"Here are some budget-friendly options I found:"
        else:
            intro = f"Based on your search for '{query}', here's what I found:"
        
        response = intro + "\n\n"
        
        # Format top 3 products with more detail
        for i, product in enumerate(products[:3], 1):
            category = product.get('category', '').split(',')[0]  # Get first category
            brand = product.get('brand', '')
            
            if brand and category:
                response += f"{i}. {product['name']} by {brand}\n   ${product['price']} - {category}\n\n"
            elif category:
                response += f"{i}. {product['name']}\n   ${product['price']} - {category}\n\n"
            else:
                response += f"{i}. {product['name']} - ${product['price']}\n\n"
        
        # Add helpful closing
        if len(products) > 3:
            response += f"Plus {len(products) - 3} more options available! "
        
        response += "Click on any product to learn more. Is there anything specific you'd like to know about these items?"
        
        return response

# Initialize the AI search service
ai_search = AISearchService()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'chroma_connected': chroma_client is not None,
        'openai_configured': OPENAI_API_KEY is not None,
        'gemini_configured': GEMINI_API_KEY is not None
    })

@app.route('/search', methods=['POST'])
def search():
    """Main search endpoint"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        limit = data.get('limit', 10)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Search for products
        products = ai_search.search_products(query, limit)
        
        # Generate AI response
        ai_response = ai_search.generate_ai_response(query, products)
        
        return jsonify({
            'query': query,
            'ai_response': ai_response,
            'products': products,
            'total_results': len(products)
        })
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({'error': 'Search failed'}), 500

@app.route('/add_products', methods=['POST'])
def add_products():
    """Add products to the vector database"""
    try:
        data = request.get_json()
        products = data.get('products', [])
        
        if not products:
            return jsonify({'error': 'Products array is required'}), 400
        
        success = ai_search.add_products(products)
        
        if success:
            return jsonify({
                'message': f'Successfully added {len(products)} products',
                'count': len(products)
            })
        else:
            return jsonify({'error': 'Failed to add products'}), 500
            
    except Exception as e:
        logger.error(f"Add products error: {e}")
        return jsonify({'error': 'Failed to add products'}), 500

@app.route('/collection_info', methods=['GET'])
def collection_info():
    """Get information about the product collection"""
    try:
        if not ai_search.collection:
            return jsonify({'error': 'Collection not available'}), 500
        
        count = ai_search.collection.count()
        
        return jsonify({
            'collection_name': ai_search.collection_name,
            'product_count': count,
            'status': 'active'
        })
        
    except Exception as e:
        logger.error(f"Collection info error: {e}")
        return jsonify({'error': 'Failed to get collection info'}), 500

if __name__ == '__main__':
    logger.info("Starting AI Search API service...")
    app.run(host='0.0.0.0', port=5000, debug=True)