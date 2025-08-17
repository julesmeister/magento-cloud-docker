<?php
namespace Custom\AiSearch\Console\Command;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Magento\Catalog\Model\ResourceModel\Product\CollectionFactory;
use Magento\Catalog\Helper\Image;
use Magento\Store\Model\StoreManagerInterface;
use Magento\Framework\App\Area;
use Magento\Framework\App\State;

class IndexProducts extends Command
{
    private $productCollectionFactory;
    private $imageHelper;
    private $storeManager;
    private $appState;

    public function __construct(
        CollectionFactory $productCollectionFactory,
        Image $imageHelper,
        StoreManagerInterface $storeManager,
        State $appState
    ) {
        $this->productCollectionFactory = $productCollectionFactory;
        $this->imageHelper = $imageHelper;
        $this->storeManager = $storeManager;
        $this->appState = $appState;
        parent::__construct();
    }

    protected function configure()
    {
        $this->setName('aisearch:index:products')
             ->setDescription('Index Magento products into ChromaDB for AI search');
    }

    protected function execute(InputInterface $input, OutputInterface $output)
    {
        try {
            $this->appState->setAreaCode(Area::AREA_FRONTEND);
        } catch (\Exception $e) {
            // Area already set
        }

        $output->writeln('<info>Starting product indexing...</info>');

        // Get all enabled products
        $collection = $this->productCollectionFactory->create();
        $collection->addAttributeToSelect('*')
                  ->addAttributeToFilter('status', 1) // Only enabled products
                  ->addAttributeToFilter('visibility', ['neq' => 1]) // Exclude not visible individually
                  ->setPageSize(100); // Process in batches

        $totalProducts = $collection->getSize();
        $output->writeln("<info>Found {$totalProducts} products to index</info>");

        $products = [];
        $processed = 0;
        
        foreach ($collection as $product) {
            try {
                $productData = [
                    'id' => $product->getId(),
                    'sku' => $product->getSku(),
                    'name' => $product->getName(),
                    'description' => strip_tags($product->getDescription() ?: $product->getShortDescription()),
                    'price' => number_format((float)$product->getPrice(), 2),
                    'category' => $this->getProductCategories($product),
                    'brand' => $product->getManufacturer() ?: $product->getBrand() ?: '',
                    'url' => $product->getProductUrl(),
                    'image' => $this->getProductImageUrl($product)
                ];

                $products[] = $productData;
                $processed++;

                // Send in batches of 50
                if (count($products) >= 50) {
                    $this->sendToApi($products, $output);
                    $products = [];
                }

                if ($processed % 100 == 0) {
                    $output->writeln("<info>Processed {$processed}/{$totalProducts} products</info>");
                }

            } catch (\Exception $e) {
                $output->writeln("<error>Error processing product {$product->getSku()}: {$e->getMessage()}</error>");
            }
        }

        // Send remaining products
        if (!empty($products)) {
            $this->sendToApi($products, $output);
        }

        $output->writeln("<info>Product indexing completed. Processed {$processed} products.</info>");
        return 0;
    }

    private function getProductCategories($product)
    {
        $categories = [];
        foreach ($product->getCategoryIds() as $categoryId) {
            try {
                $category = $this->storeManager->getStore()->getModel('Magento\Catalog\Model\Category')->load($categoryId);
                if ($category->getName()) {
                    $categories[] = $category->getName();
                }
            } catch (\Exception $e) {
                // Skip this category
            }
        }
        return implode(', ', $categories);
    }

    private function getProductImageUrl($product)
    {
        try {
            return $this->imageHelper->init($product, 'product_thumbnail_image')->getUrl();
        } catch (\Exception $e) {
            return '';
        }
    }

    private function sendToApi($products, $output)
    {
        try {
            $apiUrl = 'http://localhost:5000/add_products';
            
            $data = json_encode(['products' => $products]);
            
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $apiUrl);
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
            curl_setopt($ch, CURLOPT_HTTPHEADER, [
                'Content-Type: application/json',
                'Content-Length: ' . strlen($data)
            ]);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLOPT_TIMEOUT, 30);
            
            $response = curl_exec($ch);
            $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
            
            if (curl_errno($ch)) {
                throw new \Exception('Curl error: ' . curl_error($ch));
            }
            
            curl_close($ch);
            
            if ($httpCode !== 200) {
                throw new \Exception("API returned HTTP {$httpCode}: {$response}");
            }
            
            $result = json_decode($response, true);
            if (isset($result['message'])) {
                $output->writeln("<info>✓ " . $result['message'] . "</info>");
            }
            
        } catch (\Exception $e) {
            $output->writeln("<error>Failed to send products to API: {$e->getMessage()}</error>");
        }
    }
}