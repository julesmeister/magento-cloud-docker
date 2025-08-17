@echo off
echo Starting Magento AI Search Development Environment (Simplified)
echo =============================================================
echo.

REM Set Docker path
set DOCKER_PATH="C:\Program Files\Docker\Docker\resources\bin\docker.exe"

REM Navigate to project directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

echo Checking Docker...
%DOCKER_PATH% --version
if %errorlevel% neq 0 (
    echo ERROR: Docker not accessible
    pause
    exit /b 1
)
echo.

echo Stopping any existing containers...
%DOCKER_PATH% compose down --remove-orphans

echo Starting services with docker-compose.yml...
%DOCKER_PATH% compose up -d
set DOCKER_EXIT_CODE=%errorlevel%

echo.
echo ================================================
echo Magento AI Search environment is starting up!
echo ================================================
echo.
echo Services:
%DOCKER_PATH% compose ps
echo.
echo Available services:
echo - Magento Web: http://localhost
echo - Database: localhost:3306 (magento2/magento2)
echo - Redis: localhost:6379
echo - Elasticsearch: http://localhost:9200
echo - ChromaDB (Vector DB): http://localhost:8000
echo - AI Search API: http://localhost:5000
echo - MailHog: http://localhost:8025
echo.
echo To stop: docker compose down
echo To view logs: docker compose logs -f [service_name]
echo.

if %DOCKER_EXIT_CODE% neq 0 (
    echo ERROR: Failed to start containers (Exit code: %DOCKER_EXIT_CODE%)
    echo Check the error messages above
) else (
    echo All services started successfully!
    echo.
    echo Opening Magento with AI Search...
    timeout /t 5 /nobreak >nul
    start http://localhost
)

pause