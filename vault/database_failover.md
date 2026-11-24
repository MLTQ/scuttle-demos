# Database Failover

Primary Postgres cluster replicates synchronously to a standby region. During failover, connection poolers drain for 15 seconds and fetch fresh credentials from [[Secret Manager]]. Monitor lag metrics in [[Observability]].
