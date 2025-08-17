<?php
/**
 * AI Search Module Registration
 * 
 * This module provides AI-powered search functionality using RAG architecture
 * with vector database and LLM integration for intelligent product search.
 */

use Magento\Framework\Component\ComponentRegistrar;

ComponentRegistrar::register(
    ComponentRegistrar::MODULE,
    'Custom_AiSearch',
    __DIR__
);