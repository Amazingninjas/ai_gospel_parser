# Monitoring & Analytics Guide

This guide explains how to monitor the AI Gospel Parser application and track usage analytics.

## Overview

The application includes built-in monitoring and analytics capabilities:

1. **Performance Monitoring** - Track API response times
2. **Usage Analytics** - Track user behavior (privacy-focused)
3. **Health Checks** - Monitor application health
4. **System Metrics** - CPU, memory, disk usage
5. **Database Metrics** - User and conversation statistics

## Monitoring Endpoints

All monitoring endpoints are available at `/api/metrics/`:

### Health Check

```bash
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "healthy",
  "version": "1.0.0"
}
```

**Use Cases:**
- Load balancer health checks
- Uptime monitoring
- Automated alerts

### Performance Metrics

```bash
GET /api/metrics/performance
```

**Response:**
```json
{
  "endpoints": {
    "GET /api/verses": {
      "count": 1523,
      "avg_ms": 42.3,
      "min_ms": 15.2,
      "max_ms": 234.1
    },
    ...
  }
}
```

**Metrics Tracked:**
- Average response time (ms)
- Minimum response time
- Maximum response time
- Request count (last 100 requests per endpoint)

**Use Cases:**
- Identify slow endpoints
- Detect performance degradation
- Capacity planning

### Usage Analytics

```bash
GET /api/metrics/analytics
```

**Response:**
```json
{
  "summary": {
    "total_events": 5432,
    "last_7_days": {
      "active_users": 23,
      "verse_lookups": 543,
      "lexicon_lookups": 234,
      "chat_messages": 432,
      "conversations": 45
    },
    "daily_breakdown": [...]
  },
  "popular_verses": [
    {"reference": "John 3:16", "count": 45},
    {"reference": "Romans 8:28", "count": 32}
  ],
  "popular_words": [
    {"word": "ἀγάπη", "count": 67},
    {"word": "πίστις", "count": 54}
  ]
}
```

**Privacy Features:**
- No personally identifiable information (PII)
- User IDs are hashed
- No tracking of message content
- Data aggregated by day
- Only last 10,000 events stored

**Use Cases:**
- Understand usage patterns
- Identify popular content
- Measure user engagement

### Database Metrics

```bash
GET /api/metrics/database
```

**Response:**
```json
{
  "total_users": 125,
  "active_users": 78,
  "total_conversations": 543,
  "avg_conversations_per_user": 4.34
}
```

**Use Cases:**
- Track growth
- Measure engagement
- Database capacity planning

### System Metrics

```bash
GET /api/metrics/system
```

**Response:**
```json
{
  "cpu_percent": 15.4,
  "memory": {
    "percent": 42.1,
    "used_gb": 4.2,
    "total_gb": 16.0
  },
  "disk": {
    "percent": 65.3,
    "used_gb": 123.4,
    "total_gb": 256.0
  },
  "process": {
    "memory_mb": 245.3,
    "pid": 12345
  }
}
```

**Requirements:**
- Install `psutil`: `pip install psutil`

**Use Cases:**
- Resource monitoring
- Detect memory leaks
- Capacity planning
- Alert on high CPU/memory usage

### Monitoring Dashboard

```bash
GET /api/metrics/dashboard
```

**Authentication Required:** Yes (JWT token)

**Response:** Combined data from all monitoring endpoints

**Use Cases:**
- Single endpoint for monitoring dashboard
- Comprehensive system overview
- Integration with monitoring tools

## Tracking Events

### Automatic Tracking

The analytics service automatically tracks:

**API Calls:**
```python
# Tracked automatically via middleware
analytics.track_api_call(endpoint="/api/verses", user_id=user.id)
```

**Performance:**
```python
# Tracked automatically via middleware
monitor.record(endpoint="GET /api/verses", duration_ms=42.3)
```

### Manual Tracking

Track custom events in your code:

```python
from services.analytics_service import analytics

# Track verse lookup
analytics.track_event(
    event_type="verse_lookup",
    user_id=user.id,
    metadata={"reference": "John 3:16"}
)

# Track lexicon lookup
analytics.track_event(
    event_type="lexicon_lookup",
    user_id=user.id,
    metadata={"word": "ἀγάπη", "strongs": "G26"}
)

# Track chat message
analytics.track_event(
    event_type="chat_message",
    user_id=user.id,
    metadata={"verse_context": "John 3:16"}
)

# Track conversation created
analytics.track_event(
    event_type="conversation_created",
    user_id=user.id
)
```

**Event Types:**
- `verse_lookup` - User searched for a verse
- `lexicon_lookup` - User clicked a Greek word
- `chat_message` - User sent a chat message
- `conversation_created` - User created a conversation
- `user_registered` - New user registered
- `user_login` - User logged in

## Alerts & Notifications

### Slow Request Alerts

Automatically logged when requests take > 1 second:

```python
# In performance_monitor.py
if duration_ms > 1000:
    logger.warning(f"Slow request: {endpoint} took {duration_ms:.2f}ms")
```

**Setup Alert:**
- Monitor application logs
- Filter for "Slow request" warnings
- Send notification (email, Slack, PagerDuty)

### System Resource Alerts

**CPU Alert:**
```python
# Check CPU usage
if cpu_percent > 80:
    send_alert("High CPU usage: {cpu_percent}%")
```

**Memory Alert:**
```python
# Check memory usage
if memory_percent > 85:
    send_alert("High memory usage: {memory_percent}%")
```

**Disk Alert:**
```python
# Check disk usage
if disk_percent > 90:
    send_alert("High disk usage: {disk_percent}%")
```

## Integration with Monitoring Tools

### Prometheus

Export metrics in Prometheus format:

```python
# Add prometheus_client to requirements.txt
from prometheus_client import Counter, Histogram, generate_latest

# Define metrics
request_count = Counter('http_requests_total', 'Total HTTP requests')
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')

# Endpoint to expose metrics
@app.get("/metrics")
async def prometheus_metrics():
    return Response(generate_latest(), media_type="text/plain")
```

### Grafana

Create dashboards using Prometheus data source:
- Request rate (requests/sec)
- Response times (p50, p95, p99)
- Error rates
- Active users
- System resources (CPU, memory)

### Sentry

Add error tracking:

```python
# Install: pip install sentry-sdk
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)

# Errors are automatically captured
```

### DataDog / New Relic

Install respective SDKs:
- DataDog: `pip install ddtrace`
- New Relic: `pip install newrelic`

Follow their documentation for integration.

## Logging

### Structured Logging

Configure structured logging in `config.py`:

```python
import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

# Configure logger
logging.basicConfig(level=logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger = logging.getLogger("ai_gospel_parser")
logger.addHandler(handler)
```

### Log Levels

**INFO:** Normal application flow
```python
logger.info("User registered", extra={"user_id": user.id})
```

**WARNING:** Unexpected but handled situations
```python
logger.warning("Slow request", extra={"endpoint": "/api/verses", "duration_ms": 1234})
```

**ERROR:** Errors that need attention
```python
logger.error("Failed to connect to Ollama", exc_info=True)
```

**CRITICAL:** Severe errors requiring immediate action
```python
logger.critical("Database connection lost")
```

## Monitoring Checklist

### Daily Checks
- [ ] Check health endpoint status
- [ ] Review error logs
- [ ] Check slow request warnings
- [ ] Verify backup completion

### Weekly Checks
- [ ] Review performance metrics
- [ ] Analyze usage analytics
- [ ] Check system resource trends
- [ ] Review popular content

### Monthly Checks
- [ ] Database growth analysis
- [ ] User engagement metrics
- [ ] Performance trend analysis
- [ ] Capacity planning review

## Dashboard Examples

### Simple HTML Dashboard

```html
<!DOCTYPE html>
<html>
<head>
    <title>AI Gospel Parser - Monitoring</title>
    <script>
        async function loadMetrics() {
            const response = await fetch('/api/metrics/dashboard', {
                headers: {
                    'Authorization': 'Bearer YOUR_TOKEN'
                }
            });
            const data = await response.json();

            // Display metrics
            document.getElementById('health').textContent = data.health.status;
            document.getElementById('users').textContent = data.database.total_users;
            document.getElementById('cpu').textContent = data.system.cpu_percent + '%';
            // ... etc
        }

        setInterval(loadMetrics, 5000); // Refresh every 5 seconds
    </script>
</head>
<body onload="loadMetrics()">
    <h1>System Status</h1>
    <p>Health: <span id="health"></span></p>
    <p>Users: <span id="users"></span></p>
    <p>CPU: <span id="cpu"></span></p>
</body>
</html>
```

## Best Practices

1. **Don't track PII**
   - Never log passwords, tokens, or sensitive data
   - Hash user IDs if needed
   - Aggregate data where possible

2. **Set up alerts proactively**
   - Monitor critical endpoints
   - Alert on error spikes
   - Track resource usage trends

3. **Regular reviews**
   - Weekly performance reviews
   - Monthly trend analysis
   - Quarterly capacity planning

4. **Document baselines**
   - Record normal performance metrics
   - Identify seasonal patterns
   - Update baselines as app grows

5. **Test monitoring**
   - Verify alerts trigger correctly
   - Test dashboard under load
   - Practice incident response

## Troubleshooting

### High CPU Usage

**Symptoms:** CPU > 80%

**Possible Causes:**
- Heavy AI inference load
- Inefficient queries
- Too many concurrent requests

**Solutions:**
- Scale horizontally (add more servers)
- Optimize slow queries
- Add request rate limiting

### High Memory Usage

**Symptoms:** Memory > 85%

**Possible Causes:**
- Memory leaks
- Large cached data
- Too many ChromaDB embeddings loaded

**Solutions:**
- Restart application to clear memory
- Reduce cache TTL
- Add memory limits to Docker containers

### Slow Requests

**Symptoms:** Response time > 1 second

**Possible Causes:**
- Database query performance
- Ollama model slow to respond
- Network issues

**Solutions:**
- Add caching for frequently accessed data
- Optimize database indexes
- Use smaller/faster AI model

## Conclusion

Monitoring is essential for maintaining application health and understanding user behavior. Use these tools to:

- Detect issues early
- Understand usage patterns
- Plan for growth
- Improve performance

Start with basic health checks and gradually add more sophisticated monitoring as your application grows.
