# Deployment Guide

## Local Development

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up --build

# Stop services
docker-compose down
```

### Manual Setup

**Backend:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn backend.main:app --reload --port 8000
```

**Frontend:**
```bash
# Install dependencies
npm install

# Run dev server
npm run dev
```

## Production Deployment

### Frontend (Vercel)

1. **Install Vercel CLI:**
```bash
npm i -g vercel
```

2. **Login to Vercel:**
```bash
vercel login
```

3. **Deploy:**
```bash
vercel deploy --prod
```

4. **Environment Variables:**
Set in Vercel dashboard:
- `NEXT_PUBLIC_API_URL`: Backend API URL

### Backend Options

#### Option 1: Railway

1. Install Railway CLI:
```bash
npm i -g @railway/cli
```

2. Login and deploy:
```bash
railway login
railway init
railway up
```

3. Add environment variables in Railway dashboard

#### Option 2: Heroku

```bash
heroku create perplexiplay-api
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

#### Option 3: DigitalOcean App Platform

1. Connect GitHub repository
2. Configure build settings:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `uvicorn backend.main:app --host 0.0.0.0 --port 8080`
3. Add environment variables

#### Option 4: AWS ECS/Fargate

1. Build Docker image:
```bash
docker build -t perplexiplay-backend .
```

2. Push to ECR:
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker tag perplexiplay-backend:latest <account>.dkr.ecr.us-east-1.amazonaws.com/perplexiplay-backend:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/perplexiplay-backend:latest
```

3. Create ECS task and service

### Database

#### Development
SQLite (default, no setup needed)

#### Production Options

**PostgreSQL (Recommended):**
- Supabase (free tier available)
- Railway
- Heroku Postgres
- AWS RDS
- DigitalOcean Managed Database

**Connection String Format:**
```
postgresql://username:password@host:port/database
```

Update `DATABASE_URL` in environment variables.

## Environment Variables

### Backend

```env
DATABASE_URL=postgresql://user:pass@host:5432/db
JWT_SECRET_KEY=<generate-secure-key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
OPENAI_API_KEY=<your-key>
ANTHROPIC_API_KEY=<your-key>
```

### Frontend

```env
NEXT_PUBLIC_API_URL=https://your-api.com
```

## Security Checklist

- [ ] Change `JWT_SECRET_KEY` to a secure random string
- [ ] Use HTTPS in production
- [ ] Set up CORS properly
- [ ] Enable rate limiting
- [ ] Use environment variables for secrets
- [ ] Set up database backups
- [ ] Configure logging and monitoring
- [ ] Enable SSL for database connections
- [ ] Review and update dependencies regularly

## Monitoring

### Recommended Services
- **Application:** Sentry, LogRocket
- **API:** DataDog, New Relic
- **Uptime:** UptimeRobot, Pingdom

## Scaling

### Horizontal Scaling
- Use load balancers (AWS ALB, Nginx)
- Deploy multiple backend instances
- Use Redis for session storage

### Database Scaling
- Connection pooling
- Read replicas
- Caching with Redis/Memcached

## Backup Strategy

### Database Backups
```bash
# PostgreSQL
pg_dump -U username -h host database > backup.sql

# Restore
psql -U username -h host database < backup.sql
```

### Automated Backups
Configure automated backups in your database provider dashboard.

## CI/CD

GitHub Actions workflow is included (`.github/workflows/ci.yml`).

Configure secrets in GitHub:
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`

## Troubleshooting

### Build Errors
- Check Node.js version (18+)
- Check Python version (3.11+)
- Clear caches: `npm cache clean --force`, `rm -rf .next`

### Database Connection
- Verify connection string format
- Check firewall rules
- Ensure database accepts external connections

### API CORS Errors
- Update CORS settings in `backend/main.py`
- Add frontend domain to allowed origins

## Support

For deployment issues, check:
- [Next.js Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Vercel Docs](https://vercel.com/docs)
