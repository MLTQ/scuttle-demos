# Auth Service

The Auth Service issues short-lived Ed25519 JWT access tokens and manages refresh sessions in Redis. Token verification is delegated to [[API Gateway]] via the public JWKS endpoint. For zero-downtime secret rollover see [[Key Rotation Policy]].
