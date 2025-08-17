<?php
namespace Custom\AiSearch\Block;

use Magento\Framework\View\Element\Template;

class Chat extends Template
{
    /**
     * Get the AI Search API endpoint URL
     */
    public function getApiUrl()
    {
        return 'http://localhost:5000';
    }
    
    /**
     * Check if AI Search is enabled
     */
    public function isEnabled()
    {
        return true; // For now always enabled
    }
    
    /**
     * Get configuration for the chat widget
     */
    public function getChatConfig()
    {
        return [
            'apiUrl' => $this->getApiUrl(),
            'enabled' => $this->isEnabled(),
            'placeholder' => 'Ask me about products...',
            'title' => 'AI Shopping Assistant'
        ];
    }
}