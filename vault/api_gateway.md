# API Gateway

Edge reverse proxy handling TLS termination, rate limiting, and JWT signature checks against [[Auth Service]] JWKS endpoints. Caches JWKS payloads for 5 minutes; see [[Observability]] for 401 spike alerts.
