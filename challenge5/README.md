# ECHO — Challenge 5

## Run locally

Requirements: Docker Engine and Docker Compose.

1. Extract the ZIP archive.
2. Open a terminal in the extracted `echo/` directory.
3. Run:

```bash
docker compose up --build -d
```

Open **http://localhost:8080/**.

All services share this public port:

- `/` — ECHO portal
- `/challenge5.1/`
- `/challenge5.2/`
- `/challenge5.3/`

Stop the stack with:

```bash
docker compose down
```

**Security:** `challenge5/.env` contains the pattern, challenge keys, session secret, and final flag. Keep the source archive and built image private; replace these values before deploying another instance.
