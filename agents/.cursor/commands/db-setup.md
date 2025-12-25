# DB Setup - MongoDB on EC2 with Docker

**Purpose:** Set up MongoDB on EC2 instance using Docker, including docker-compose configuration and connection setup

## Usage

```bash
/db-setup              # Interactive MongoDB setup on EC2
/db-setup --redis      # Also set up Redis
```

## When to Use

Use this command when:

- Setting up MongoDB for a new project
- Need to configure MongoDB on EC2 with Docker
- Setting up development or production database
- Need Redis configuration as well

## What This Command Does

Helps set up:

1. **MongoDB Docker Configuration** - docker-compose setup for MongoDB
2. **EC2 Instance Setup** - Configuration guidance for EC2
3. **Connection Configuration** - Connection strings and environment variables
4. **Security Setup** - Authentication, network security
5. **Backup Strategy** - Backup configuration recommendations
6. **Redis Setup** - Optional Redis configuration

---

## Workflow

### Phase 1: EC2 Instance Setup

**1.1 EC2 Instance Requirements**

**Recommended instance types:**
- **Development:** t3.medium (2 vCPU, 4GB RAM)
- **Production (small):** t3.large (2 vCPU, 8GB RAM)
- **Production (medium):** m5.large (2 vCPU, 8GB RAM)
- **Production (large):** m5.xlarge (4 vCPU, 16GB RAM)

**Storage:**
- **Development:** 20GB gp3 SSD
- **Production:** 100GB+ gp3 SSD (depends on data size)
- Consider EBS snapshots for backups

**1.2 Security Groups**

Configure security groups:

```
Inbound Rules:
- SSH (22) from your IP
- MongoDB (27017) from application security group only
- Redis (6379) from application security group only (if using Redis)

Outbound Rules:
- All traffic (default)
```

**Best Practice:** Restrict MongoDB port to only application servers, not public internet.

### Phase 2: MongoDB Docker Setup

**2.1 Create docker-compose.yml**

**Basic MongoDB setup:**

```yaml
# docker-compose.yml
version: '3.8'

services:
  mongodb:
    image: mongo:7.0
    container_name: mongodb
    restart: unless-stopped
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_ROOT_USERNAME:-admin}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ROOT_PASSWORD}
      MONGO_INITDB_DATABASE: ${MONGO_DATABASE:-app}
    volumes:
      - mongodb_data:/data/db
      - mongodb_config:/data/configdb
      - ./mongo-init:/docker-entrypoint-initdb.d
    networks:
      - app-network
    command: mongod --auth

  # Optional: MongoDB Express (admin UI)
  mongo-express:
    image: mongo-express:latest
    container_name: mongo-express
    restart: unless-stopped
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: ${MONGO_ROOT_USERNAME:-admin}
      ME_CONFIG_MONGODB_ADMINPASSWORD: ${MONGO_ROOT_PASSWORD}
      ME_CONFIG_MONGODB_URL: mongodb://${MONGO_ROOT_USERNAME:-admin}:${MONGO_ROOT_PASSWORD}@mongodb:27017/
    depends_on:
      - mongodb
    networks:
      - app-network
    profiles:
      - tools  # Only start with --profile tools

volumes:
  mongodb_data:
  mongodb_config:

networks:
  app-network:
    driver: bridge
```

**2.2 Create .env file**

```env
# MongoDB Configuration
MONGO_ROOT_USERNAME=admin
MONGO_ROOT_PASSWORD=your-secure-password-here
MONGO_DATABASE=app

# Application Connection
MONGO_URI=mongodb://admin:your-secure-password-here@localhost:27017/app?authSource=admin
```

**2.3 Create initialization script (optional)**

```javascript
// mongo-init/init.js
db = db.getSiblingDB('app');

// Create application user
db.createUser({
  user: 'app_user',
  pwd: 'app_password',
  roles: [
    { role: 'readWrite', db: 'app' }
  ]
});

// Create collections with indexes
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ organization: 1 });
```

### Phase 3: Docker Installation on EC2

**3.1 Install Docker**

```bash
# Update system
sudo yum update -y

# Install Docker
sudo yum install docker -y
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Log out and back in for group changes to take effect
```

**3.2 Verify Installation**

```bash
docker --version
docker-compose --version
```

### Phase 4: Deploy MongoDB

**4.1 Transfer Files to EC2**

```bash
# From local machine
scp docker-compose.yml ec2-user@your-ec2-ip:~/
scp .env ec2-user@your-ec2-ip:~/
scp -r mongo-init ec2-user@your-ec2-ip:~/
```

**4.2 Start MongoDB**

```bash
# SSH into EC2
ssh ec2-user@your-ec2-ip

# Navigate to directory
cd ~

# Start MongoDB
docker-compose up -d mongodb

# Check status
docker-compose ps
docker-compose logs mongodb

# Start with Mongo Express (optional, for admin UI)
docker-compose --profile tools up -d
```

**4.3 Verify MongoDB**

```bash
# Connect to MongoDB
docker exec -it mongodb mongosh -u admin -p your-password --authenticationDatabase admin

# Or test connection
docker exec -it mongodb mongosh mongodb://admin:your-password@localhost:27017/admin
```

### Phase 5: Connection Configuration

**5.1 Application Connection String**

**For local development (if MongoDB on localhost):**
```env
MONGODB_URI=mongodb://app_user:app_password@localhost:27017/app?authSource=admin
```

**For application on same EC2:**
```env
MONGODB_URI=mongodb://app_user:app_password@localhost:27017/app?authSource=admin
```

**For application on different EC2 (same VPC):**
```env
MONGODB_URI=mongodb://app_user:app_password@private-ip-of-mongodb-ec2:27017/app?authSource=admin
```

**5.2 NestJS Connection**

```typescript
// src/config/database.config.ts
export const databaseConfig = {
  uri: process.env.MONGODB_URI || 'mongodb://localhost:27017/app',
  options: {
    retryWrites: true,
    w: 'majority',
  },
};
```

```typescript
// src/app.module.ts
import { Module } from '@nestjs/common';
import { MongooseModule } from '@nestjs/mongoose';
import { databaseConfig } from './config/database.config';

@Module({
  imports: [
    MongooseModule.forRoot(databaseConfig.uri, databaseConfig.options),
    // ... other modules
  ],
})
export class AppModule {}
```

### Phase 6: Security Hardening

**6.1 Network Security**

- Restrict MongoDB port (27017) to only application servers via security groups
- Use VPC private subnets for database instances
- Consider VPN or bastion host for access

**6.2 Authentication**

- Always use authentication (MONGO_INITDB_ROOT_USERNAME/PASSWORD)
- Create application-specific users with least privilege
- Rotate passwords regularly

**6.3 Firewall Rules**

```bash
# On EC2 instance, configure firewall (if needed)
sudo firewall-cmd --permanent --add-port=27017/tcp
sudo firewall-cmd --reload
```

**6.4 SSL/TLS (Production)**

For production, enable SSL/TLS:

```yaml
# docker-compose.yml (production)
services:
  mongodb:
    command: >
      mongod --auth
      --sslMode requireSSL
      --sslPEMKeyFile /etc/ssl/mongodb.pem
    volumes:
      - ./ssl:/etc/ssl
```

### Phase 7: Backup Strategy

**7.1 Automated Backups**

Create backup script:

```bash
#!/bin/bash
# backup-mongodb.sh

BACKUP_DIR="/backups/mongodb"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$DATE"

# Create backup directory
mkdir -p $BACKUP_DIR

# Create backup
docker exec mongodb mongodump --out /data/backup --authenticationDatabase admin -u admin -p $MONGO_ROOT_PASSWORD

# Compress backup
docker exec mongodb tar -czf /data/backup_$DATE.tar.gz -C /data backup

# Copy from container
docker cp mongodb:/data/backup_$DATE.tar.gz $BACKUP_FILE.tar.gz

# Cleanup old backups (keep last 7 days)
find $BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_FILE.tar.gz"
```

**7.2 Cron Job**

```bash
# Add to crontab (crontab -e)
# Daily backup at 2 AM
0 2 * * * /path/to/backup-mongodb.sh
```

**7.3 EBS Snapshots (Alternative)**

For full system backups, use EBS snapshots:
- Schedule automated EBS snapshots via AWS
- Store snapshots in different AZ for redundancy

### Phase 8: Redis Setup (Optional)

**8.1 Add Redis to docker-compose.yml**

```yaml
services:
  redis:
    image: redis:7-alpine
    container_name: redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    command: redis-server --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - app-network

volumes:
  redis_data:
```

**8.2 Redis Connection**

```env
REDIS_URL=redis://:your-redis-password@localhost:6379
```

**8.3 Start Redis**

```bash
docker-compose up -d redis
```

---

## Manual Checklist for AI Agent

When user runs `/db-setup`:

### EC2 Setup

- [ ] Verify EC2 instance is available
- [ ] Check instance type meets requirements
- [ ] Configure security groups (restrict MongoDB port)
- [ ] Set up VPC/subnet configuration

### Docker Setup

- [ ] Install Docker on EC2
- [ ] Install Docker Compose
- [ ] Verify Docker installation

### MongoDB Configuration

- [ ] Create docker-compose.yml for MongoDB
- [ ] Create .env file with credentials
- [ ] Create initialization script (optional)
- [ ] Set secure passwords

### Deployment

- [ ] Transfer files to EC2
- [ ] Start MongoDB container
- [ ] Verify MongoDB is running
- [ ] Test connection

### Application Integration

- [ ] Configure connection string in application
- [ ] Update environment variables
- [ ] Test application connection
- [ ] Verify indexes are created

### Security

- [ ] Enable authentication
- [ ] Configure security groups properly
- [ ] Set up firewall rules
- [ ] Create application user (least privilege)

### Backup

- [ ] Set up backup script
- [ ] Configure cron job for automated backups
- [ ] Test backup and restore process
- [ ] Document backup procedures

### Redis (Optional)

- [ ] Add Redis to docker-compose.yml
- [ ] Configure Redis password
- [ ] Start Redis container
- [ ] Test Redis connection

---

## Examples

### Example 1: Basic MongoDB Setup

**User:** `/db-setup`

**AI Actions:**
1. Guide through EC2 instance selection
2. Help configure security groups
3. Create docker-compose.yml
4. Generate .env file with secure passwords
5. Provide deployment instructions
6. Test connection

### Example 2: MongoDB + Redis

**User:** `/db-setup --redis`

**AI Actions:**
1. All steps from Example 1
2. Add Redis to docker-compose.yml
3. Configure Redis connection
4. Test both MongoDB and Redis

---

## Environment Variables Summary

**MongoDB:**
- `MONGO_ROOT_USERNAME` - Admin username (default: admin)
- `MONGO_ROOT_PASSWORD` - Admin password (required)
- `MONGO_DATABASE` - Default database name
- `MONGODB_URI` - Full connection string for application

**Redis (if using):**
- `REDIS_PASSWORD` - Redis password
- `REDIS_URL` - Redis connection URL

---

## Best Practices

**Security:**
- Never expose MongoDB port to public internet
- Use strong passwords
- Create application-specific users
- Enable SSL/TLS in production

**Performance:**
- Allocate sufficient RAM (MongoDB uses ~50% of available RAM)
- Use EBS gp3 volumes for better performance
- Monitor disk I/O
- Set up indexes before going to production

**Backup:**
- Daily automated backups
- Test restore procedures regularly
- Keep backups off-instance (S3, separate EBS)
- Document backup/restore procedures

**Monitoring:**
- Monitor MongoDB logs
- Set up CloudWatch alarms for disk space
- Monitor connection count
- Track query performance

---

**Created:** 2025-01-27
**Purpose:** Set up MongoDB on EC2 with Docker for micro startup infrastructure

