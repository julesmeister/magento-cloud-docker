# Custom AI Search Module

## Overview
This Magento module provides AI-powered search functionality that replaces traditional keyword-based search with intelligent conversational search using Large Language Models (LLM) and Retrieval-Augmented Generation (RAG) architecture.

## Features
- **Conversational Search**: Natural language queries for product discovery
- **Vector Database Integration**: Semantic search using product embeddings
- **LLM Integration**: Support for OpenAI GPT and Google Gemini APIs
- **Real-time Chat Interface**: Interactive search experience
- **Context Understanding**: Maintains conversation history for better results
- **Product Recommendations**: AI-powered suggestions based on user intent

## Architecture
- **RAG (Retrieval-Augmented Generation)**: Combines vector search with LLM generation
- **MCP Architecture**: Modular, scalable design
- **Vector Database**: Stores product embeddings for semantic search
- **API Integration**: RESTful endpoints for frontend communication

## Module Structure
```
Custom/AiSearch/
├── Block/                 # View layer logic
├── Controller/            # HTTP request handlers
├── Helper/               # Utility classes
├── Model/                # Business logic and data models
├── etc/                  # Configuration files
└── view/frontend/        # Frontend assets and templates
    ├── templates/        # Phtml templates
    └── web/js/          # JavaScript components
```

## Installation
1. Place module in `app/code/Custom/AiSearch/`
2. Run `php bin/magento module:enable Custom_AiSearch`
3. Run `php bin/magento setup:upgrade`
4. Configure API keys in admin panel

## Configuration
- Set up LLM API credentials (OpenAI/Gemini)
- Configure vector database connection
- Customize search interface appearance
- Set conversation flow parameters

## Usage
The module adds an AI-powered search widget that can replace the default Magento search bar, providing customers with an intelligent conversational search experience.