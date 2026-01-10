---
name: ec2-backend-deployer
description: Expert in deploying backends to EC2 instances using CI/CD pipelines, Docker containers, and GitHub Actions. This skill guides through the complete deployment workflow including Docker image building, container registry management, Tailscale integration, and automated deployment to EC2. Activates when users need to deploy backend services to EC2.
---

# EC2 Backend Deployer

You are an expert in deploying backend applications to EC2 instances using CI/CD pipelines, Docker containers, and GitHub Actions. This skill provides comprehensive guidance for setting up automated deployments from GitHub to EC2, including Docker image building, container registry management, secure access via Tailscale, and service orchestration.

## When to Use This Skill

This skill activates automatically when you're:

- Setting up CI/CD for backend deployment to EC2
- Configuring Docker-based deployments
- Implementing automated deployment pipelines
- Deploying NestJS, Next.js, or Express backends to EC2
- Setting up container registries and image management
- Configuring secure EC2 access for deployments
- Implementing health checks and deployment verification
- Setting up multi-service deployments with dependencies

## Project Context Discovery

**Before deploying, discover the project's context:**

1. **Identify Project Type:**
   - Scan for `package.json` to detect framework (NestJS, Next.js, Express)
   - Check for `nest-cli.json` (NestJS)
   - Check for `next.config.js` (Next.js)
   - Check for monorepo structure (workspaces)

2. **Check Existing Setup:**
   - Look for existing Dockerfiles
   - Check for docker-compose files
   - Review existing GitHub Actions workflows
   - Check for deployment scripts
   - Verify environment configuration files

3. **Identify Infrastructure:**
   - Check for EC2 instance details
   - Verify Tailscale setup (if using secure access)
   - Check for container registry configuration
   - Review security group and network setup

4. **Use Project-Specific Skills:**
   - Check for `[project]-ec2-backend-deployer` skill
   - Review project-specific deployment patterns
   - Follow project's infrastructure standards

## Docker Setup

### Multi-Stage Dockerfile Pattern

**Recommended structure for production deployments:**

```dockerfile
# ==================================================
# Stage 1: Base - Install dependencies
# ==================================================
FROM node:22.17.0 AS base

# Install bun (or use npm if preferred)
RUN curl -fsSL https://bun.sh/install | bash && \
    cp /root/.bun/bin/bun /usr/local/bin/bun && \
    chmod +x /usr/local/bin/bun
ENV PATH="/usr/local/bin:${PATH}"

# Set memory limits for builds
ENV NODE_OPTIONS=--max-old-space-size=4096

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Copy package files
COPY package.json package-lock.json* bun.lockb* ./
COPY .npmrc ./

# For monorepos: create workspace structure
RUN mkdir -p apps libs

# Install dependencies with secrets for private packages
RUN --mount=type=secret,id=NPM_TOKEN \
    export NPM_TOKEN=$(cat /run/secrets/NPM_TOKEN 2>/dev/null || echo "") && \
    npm ci --frozen-lockfile || bun install --frozen-lockfile

# ==================================================
# Stage 2: Builder - Build application
# ==================================================
FROM base AS builder

# Copy source code
COPY . .

# Build application (with build secrets if needed)
RUN --mount=type=secret,id=SENTRY_AUTH_TOKEN \
    export SENTRY_AUTH_TOKEN=$(cat /run/secrets/SENTRY_AUTH_TOKEN 2>/dev/null || echo "") && \
    npm run build:prod || bun run build:prod

# ==================================================
# Stage 3: Production - Runtime image
# ==================================================
FROM node:22.17.0-slim AS production

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    bash \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Copy built artifacts and production dependencies
COPY --from=builder /usr/src/app/dist ./dist
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY --from=builder /usr/src/app/package.json ./package.json
COPY --from=builder /usr/src/app/public ./public

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -u 1001 appuser

# Set permissions
RUN chown -R appuser:appuser /usr/src/app

# Switch to non-root user
USER appuser

# Expose application port
EXPOSE 3001

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:3001/v1/health || exit 1

# Start application
CMD ["node", "dist/main.js"]
```

**For NestJS specifically:**

```dockerfile
# Use the pattern above but adjust:
# - Build command: npm run build (creates dist/)
# - Start command: node dist/main.js
# - Health endpoint: /v1/health or /health
```

**For Next.js API routes:**

```dockerfile
# Adjust for Next.js:
# - Build command: npm run build
# - Start command: npm start
# - Health endpoint: /api/health
```

### Dockerfile Best Practices

- **Multi-stage builds**: Reduce final image size
- **Non-root user**: Run containers as non-root for security
- **Health checks**: Include HEALTHCHECK in Dockerfile
- **Build secrets**: Use BuildKit secrets for sensitive data
- **Layer caching**: Order COPY commands to maximize cache hits
- **System dependencies**: Install only what's needed in production stage

## Container Registry Setup

### GitHub Container Registry (ghcr.io) - Recommended

**Advantages:**
- Integrated with GitHub
- Free for public repos, included with GitHub plans
- Automatic authentication via GitHub tokens
- Image versioning with tags

**Setup:**

1. **Enable GitHub Container Registry:**
   - Go to repository Settings → Packages
   - Container registry is automatically enabled

2. **Image Naming Convention:**
   ```
   ghcr.io/[owner]/[service-name]:[tag]
   ```

3. **Image Tagging Strategy:**
   - `latest` - Most recent deployment
   - `production` - Production deployments
   - `[branch]-[sha]` - Branch and commit SHA
   - `[version]` - Semantic versioning

**Authentication in GitHub Actions:**

```yaml
- name: Log in to Container Registry
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

**Authentication on EC2:**

```bash
# Login to registry
echo "$GITHUB_TOKEN" | docker login ghcr.io -u USERNAME --password-stdin
```

### AWS ECR (Alternative)

**Setup:**

1. **Create ECR Repository:**
   ```bash
   aws ecr create-repository --repository-name [service-name]
   ```

2. **Get Login Token:**
   ```bash
   aws ecr get-login-password --region [region] | \
     docker login --username AWS --password-stdin [account-id].dkr.ecr.[region].amazonaws.com
   ```

3. **Push Image:**
   ```bash
   docker tag [image]:[tag] [account-id].dkr.ecr.[region].amazonaws.com/[service-name]:[tag]
   docker push [account-id].dkr.ecr.[region].amazonaws.com/[service-name]:[tag]
   ```

### Docker Hub (Alternative)

**Setup:**

```yaml
- name: Log in to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKER_USERNAME }}
    password: ${{ secrets.DOCKER_PASSWORD }}
```

## CI/CD Pipeline (GitHub Actions)

### Main Deployment Workflow

**File:** `.github/workflows/deploy-production.yml`

```yaml
name: Deploy Production

on:
  push:
    branches: [master]
    paths:
      - 'apps/**'
      - 'libs/**'
      - 'package.json'
      - 'Dockerfile*'
      - 'docker/**'
  workflow_dispatch:
    branches: [master]
    inputs:
      skip_tests:
        description: 'Skip pre-deployment tests'
        required: false
        default: false
        type: boolean

env:
  REGISTRY: ghcr.io
  IMAGE_PREFIX: ${{ github.repository_owner }}/[service-name]

jobs:
  # Branch safety check
  branch-check:
    name: Branch Safety Check
    runs-on: ubuntu-latest
    steps:
      - name: Verify master branch
        run: |
          if [ "${{ github.ref_name }}" != "master" ]; then
            echo "❌ ERROR: Production deployment can only run from master branch"
            exit 1
          fi

  # Pre-deployment checks
  pre-deployment-checks:
    name: Pre-Deployment Checks
    runs-on: ubuntu-latest
    needs: [branch-check]
    if: inputs.skip_tests != true
    steps:
      - name: Checkout code
        uses: actions/checkout@v5

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint
        continue-on-error: true

      - name: Run tests
        run: npm test
        continue-on-error: true

  # Build and push image
  build-image:
    name: Build and Push Image
    needs: [branch-check, pre-deployment-checks]
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v5

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}
          tags: |
            type=sha,prefix={{branch}}-
            type=raw,value=latest
            type=raw,value=production

      - name: Build and push image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}:buildcache
          cache-to: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}:buildcache,mode=max
          secrets: |
            NPM_TOKEN=${{ secrets.NPM_TOKEN }}
            SENTRY_AUTH_TOKEN=${{ secrets.SENTRY_AUTH_TOKEN }}
          platforms: linux/amd64

  # Deploy to EC2
  deploy:
    name: Deploy to EC2
    needs: [build-image]
    runs-on: ubuntu-latest
    steps:
      - name: Setup Tailscale
        uses: tailscale/github-action@v2
        with:
          oauth-client-id: ${{ secrets.TAILSCALE_CLIENT_ID }}
          oauth-secret: ${{ secrets.TAILSCALE_CLIENT_SECRET }}
          tags: tag:ci

      - name: Verify Tailscale connectivity
        run: |
          echo "⏳ Waiting for Tailscale to connect..."
          timeout 30 bash -c 'until tailscale status >/dev/null 2>&1; do sleep 1; done'
          echo "✅ Tailscale connected"

      - name: Deploy to instance
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ vars.TAILSCALE_INSTANCE_IP || secrets.EC2_IP }}
          username: ${{ secrets.EC2_USER }}
          key: ${{ secrets.EC2_SSH_KEY }}
          port: 22
          script: |
            set -euo pipefail

            echo "🔐 Logging into container registry..."
            echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin

            cd ~/[project-path] || mkdir -p ~/[project-path] && cd ~/[project-path]

            # Verify Docker Compose v2
            if ! docker compose version &>/dev/null; then
              echo "❌ ERROR: Docker Compose v2 is not installed"
              exit 1
            fi

            # Update docker-compose file
            cat > docker-compose.yml << 'EOF'
            version: '3.8'
            services:
              api:
                image: ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}:latest
                restart: unless-stopped
                ports:
                  - '3001:3001'
                env_file:
                  - .env.production
                healthcheck:
                  test: ['CMD', 'curl', '-f', 'http://localhost:3001/v1/health']
                  interval: 30s
                  timeout: 10s
                  retries: 5
                  start_period: 40s
            EOF

            # Pull latest images
            docker compose pull

            # Deploy
            docker compose up -d --force-recreate

            # Wait for health check
            echo "🏥 Waiting for service to be healthy..."
            sleep 10
            for i in {1..60}; do
              STATUS=$(docker inspect --format='{{.State.Health.Status}}' [container-name] 2>/dev/null || echo "none")
              if [ "$STATUS" = "healthy" ]; then
                echo "✅ Service is healthy"
                break
              fi
              if [ $i -eq 60 ]; then
                echo "❌ Service failed to become healthy"
                docker compose logs --tail=50
                exit 1
              fi
              echo "Waiting for service... ($i/60) [status: $STATUS]"
              sleep 3
            done

            echo "✅ Deployment complete!"
```

### Reusable Deployment Workflow

**File:** `.github/workflows/_deploy-service.yml`

For projects with multiple services, create a reusable workflow:

```yaml
name: Deploy Service (Reusable)

on:
  workflow_call:
    inputs:
      service_name:
        required: true
        type: string
      instance_ip:
        required: true
        type: string
      docker_compose_file:
        required: true
        type: string
      health_check_services:
        required: false
        type: string
        default: ''
    secrets:
      TAILSCALE_CLIENT_ID:
        required: true
      TAILSCALE_CLIENT_SECRET:
        required: true
      EC2_USER:
        required: true
      EC2_SSH_KEY:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Setup Tailscale
        uses: tailscale/github-action@v2
        with:
          oauth-client-id: ${{ secrets.TAILSCALE_CLIENT_ID }}
          oauth-secret: ${{ secrets.TAILSCALE_CLIENT_SECRET }}
          tags: tag:ci

      - name: Deploy to instance
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ inputs.instance_ip }}
          username: ${{ secrets.EC2_USER }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            # Deployment script (same as above)
```

## EC2 Deployment Process

### Tailscale Integration (Recommended)

**Why Tailscale:**
- Secure access without public IPs
- No need to manage security groups for SSH
- Easy connectivity from CI/CD runners
- Works across networks

**Setup:**

1. **Install Tailscale on EC2:**
   ```bash
   curl -fsSL https://tailscale.com/install.sh | sh
   sudo tailscale up
   ```

2. **Get Tailscale IP:**
   ```bash
   tailscale ip -4
   ```

3. **Configure GitHub Secrets:**
   - `TAILSCALE_CLIENT_ID` - OAuth client ID from Tailscale
   - `TAILSCALE_CLIENT_SECRET` - OAuth client secret
   - `TAILSCALE_INSTANCE_IP` - Tailscale IP of EC2 instance

4. **Use in GitHub Actions:**
   ```yaml
   - name: Setup Tailscale
     uses: tailscale/github-action@v2
     with:
       oauth-client-id: ${{ secrets.TAILSCALE_CLIENT_ID }}
       oauth-secret: ${{ secrets.TAILSCALE_CLIENT_SECRET }}
       tags: tag:ci
   ```

### SSH Configuration (Alternative)

If not using Tailscale, use direct SSH:

**GitHub Secrets Required:**
- `EC2_USER` - SSH username (e.g., `ubuntu`, `ec2-user`)
- `EC2_SSH_KEY` - Private SSH key
- `EC2_IP` - Public IP or hostname

**Security Group Configuration:**
- Allow SSH (port 22) from GitHub Actions IPs
- Or use a bastion host for additional security

### Docker Compose Deployment

**Requirements on EC2:**
- Docker installed
- Docker Compose v2 (not v1)
- Sufficient disk space
- Network access to container registry

**Deployment Steps:**

1. **SSH to EC2 instance**

2. **Login to container registry:**
   ```bash
   echo "$GITHUB_TOKEN" | docker login ghcr.io -u USERNAME --password-stdin
   ```

3. **Create/update docker-compose.yml:**
   ```yaml
   version: '3.8'
   services:
     api:
       image: ghcr.io/owner/service:latest
       restart: unless-stopped
       ports:
         - '3001:3001'
       env_file:
         - .env.production
       healthcheck:
         test: ['CMD', 'curl', '-f', 'http://localhost:3001/v1/health']
         interval: 30s
         timeout: 10s
         retries: 5
         start_period: 40s
   ```

4. **Pull latest images:**
   ```bash
   docker compose pull
   ```

5. **Deploy services:**
   ```bash
   docker compose up -d --force-recreate
   ```

6. **Verify health:**
   ```bash
   docker compose ps
   docker inspect --format='{{.State.Health.Status}}' [container-name]
   ```

### Multi-Service Deployment

**Deployment Order:**
1. Dependencies first (Redis, databases)
2. Independent services
3. Dependent services (API)

**Example with Redis:**

```yaml
services:
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    ports:
      - '6379:6379'
    healthcheck:
      test: ['CMD', 'redis-cli', 'ping']
      interval: 30s
      timeout: 3s
      retries: 5

  api:
    image: ghcr.io/owner/api:latest
    depends_on:
      redis:
        condition: service_healthy
    environment:
      - REDIS_URL=redis://redis:6379
```

## Security Best Practices

### GitHub Secrets Management

**Required Secrets:**
- `TAILSCALE_CLIENT_ID` / `TAILSCALE_CLIENT_SECRET` - For Tailscale access
- `EC2_USER` / `EC2_SSH_KEY` - For SSH access (if not using Tailscale)
- `NPM_TOKEN` - For private npm packages
- `SENTRY_AUTH_TOKEN` - For Sentry source maps (if using)
- `GITHUB_TOKEN` - Automatically provided, for registry access

**Setting Secrets:**
1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add each secret with appropriate values

### Build Secrets in Docker

**Use BuildKit secrets for sensitive build-time data:**

```dockerfile
RUN --mount=type=secret,id=NPM_TOKEN \
    export NPM_TOKEN=$(cat /run/secrets/NPM_TOKEN 2>/dev/null || echo "") && \
    npm ci
```

**In GitHub Actions:**
```yaml
secrets: |
  NPM_TOKEN=${{ secrets.NPM_TOKEN }}
  SENTRY_AUTH_TOKEN=${{ secrets.SENTRY_AUTH_TOKEN }}
```

### Container Security

- **Non-root user**: Always run containers as non-root
- **Minimal base images**: Use `-slim` or `-alpine` variants
- **No secrets in images**: Use environment variables or secrets management
- **Health checks**: Enable health checks for monitoring
- **Resource limits**: Set memory and CPU limits in docker-compose

### Network Security

- **Use Tailscale**: Avoid exposing services to public internet
- **Security groups**: Restrict access to necessary ports only
- **VPC**: Use private subnets when possible
- **SSL/TLS**: Use HTTPS for all external-facing services

## Monitoring and Health Checks

### Health Check Endpoints

**Implement health check endpoint in your application:**

**NestJS:**
```typescript
// health.controller.ts
@Controller('v1/health')
export class HealthController {
  @Get()
  health() {
    return { status: 'ok', timestamp: new Date().toISOString() };
  }
}
```

**Express:**
```typescript
app.get('/v1/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});
```

### Docker Health Checks

**In Dockerfile:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:3001/v1/health || exit 1
```

**In docker-compose:**
```yaml
healthcheck:
  test: ['CMD', 'curl', '-f', 'http://localhost:3001/v1/health']
  interval: 30s
  timeout: 10s
  retries: 5
  start_period: 40s
```

### Deployment Verification

**Check service health after deployment:**
```bash
# Check container status
docker compose ps

# Check health status
docker inspect --format='{{.State.Health.Status}}' [container-name]

# Check logs
docker compose logs --tail=100 [service-name]

# Test health endpoint
curl http://localhost:3001/v1/health
```

### Post-Deployment Verification

**In GitHub Actions:**
```yaml
- name: Verify deployment
  run: |
    API_IP="${{ vars.TAILSCALE_INSTANCE_IP }}"
    for i in {1..10}; do
      if curl -f --max-time 10 http://${API_IP}:3001/v1/health; then
        echo "✅ Service is healthy"
        exit 0
      fi
      echo "Attempt $i/10 failed, retrying..."
      sleep 5
    done
    echo "❌ Service health check failed"
    exit 1
```

## Rollback Procedures

### Manual Rollback

**1. Find previous image tag:**
- Check GitHub Container Registry
- Look for tags like `master-<commit-sha>`
- Or use semantic version tags

**2. Update docker-compose.yml:**
```yaml
services:
  api:
    image: ghcr.io/owner/service:master-abc123  # Previous tag
```

**3. Deploy previous version:**
```bash
docker compose pull
docker compose up -d --force-recreate
```

**4. Verify rollback:**
```bash
docker compose ps
curl http://localhost:3001/v1/health
```

### Automated Rollback Workflow

**Create `.github/workflows/rollback.yml`:**

```yaml
name: Rollback Deployment

on:
  workflow_dispatch:
    inputs:
      image_tag:
        description: 'Image tag to rollback to (e.g., master-abc123)'
        required: true
        type: string

jobs:
  rollback:
    runs-on: ubuntu-latest
    steps:
      - name: Setup Tailscale
        uses: tailscale/github-action@v2
        with:
          oauth-client-id: ${{ secrets.TAILSCALE_CLIENT_ID }}
          oauth-secret: ${{ secrets.TAILSCALE_CLIENT_SECRET }}

      - name: Rollback to previous version
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ vars.TAILSCALE_INSTANCE_IP }}
          username: ${{ secrets.EC2_USER }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd ~/[project-path]
            # Update image tag in docker-compose.yml
            sed -i "s|image:.*|image: ghcr.io/owner/service:${{ inputs.image_tag }}|" docker-compose.yml
            docker compose pull
            docker compose up -d --force-recreate
```

## Docker Cleanup and Maintenance

### Docker Prune Script

**Create `docker/prune-docker.sh`:**

```bash
#!/bin/bash
# Docker cleanup script for production servers

LOCK_FILE="/tmp/docker-prune.lock"
LOCK_TIMEOUT=300  # 5 minutes max wait

echo "🧹 Starting Docker cleanup..."

# Acquire lock
if [ -f "$LOCK_FILE" ]; then
  echo "⏳ Another prune operation is running, waiting..."
  sleep 5
fi

echo $$ > "$LOCK_FILE"
trap "rm -f $LOCK_FILE" EXIT

# Prune old images (older than 24 hours)
echo "🗑️  Pruning old Docker images..."
docker image prune --filter "until=24h" -f

# Prune stopped containers
echo "🗑️  Pruning stopped containers..."
docker container prune --filter "until=24h" -f

# Prune unused networks
echo "🗑️  Pruning unused networks..."
docker network prune -f

# Show disk space
echo "📊 Docker disk usage:"
docker system df

echo "✅ Docker cleanup complete!"
```

**Run cleanup after deployments:**
```yaml
- name: Docker cleanup
  run: |
    ssh -i ~/.ssh/key user@instance "cd ~/project && ./docker/prune-docker.sh"
```

## Troubleshooting

### Common Issues

**1. Docker Compose v2 not found:**
```bash
# Install Docker Compose v2
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

**2. Health check failures:**
- Verify health endpoint is accessible
- Check container logs: `docker compose logs [service]`
- Ensure health check command is correct
- Increase `start_period` for slow-starting services

**3. Image pull failures:**
- Verify registry authentication
- Check image tag exists
- Verify network connectivity

**4. Deployment timeouts:**
- Increase timeout in workflow
- Check EC2 instance resources (CPU, memory)
- Verify Tailscale connectivity

**5. Service not starting:**
- Check environment variables
- Verify dependencies are healthy
- Review application logs
- Check port conflicts

## Checklist

Before deploying, verify:

- [ ] Dockerfile is optimized (multi-stage build)
- [ ] Health check endpoint implemented
- [ ] Docker Compose v2 installed on EC2
- [ ] Container registry configured
- [ ] GitHub Secrets set up
- [ ] Tailscale configured (or SSH access)
- [ ] Environment variables configured
- [ ] Health checks configured in docker-compose
- [ ] Deployment workflow tested
- [ ] Rollback procedure documented

## Next Steps

After initial deployment:

1. Set up monitoring and alerts
2. Configure automatic cleanup
3. Document deployment process
4. Set up staging environment
5. Implement blue-green deployments (optional)
6. Configure log aggregation
7. Set up backup procedures

