@echo off
echo Magento AI Search Module Setup
echo ==============================
echo.

REM Navigate to project directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

echo Setting up AI Search module...
echo.

REM Create additional required directories for the AI Search module
echo Creating module directories...
if not exist "app\code\Custom\AiSearch\Api" mkdir "app\code\Custom\AiSearch\Api"
if not exist "app\code\Custom\AiSearch\Api\Data" mkdir "app\code\Custom\AiSearch\Api\Data"
if not exist "app\code\Custom\AiSearch\Setup" mkdir "app\code\Custom\AiSearch\Setup"
if not exist "app\code\Custom\AiSearch\Observer" mkdir "app\code\Custom\AiSearch\Observer"
if not exist "app\code\Custom\AiSearch\Plugin" mkdir "app\code\Custom\AiSearch\Plugin"
if not exist "app\code\Custom\AiSearch\Service" mkdir "app\code\Custom\AiSearch\Service"
if not exist "app\code\Custom\AiSearch\view\adminhtml\templates" mkdir "app\code\Custom\AiSearch\view\adminhtml\templates"
if not exist "app\code\Custom\AiSearch\view\adminhtml\web\js" mkdir "app\code\Custom\AiSearch\view\adminhtml\web\js"

echo Module directories created successfully!
echo.

echo AI Search module structure:
echo ├── Api/                   # Interface definitions
echo ├── Api/Data/             # Data interface definitions  
echo ├── Block/                # View layer logic
echo ├── Controller/           # HTTP request handlers
echo ├── Helper/               # Utility classes
echo ├── Model/                # Business logic and data models
echo ├── Observer/             # Event observers
echo ├── Plugin/               # Plugin classes
echo ├── Service/              # Service layer classes
echo ├── Setup/                # Installation/upgrade scripts
echo ├── etc/                  # Configuration files
echo └── view/                 # Frontend and admin templates
echo     ├── adminhtml/        # Admin panel assets
echo     └── frontend/         # Frontend assets
echo.

echo Next steps:
echo 1. Run docker-run.bat to start the Magento environment
echo 2. Install Magento in the Docker container
echo 3. Enable the Custom_AiSearch module
echo 4. Configure AI API keys in admin panel
echo.

echo Module setup completed!
pause