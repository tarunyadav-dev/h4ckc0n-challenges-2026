# NovaVault — Challenge 2: Digital Footprints

A guided, identifier-driven forensic investigation console for the Mirror Investigation CTF.

## Requirements

- Docker Desktop (Windows/macOS) or Docker Engine + Docker Compose (Linux)
- Netcat (`nc`) on the player/client machine
- A private `.env` file configured by the challenge operator

## Configure

- copy the zip file provided here.
- cd into this folder.

## Build and start

```bash
docker compose up --build -d
```

Check the service:

```bash
docker compose ps
docker compose logs -f novavault
```

Connect from the Docker host:

```bash
nc 127.0.0.1 4444
```

Connect from another machine:

```bash
nc <SERVER_IP> 4444
```

Allow inbound TCP port `4444` in the host/cloud firewall. Use a trusted network or VPN; the console uses plain TCP.

## Stop

```bash
docker compose down
```
