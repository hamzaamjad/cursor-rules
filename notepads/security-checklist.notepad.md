# General Security Checklist

This checklist provides common security verification points. Refer to specific rules like `backend-security.mdc` for detailed requirements.

## Input Validation
- [ ] Are all external inputs (params, body, headers, uploads) validated? (Type, length, format, range)
- [ ] Is sanitization applied to prevent injection (SQLi, XSS, Command Injection)?
- [ ] Are strong, well-tested validation libraries used?

## Authentication (AuthN)
- [ ] Are strong password policies enforced?
- [ ] Is multi-factor authentication (MFA) available/enforced for sensitive accounts?
- [ ] Are brute-force attacks mitigated (e.g., rate limiting, account lockout)?
- [ ] Are session management mechanisms secure (e.g., HTTPS-only cookies, secure flags, short timeouts)?

## Authorization (AuthZ)
- [ ] Is the principle of least privilege applied?
- [ ] Are access controls enforced on every sensitive resource/operation?
- [ ] Are roles and permissions clearly defined and regularly reviewed?
- [ ] Are authorization checks performed server-side, not just client-side?

## Data Handling & Storage
- [ ] Is sensitive data (PII, secrets) encrypted at rest?
- [ ] Is sensitive data encrypted in transit (TLS 1.2+)?
- [ ] Are secrets (API keys, DB creds) stored securely (e.g., Vault, KMS), not in code/config files?
- [ ] Is data minimization practiced (collect/store only what's necessary)?
- [ ] Are there procedures for secure data disposal?

## Error Handling & Logging
- [ ] Are generic error messages returned to users (no stack traces or sensitive details)?
- [ ] Are detailed errors logged securely for internal use?
- [ ] Do logs avoid recording PII or secrets? If so, is masking effective?
- [ ] Are security-relevant events logged (e.g., failed logins, access denials)?

## Dependency Management
- [ ] Are dependencies regularly scanned for vulnerabilities?
- [ ] Is there a process for patching known vulnerabilities promptly?

## API Security
- [ ] Are public APIs rate-limited?
- [ ] Are API endpoints properly secured with AuthN/AuthZ?
- [ ] Is OpenAPI/Swagger documentation up-to-date and reviewed for info leakage?

## Secure Configuration
- [ ] Are default credentials changed?
- [ ] Are unnecessary services/features disabled?
- [ ] Are security headers (CSP, HSTS, X-Frame-Options) used appropriately for web apps?
