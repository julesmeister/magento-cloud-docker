
# Magento AI Search

AI-powered search chatbot integration for Magento Community Edition using RAG (Retrieval-Augmented Generation) architecture with vector databases and LLM integration.

## Project Overview

This project integrates an AI-powered search chatbot into Magento Community Edition, replacing traditional search with conversational AI. The chatbot appears in the bottom-right corner of the e-commerce site and provides intelligent product search and recommendations.

## Architecture

- **RAG Architecture**: Retrieval-Augmented Generation for contextual responses
- **Vector Database**: ChromaDB for semantic search and embeddings
- **LLM Integration**: Support for OpenAI GPT and Google Gemini
- **Magento Module**: Custom_AiSearch module integrated into Magento core
- **Containerized**: Full Docker development environment

## Project Structure

```
magento-ai-search/
├── app/code/Custom/AiSearch/          # Magento AI Search Module
│   ├── registration.php               # Module registration
│   ├── etc/module.xml                 # Module configuration
│   └── ai_search_api.py              # Flask API service
├── docker/                           # Docker configuration
│   ├── magento-php/Dockerfile        # Custom PHP-FPM image
│   └── nginx/nginx.conf              # Nginx configuration
├── docker-compose.yml                # Multi-service setup
└── docker-run.bat                   # Windows startup script
```

## Quick Start

1. **Start Docker Environment**:
   ```bash
   # Windows
   docker-run.bat
   
   # Linux/Mac
   docker compose up -d
   ```

2. **Access Applications**:
   - **Magento Store**: http://localhost
   - **Magento Admin**: http://localhost/admin (admin/admin123)
   - **AI Search API**: http://localhost:5000
   - **ChromaDB**: http://localhost:8000
   - **Mailhog**: http://localhost:8025

## Components Status

### ✅ Completed
- [x] Magento Community Edition 2.4.6 installation
- [x] Custom_AiSearch module structure
- [x] Docker environment with all services
- [x] AI Search API with Flask and ChromaDB
- [x] Vector database integration
- [x] LLM framework (OpenAI/Gemini support)
- [x] Nginx configuration for Magento
- [x] Database and Redis setup
- [x] Developer mode configuration
- [x] Cache and permissions setup
- [x] Indexers configured
- [x] Static content deployment and versioning fixes
- [x] Customer account creation functionality
- [x] Password requirements optimization

### 🚧 In Development
- [ ] Frontend chatbot widget integration
- [ ] Product data indexing to vector database
- [ ] Search UI in Magento theme
- [ ] Admin panel for AI search configuration
- [ ] Search analytics and logging

### 📋 Planned Features
- [ ] Real-time product search suggestions
- [ ] Natural language query processing
- [ ] Product recommendation engine
- [ ] Multi-language support
- [ ] Search result personalization
- [ ] Performance optimization

## Technical Details

### Services Architecture

| Service | Port | Description |
|---------|------|-------------|
| nginx | 80, 443 | Web server for Magento |
| php-fpm | 9000 | PHP processor with Magento extensions |
| mariadb | 3306 | Database server |
| redis | 6379 | Cache and session storage |
| elasticsearch | 9200 | Search engine for Magento |
| chromadb | 8000 | Vector database for AI search |
| ai-search-api | 5000 | Flask API for AI search functionality |
| mailhog | 1025, 8025 | Email testing service |

### Development Environment

- **Magento Version**: Community Edition 2.4.6
- **PHP Version**: 8.2-FPM with required extensions
- **Database**: MariaDB 10.6
- **Search Engine**: Elasticsearch 7.17.9
- **Vector DB**: ChromaDB latest
- **Container Orchestration**: Docker Compose

## Troubleshooting

### Common Issues

**Customer Account Creation Problems:**
- Password strength indicator shows "No Password"
- Account creation button is slow or refreshes page

**Solutions Applied:**
1. **Static file versioning disabled** - Prevents 404 errors on JS/CSS files
2. **Static content force-deployed** - All frontend assets properly generated
3. **Developer mode enabled** - Auto-generation of missing files
4. **Password requirements reduced** - Minimum 6 characters, 1 character class only
5. **Cache and permissions optimized** - All directories writable by www-data

**Current Status:**
- ✅ Customer account creation working
- ✅ Password validation functional
- ✅ JavaScript/CSS loading properly
- ✅ Form submissions working correctly

## Next Steps

1. **Frontend Integration**: Implement chatbot widget in Magento theme
2. **Product Indexing**: Sync Magento catalog with ChromaDB
3. **Search Enhancement**: Natural language processing for queries
4. **Admin Configuration**: Management interface for AI search settings
5. **Performance Optimization**: Caching and response time improvements

### Maintainers

We encourage experts from the Community to help us with GitHub routines such as accepting, merging, or rejecting pull requests and reviewing issues. Adobe has granted the Community Maintainers permission to accept, merge, and reject pull requests, as well as review issues. Thanks to invaluable input from the Community Maintainers team, we can significantly improve contribution quality and accelerate the time to deliver your updates to production. 

- [Learn more about the Maintainer role](https://devdocs.magento.com/contributor-guide/maintainers.html)
- [Maintainer's Handbook](https://devdocs.magento.com/contributor-guide/maintainer-handbook.html)

[![](https://raw.githubusercontent.com/wiki/magento/magento2/images/maintainers.png)](https://magento.com/magento-contributors#maintainers)

### Leaders

Adobe highly appreciates contributions that help us to improve the code, clarify the documentation, and increase test coverage. Check out our Community leaders, superstars, and superheroes on the [leaderboard](https://magento.biterg.io/app/kibana#/dashboard/41dc0c60-fa06-11eb-bbaa-dd6ca6f8fda8?_g=()).

[![](https://raw.githubusercontent.com/wiki/magento/magento2/images/contributors.png)](https://magento.com/magento-contributors)

### Labeling

We use labels in the GitHub issues and pull requests to help the participants retrieve additional information such as progress, component assignments, or release lines.

- [Labels applied by the Community Engineering team](https://devdocs.magento.com/contributor-guide/contributing.html#labels)

## Security

[Security](https://devdocs.magento.com/guides/v2.4/architecture/security_intro.html) is one of the highest priorities at Adobe. To learn more about reporting security concerns, visit the [Adobe Bug Bounty Program](https://hackerone.com/adobe).

Stay up-to-date on the latest security news and patches by signing up for [Security Alert Notifications](https://magento.com/security/sign-up).

## Licensing

Each Magento source file included in this distribution is licensed under OSL 3.0 or the terms and conditions of the applicable ordering document between Licensee/Customer and Adobe (or Magento).
 
[Open Software License (OSL 3.0)](https://opensource.org/licenses/osl-3.0.php) – Please see [LICENSE.txt](LICENSE.txt) for the full text of the OSL 3.0 license.
 
Subject to Licensee's/Customer's payment of fees and compliance with the terms and conditions of the applicable ordering document between Licensee/Customer and Adobe (or Magento), the terms and conditions of the applicable ordering between Licensee/Customer and Adobe (or Magento) supersede the OSL 3.0 license for each source file.

## Communications

We are dedicated to our Community and encourage your contributions and welcome feedback through [events](https://www.adobe.io/open/magento/calendar), our [DevBlog](https://community.magento.com/t5/Magento-DevBlog/bg-p/devblog), Twitter and YouTube channels, and [other Community resources](https://devdocs.magento.com/community/resources.html).

To connect with people from the Community and Adobe engineering, [join us in Slack](https://magentocommeng.slack.com). We have a channel for every project. To join a particular channel, send us a request at [engcom@adobe.com](mailto:engcom@adobe.com), or [sign up](https://opensource.magento.com/slack).

- [Popular Slack channels](https://www.adobe.io/open/magento/slack)

If you are a new Community member, check out the following channels:

- [general](https://magentocommeng.slack.com/archives/C4YS78WE6) is an open chat for introductions and Magento 2 questions
- [github](https://magentocommeng.slack.com/archives/C7KB93M32) is a support channel for GitHub issues, pull requests, and processes
- [public-backlog](https://magentocommeng.slack.com/archives/CCV3J3RV5) for discussions of the backlog
