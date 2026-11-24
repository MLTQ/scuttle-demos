# Key Rotation Policy

To rotate expired Ed25519 signing keys without dropping active user sessions, publish the new public key (`kid_next`) to the JWKS set at least 24 hours before switching the signer. Keep the retiring key (`kid_prev`) in the JWKS verification window until all outstanding refresh tokens expire (max 7 days), then revoke `kid_prev` via [[Secret Manager]] and audit [[API Gateway]] cache TTLs.
