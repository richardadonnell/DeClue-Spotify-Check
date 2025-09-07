<!-- markdownlint-disable-file -->
# Task Details: Docker Deployment for Coolify VPS

## Research Reference

**Source Research**: #file:../research/20250907-docker-coolify-deployment-research.md

## Phase 1: Create Docker Configuration

### Task 1.1: Create optimized multi-stage Dockerfile

Create a production-ready multi-stage Dockerfile optimized for Coolify deployment:

- **Files**:
  - `Dockerfile` - Multi-stage build configuration
  - `requirements.txt` - Python dependencies (already exists)

- **Success**:
  - Dockerfile uses Python 3.11-slim base image for security and size
  - Multi-stage build separates build and runtime stages
  - Dependencies installed in build stage, copied to runtime stage
  - Non-root user created for security
  - Proper working directory and file permissions set
  - CMD uses exec form for proper signal handling

- **Research References**:
  - #file:../research/20250907-docker-coolify-deployment-research.md (Lines 78-95) - Complete Dockerfile example
  - #fetch:https://docs.docker.com/develop/dev-best-practices/ - Docker best practices
  - #fetch:https://docs.docker.com/language/python/ - Python-specific Docker guidelines

- **Dependencies**:
  - Python 3.9+ runtime environment
  - requirements.txt with minimal dependencies

### Task 1.2: Create docker-compose.yml for Coolify

Develop docker-compose.yml configuration for Coolify deployment:

- **Files**:
  - `docker-compose.yml` - Service definition and configuration
  - `.env.example` - Environment variable template (already exists)

- **Success**:
  - Service uses build context with Dockerfile
  - All environment variables properly defined
  - Named volumes configured for persistent data
  - Restart policy set to unless-stopped
  - Health check configured for container monitoring
  - No port mappings (Coolify handles networking)

- **Research References**:
  - #file:../research/20250907-docker-coolify-deployment-research.md (Lines 97-120) - Complete docker-compose.yml example
  - #githubRepo:"coollabsio/coolify docker python" - Coolify Docker patterns
  - #fetch:https://coolify.io/docs - Coolify deployment documentation

- **Dependencies**:
  - Dockerfile from Task 1.1
  - Environment variable definitions

### Task 1.3: Create .dockerignore file

Create .dockerignore to optimize build context and security:

- **Files**:
  - `.dockerignore` - Build context exclusions

- **Success**:
  - Excludes virtual environment (env/)
  - Excludes logs and temporary files
  - Excludes Git repository data
  - Excludes sensitive files (.env)
  - Excludes development files
  - Minimizes build context size

- **Research References**:
  - #fetch:https://docs.docker.com/develop/dev-best-practices/#exclude-with-dockerignore - Docker ignore best practices
  - #file:../research/20250907-docker-coolify-deployment-research.md (Lines 1-30) - Project file analysis

- **Dependencies**:
  - Project file structure analysis

## Phase 2: Environment and Configuration

### Task 2.1: Update environment variable handling for containers

Ensure environment variables work correctly in containerized environment:

- **Files**:
  - `main.py` - Python application (already exists)
  - `.env.example` - Environment template (already exists)

- **Success**:
  - All environment variables properly loaded via python-dotenv
  - Default values handled for optional variables
  - Error handling for missing required variables
  - Logging configuration works in container
  - File paths use container-appropriate locations

- **Research References**:
  - #file:../research/20250907-docker-coolify-deployment-research.md (Lines 1-30) - Environment variable analysis
  - #githubRepo:"coollabsio/coolify docker python" - Environment variable patterns

- **Dependencies**:
  - Existing main.py with environment variable usage
  - Environment variable definitions

### Task 2.2: Configure persistent volume mounts

Set up proper volume mounting for data persistence:

- **Files**:
  - `docker-compose.yml` - Volume configuration
  - `main.py` - File path handling

- **Success**:
  - last_episodes.json stored in persistent volume
  - debug.log and cron.log stored in persistent volume
  - Volume mounts configured in docker-compose.yml
  - Application creates necessary directories
  - File permissions appropriate for container user

- **Research References**:
  - #file:../research/20250907-docker-coolify-deployment-research.md (Lines 97-120) - Volume mounting examples
  - #githubRepo:"coollabsio/coolify docker python" - Coolify volume patterns

- **Dependencies**:
  - docker-compose.yml from Task 1.2
  - File I/O operations in main.py

### Task 2.3: Add health check configuration

Implement health checks for container monitoring:

- **Files**:
  - `docker-compose.yml` - Health check configuration
  - `main.py` - Health check endpoint (optional)

- **Success**:
  - Health check command tests Python execution
  - Appropriate intervals and timeouts configured
  - Health check doesn't interfere with application logic
  - Coolify can monitor container health
  - Failed health checks trigger appropriate actions

- **Research References**:
  - #file:../research/20250907-docker-coolify-deployment-research.md (Lines 116-118) - Health check example
  - #githubRepo:"coollabsio/coolify docker python" - Health check patterns

- **Dependencies**:
  - docker-compose.yml from Task 1.2
  - Python application functionality

## Phase 3: Coolify Integration

### Task 3.1: Prepare deployment documentation

Create comprehensive deployment guide for Coolify:

- **Files**:
  - `README-Docker.md` - Docker deployment instructions
  - `COOLIFY-DEPLOYMENT.md` - Coolify-specific setup guide

- **Success**:
  - Step-by-step deployment instructions
  - Environment variable configuration guide
  - Cron scheduling setup instructions
  - Troubleshooting common issues
  - Migration from existing cron setup

- **Research References**:
  - #file:../research/20250907-docker-coolify-deployment-research.md (Lines 139-155) - Implementation guidance
  - #fetch:https://coolify.io/docs - Coolify deployment documentation

- **Dependencies**:
  - All Docker configuration files
  - Environment setup knowledge

### Task 3.2: Create Coolify environment setup guide

Document Coolify dashboard configuration:

- **Files**:
  - `COOLIFY-ENVIRONMENT.md` - Environment setup guide
  - `COOLIFY-CRON.md` - Cron scheduling guide

- **Success**:
  - Environment variable setup in Coolify UI
  - Secret management for sensitive data
  - Cron job configuration through Coolify
  - Volume configuration for persistent data
  - Domain and SSL certificate setup

- **Research References**:
  - #githubRepo:"coollabsio/coolify docker python" - Coolify configuration patterns
  - #fetch:https://coolify.io/docs - Coolify environment management

- **Dependencies**:
  - Coolify platform knowledge
  - Environment variable requirements

### Task 3.3: Document cron scheduling migration

Create migration guide from system cron to Coolify scheduling:

- **Files**:
  - `CRON-MIGRATION.md` - Migration documentation
  - `run_script.sh` - Archive current script

- **Success**:
  - Clear migration steps from crontab to Coolify
  - Backup procedures for existing data
  - Testing procedures for new setup
  - Rollback procedures if needed
  - Monitoring and alerting setup

- **Research References**:
  - #file:../research/20250907-docker-coolify-deployment-research.md (Lines 139-155) - Cron scheduling guidance
  - #fetch:https://coolify.io/docs - Coolify cron scheduling

- **Dependencies**:
  - Current cron setup understanding
  - Coolify scheduling capabilities

## Dependencies

- Docker runtime environment
- Coolify VPS platform access
- Python 3.9+ base image availability
- Network access for Spotify API and webhooks
- SMTP server access for error notifications

## Success Criteria

- Application successfully builds and runs in Docker container
- All environment variables properly configured through Coolify
- Persistent data storage working for state files and logs
- Coolify cron scheduling replaces system cron functionality
- Health checks pass and container monitoring works
- Webhook notifications and email alerts function correctly
