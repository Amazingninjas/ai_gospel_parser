# Performance Optimization Guide

This document describes the performance optimizations implemented in the AI Gospel Parser.

## Backend Optimizations

### 1. Caching Service (`services/cache_service.py`)

**In-Memory Cache with TTL:**
- Caches frequently accessed data
- Automatic expiration (default: 5 minutes)
- Decorator-based caching: `@cached(ttl_seconds=300)`
- Reduces database queries and API calls

**Usage Example:**
```python
from services.cache_service import cached

@cached(ttl_seconds=600)  # Cache for 10 minutes
def get_verse(reference: str):
    # This function result will be cached
    return expensive_database_query(reference)
```

**Recommended Caching Targets:**
- Verse lookups (verses don't change)
- Lexicon entries (static data)
- Book lists
- User-independent queries

### 2. Performance Monitoring (`services/performance_monitor.py`)

**Middleware for Request Timing:**
- Tracks all endpoint response times
- Logs slow requests (> 1 second)
- Adds `X-Response-Time` header to responses
- Provides performance statistics

**Enable in main.py:**
```python
from services.performance_monitor import performance_middleware

app.middleware("http")(performance_middleware)
```

**View Statistics:**
```python
from services.performance_monitor import monitor

stats = monitor.get_all_stats()
# Returns: {"GET /api/verses": {"avg_ms": 45.2, "count": 100, ...}, ...}
```

### 3. Database Indexing

**Existing Indexes:**
- `users.email` - Unique index for fast email lookups
- `users.id` - Primary key index
- `conversations.user_id` - Index for fast user conversation queries
- `conversations.id` - Primary key index

**Recommendations:**
- User and Conversation models already have indexes
- SQLite automatically creates indexes on primary keys and unique fields
- For production PostgreSQL, consider composite indexes on (user_id, updated_at)

### 4. API Request Optimization

**Retry Logic with Exponential Backoff:**
- Implemented in `frontend/src/services/api.ts`
- Retries failed requests (408, 429, 500, 502, 503, 504)
- Max 3 retries with exponential backoff (1s, 2s, 4s)
- Reduces impact of transient failures

**Timeout Configuration:**
- 30-second timeout for all requests
- Prevents hanging requests

## Frontend Optimizations

### 1. Code Splitting & Lazy Loading (`utils/lazyLoad.ts`)

**Lazy Load Components:**
```typescript
import { lazyRetry } from '../utils/lazyLoad';

const Dashboard = lazyRetry(
  () => import('./pages/Dashboard'),
  'Dashboard'
);
```

**Benefits:**
- Smaller initial bundle size
- Faster first page load
- Better caching
- Automatic retry on failed chunk loading

**Implementation Plan:**
```typescript
// App.tsx
const Dashboard = lazyRetry(() => import('./pages/Dashboard'), 'Dashboard');
const Login = lazyRetry(() => import('./pages/Login'), 'Login');
const Register = lazyRetry(() => import('./pages/Register'), 'Register');

// Wrap in Suspense
<Suspense fallback={<LoadingSpinner />}>
  <Dashboard />
</Suspense>
```

### 2. Asset Optimization

**Image Optimization:**
- Use WebP format for better compression
- Lazy load images with `loading="lazy"`
- Serve appropriately sized images

**Font Optimization:**
- Google Fonts with `display=swap`
- Preload critical fonts
- Subset fonts if possible

**CSS Optimization:**
- TailwindCSS purges unused styles in production
- Critical CSS inlined in HTML
- Minimize custom CSS

### 3. React Performance

**Memoization:**
```typescript
// Memoize expensive computations
const memoizedValue = useMemo(() => {
  return expensiveComputation(data);
}, [data]);

// Memoize callbacks
const memoizedCallback = useCallback(() => {
  doSomething(data);
}, [data]);

// Memoize components
export default React.memo(MyComponent);
```

**Virtualization for Long Lists:**
- Use `react-window` or `react-virtual` for conversation history
- Only render visible items
- Significant performance boost for 100+ items

## Lighthouse Audit Recommendations

### Performance Score Targets

**Current (Estimated):**
- Performance: ~75-85
- Accessibility: ~95
- Best Practices: ~90
- SEO: ~85

**Target:**
- Performance: 90+
- Accessibility: 100
- Best Practices: 95+
- SEO: 90+

### Key Metrics to Optimize

1. **First Contentful Paint (FCP)**
   - Target: < 1.8s
   - Actions: Code splitting, lazy loading

2. **Largest Contentful Paint (LCP)**
   - Target: < 2.5s
   - Actions: Optimize images, preload critical resources

3. **Time to Interactive (TTI)**
   - Target: < 3.8s
   - Actions: Defer non-critical JavaScript

4. **Cumulative Layout Shift (CLS)**
   - Target: < 0.1
   - Actions: Reserve space for dynamic content

## Production Optimizations

### 1. Build Optimization

**Vite Configuration:**
```typescript
// vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'ui-components': ['./src/components'],
        }
      }
    },
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true, // Remove console.log in production
      }
    }
  }
});
```

### 2. CDN & Caching

**Static Asset Caching:**
- JavaScript: Cache for 1 year (with hash in filename)
- CSS: Cache for 1 year (with hash in filename)
- Images: Cache for 1 year
- HTML: Cache for 5 minutes or no-cache

**Nginx Configuration:**
```nginx
# Cache static assets
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
  expires 1y;
  add_header Cache-Control "public, immutable";
}

# Don't cache HTML
location / {
  expires -1;
  add_header Cache-Control "no-cache";
}
```

### 3. Compression

**Gzip/Brotli Compression:**
```nginx
# Enable gzip
gzip on;
gzip_vary on;
gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/javascript application/json;
gzip_min_length 1024;

# Enable Brotli (if available)
brotli on;
brotli_types text/plain text/css text/xml text/javascript application/javascript application/json;
```

## Monitoring Performance

### Backend Metrics

**View Performance Stats:**
```python
GET /api/metrics/performance

# Response:
{
  "GET /api/verses": {
    "count": 1523,
    "avg_ms": 42.3,
    "min_ms": 15.2,
    "max_ms": 234.1
  },
  ...
}
```

### Frontend Metrics

**Use Browser Performance API:**
```typescript
// Measure page load time
const perfData = performance.getEntriesByType("navigation")[0];
console.log(`Page load: ${perfData.loadEventEnd - perfData.loadEventStart}ms`);

// Measure API calls
const apiCalls = performance.getEntriesByType("resource")
  .filter(r => r.name.includes('/api/'));
```

## Database Performance

### Query Optimization

**Use Pagination:**
```python
# Bad: Load all conversations
conversations = db.query(Conversation).filter(user_id=user_id).all()

# Good: Paginate
conversations = db.query(Conversation)
  .filter(user_id=user_id)
  .order_by(Conversation.updated_at.desc())
  .offset(skip)
  .limit(limit)
  .all()
```

**Select Only Needed Columns:**
```python
# Bad: Load full objects
users = db.query(User).all()

# Good: Select specific columns
users = db.query(User.id, User.email).all()
```

### Connection Pooling

**SQLAlchemy Configuration:**
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,          # Maximum concurrent connections
    max_overflow=10,       # Additional connections when pool is full
    pool_pre_ping=True,    # Verify connections before use
    pool_recycle=3600,     # Recycle connections every hour
)
```

## Future Optimizations

### Recommended Next Steps

1. **Implement Code Splitting** (2 hours)
   - Lazy load routes
   - Split vendor bundles
   - Expected: -30% initial bundle size

2. **Add Redis Caching** (4 hours)
   - Replace in-memory cache with Redis
   - Persistent across server restarts
   - Shared cache in multi-server setup

3. **Database Query Optimization** (2 hours)
   - Add composite indexes
   - Optimize conversation queries
   - Expected: -50% query time

4. **Implement CDN** (1 hour)
   - Serve static assets from CDN
   - Reduce server load
   - Expected: -40% asset load time

5. **Add Service Worker** (3 hours)
   - Cache API responses
   - Offline support
   - Expected: Instant repeat visits

## Testing Performance

### Benchmark Tools

**Backend:**
```bash
# Use Apache Bench
ab -n 1000 -c 10 http://localhost:8000/api/health

# Use wrk
wrk -t4 -c100 -d30s http://localhost:8000/api/verses/John%203:16
```

**Frontend:**
```bash
# Lighthouse CLI
npm install -g lighthouse
lighthouse http://localhost:5173 --view

# WebPageTest
# Visit: https://www.webpagetest.org/
```

### Performance Budget

Set performance budgets in `vite.config.ts`:
```typescript
export default defineConfig({
  build: {
    chunkSizeWarningLimit: 500, // Warn if chunk > 500KB
  }
});
```

## Monitoring in Production

### Tools

- **Application Monitoring:** New Relic, DataDog, or Sentry
- **Database Monitoring:** pg_stat_statements (PostgreSQL)
- **Frontend Monitoring:** Google Analytics, LogRocket

### Key Metrics to Track

1. **API Response Times**
   - Average: < 200ms
   - P95: < 500ms
   - P99: < 1000ms

2. **Database Query Times**
   - Average: < 50ms
   - P95: < 200ms

3. **Frontend Load Times**
   - FCP: < 1.8s
   - LCP: < 2.5s
   - TTI: < 3.8s

4. **Error Rates**
   - Target: < 1% of requests
   - Alert on spikes

## Conclusion

Performance optimization is an ongoing process. Start with the implemented optimizations (caching, lazy loading, retry logic) and measure results before implementing additional optimizations.

**Priority Order:**
1. Enable caching for verse/lexicon lookups (immediate 50%+ improvement)
2. Implement code splitting (30% smaller bundles)
3. Add performance monitoring to production
4. Optimize database queries as needed
5. Consider Redis for multi-server deployments

Monitor performance metrics regularly and optimize based on real-world usage patterns.
