#!/usr/bin/env bash
# FULL SETUP: n8n + Postgres + Python runner (Playwright headful via Xvfb) + WAHA Plus
# Usage:
#   ./bootstrap.sh [--fresh]
set -euo pipefail
IFS=$'\n\t'
trap 'echo "ERROR at line $LINENO"; exit 1' ERR

# Args
FRESH="${1:-}"
if [[ "$FRESH" != "--fresh" && "${2:-}" == "--fresh" ]]; then
  FRESH="--fresh"
fi

: "${PORT:=5678}"
: "${WAHA_PORT:=3000}"

# Webhook URL for N8N UI display (Localhost)
export WEBHOOK_URL="http://localhost:${PORT}"

# Paths (RELATIF ke folder script)
ROOT_DIR="$(pwd)"
N8N_DATA_DIR="${ROOT_DIR}/n8n-data"
PY_CODE_DIR="${ROOT_DIR}/py"
RUNNER_DIR="${ROOT_DIR}/runner"

# WAHA: paths & secrets dir
WAHA_SESS_DIR="${ROOT_DIR}/waha-sessions"
WAHA_MEDIA_DIR="${ROOT_DIR}/waha-media"
SECRETS_DIR="${ROOT_DIR}/secrets"

mkdir -p "${N8N_DATA_DIR}" "${PY_CODE_DIR}" "${RUNNER_DIR}" \
         "${WAHA_SESS_DIR}" "${WAHA_MEDIA_DIR}" "${SECRETS_DIR}" backups scripts

# Optional fresh wipe
if [[ "${FRESH:-}" == "--fresh" ]]; then
  echo "[*] Fresh wipe..."
  docker compose down -v 2>/dev/null || true
  for c in n8n-agent postgres python-runner waha; do docker rm -f "$c" 2>/dev/null || true; done
  docker volume rm pgdata 2>/dev/null || true
  docker builder prune -af  2>/dev/null || true
  docker image   prune -af  2>/dev/null || true
  docker system  prune -af  2>/dev/null || true

  # Aman di /mnt/c (DrvFS)
  for d in "${N8N_DATA_DIR}" "${WAHA_SESS_DIR}" "${WAHA_MEDIA_DIR}" "${SECRETS_DIR}"; do
    if [[ -e "$d" ]]; then
      chmod -R u+rw "$d" 2>/dev/null || true
      rm -rf -- "$d"     2>/dev/null || true
      if [[ -e "$d" ]]; then
        find "$d" -mindepth 1 -exec rm -rf -- {} + 2>/dev/null || true
        rmdir "$d" 2>/dev/null || true
      fi
    fi
    mkdir -p "$d"
  done
fi

# N8N ENCRYPTION KEY (re-use jika ada)
if [[ -f "${N8N_DATA_DIR}/ENCRYPTION_KEY" ]]; then
  N8N_ENCRYPTION_KEY="$(cat "${N8N_DATA_DIR}/ENCRYPTION_KEY")"
else
  N8N_ENCRYPTION_KEY="$(tr -dc A-Za-z0-9 </dev/urandom | head -c 32 || true)"
  printf '%s' "$N8N_ENCRYPTION_KEY" > "${N8N_DATA_DIR}/ENCRYPTION_KEY"
fi
export N8N_ENCRYPTION_KEY

# WAHA secrets (auto; ikut terhapus saat --fresh)
if [[ -f "${SECRETS_DIR}/waha_dashboard_user" && -f "${SECRETS_DIR}/waha_dashboard_pass" ]]; then
  WAHA_USER="$(cat "${SECRETS_DIR}/waha_dashboard_user")"
  WAHA_PASS="$(cat "${SECRETS_DIR}/waha_dashboard_pass")"
else
  WAHA_USER="waha"
  set +o pipefail
  WAHA_PASS="$(head -c 32 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 20)"
  set -o pipefail
  printf '%s' "${WAHA_USER}" > "${SECRETS_DIR}/waha_dashboard_user"
  printf '%s' "${WAHA_PASS}" > "${SECRETS_DIR}/waha_dashboard_pass"
  chmod 600 "${SECRETS_DIR}/waha_dashboard_user" "${SECRETS_DIR}/waha_dashboard_pass"
fi

if [[ -f "${SECRETS_DIR}/waha_api_key_plain" && -f "${SECRETS_DIR}/waha_api_key_sha512" ]]; then
  WAHA_API_KEY_PLAIN="$(cat "${SECRETS_DIR}/waha_api_key_plain")"
  WAHA_API_KEY_SHA512="$(cat "${SECRETS_DIR}/waha_api_key_sha512")"
else
  if command -v uuidgen >/dev/null 2>/dev/null; then
    WAHA_API_KEY_PLAIN="$(uuidgen | tr -d '-')"
  else
    WAHA_API_KEY_PLAIN="$(tr -dc 'A-Za-z0-9' </dev/urandom | head -c 32)"
  fi
  if command -v sha512sum >/dev/null 2>&1; then
    set +o pipefail
    WAHA_API_KEY_SHA512="$(printf %s "${WAHA_API_KEY_PLAIN}" | sha512sum | awk '{print $1}')" || WAHA_API_KEY_SHA512=""
    set -o pipefail
  elif command -v openssl >/dev/null 2>&1; then
    WAHA_API_KEY_SHA512="$(printf %s "${WAHA_API_KEY_PLAIN}" | openssl dgst -sha512 -r | awk '{print $1}')" || WAHA_API_KEY_SHA512=""
  else
    echo "[ERR] sha512sum/openssl tidak tersedia"; exit 1
  fi
  printf '%s' "${WAHA_API_KEY_PLAIN}"  > "${SECRETS_DIR}/waha_api_key_plain"
  printf '%s' "${WAHA_API_KEY_SHA512}" > "${SECRETS_DIR}/waha_api_key_sha512"
  chmod 600 "${SECRETS_DIR}/waha_api_key_plain" "${SECRETS_DIR}/waha_api_key_sha512"
fi

export WAHA_USER WAHA_PASS WAHA_API_KEY_SHA512

# ==== WAHA PLUS: login -> pull -> logout (sesuai panel) ====
WAHA_PLUS_KEY=dckr_pat_vB6GmzJKhncKUFA3xgTsTy6CaHU
echo "[*] Login to WAHA Plus registry..."
docker login -u devlikeapro -p ${WAHA_PLUS_KEY}
echo "[*] Pulling WAHA Plus image..."
docker pull devlikeapro/waha-plus:latest
echo "[*] Logout from WAHA Plus registry..."
docker logout
# ==========================================================

# Python runner app
cat > "${RUNNER_DIR}/app.py" <<'PY'
#!/usr/bin/env python3
from flask import Flask, request, jsonify, make_response
import subprocess, os

app = Flask(__name__)

@app.get("/healthz")
def healthz():
  resp = make_response("ok", 200)
  resp.headers["Connection"] = "close"
  return resp

@app.post("/run")
def run():
  data = request.get_json(force=True) or {}
  entry = data.get("entry","agent.py")
  args  = list(map(str, data.get("args", [])))
  path  = f"/code/{entry}"
  if not os.path.exists(path):
    resp = make_response(jsonify(error=f"not found: {entry}"), 404)
    resp.headers["Connection"] = "close"
    return resp

  timeout_sec = int(data.get("timeout", os.getenv("RUN_TIMEOUT_SEC", "1800")))
  env = os.environ.copy()
  for k, v in (data.get("env", {}) or {}).items():
    env[str(k)] = str(v)

  try:
    out = subprocess.check_output(
      ["python", path, *args],
      stderr=subprocess.STDOUT, text=True,
      timeout=timeout_sec, env=env, cwd="/code"
    )
    resp = make_response(jsonify(output=out), 200)
    resp.headers["Connection"] = "close"
    return resp
  except subprocess.CalledProcessError as e:
    resp = make_response(jsonify(error=e.output, returncode=e.returncode), 500)
    resp.headers["Connection"] = "close"
    return resp
  except subprocess.TimeoutExpired as e:
    resp = make_response(jsonify(error=f"timeout after {timeout_sec}s", output=e.output or ""), 504)
    resp.headers["Connection"] = "close"
    return resp

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8000, threaded=True)
PY

# compose.yaml
cat > compose.yaml <<YML
services:
  postgres:
    image: postgres:18
    container_name: postgres
    environment:
      POSTGRES_USER: agent
      POSTGRES_PASSWORD: 123
      POSTGRES_DB: amarthafin
      PGDATA: /var/lib/postgresql/18/docker
    ports: ["5433:5432"]
    volumes:
      - pgdata:/var/lib/postgresql
    healthcheck:
      test: ["CMD-SHELL","pg_isready -h localhost -U $$POSTGRES_USER -d $$POSTGRES_DB"]
      interval: 10s
      timeout: 10s
      retries: 20
      start_period: 300s
    networks: { n8n: { aliases: [postgres] } }

  python-runner:
    image: python:3.14.0-slim-bookworm
    container_name: python-runner
    working_dir: /app
    restart: unless-stopped
    environment:
      PIP_DISABLE_PIP_VERSION_CHECK: "1"
      PYTHONUNBUFFERED: "1"
      HEADLESS: "0"
      PW_NO_SANDBOX: "1"
      DISPLAY: ":99"
      XDG_RUNTIME_DIR: "/tmp/runtime"
      PGHOST: "postgres"
      PGPORT: "5432"
      PGUSER: "agent"
      PGPASSWORD: "123"
      PGDATABASE: "amarthafin"
      PY_CODE_DIR: "/code"
    volumes:
      - ./runner:/app
      - ./py:/code
    command: >
      bash -lc 'set -e;
        apt-get update;
        apt-get install -y --no-install-recommends xvfb curl ca-certificates netcat-openbsd;
        rm -rf /var/lib/apt/lists/*;

        python -m pip install -qU pip;
        pip install -q --no-cache-dir flask requests pandas openpyxl "psycopg[binary]>=3.2" "psycopg2-binary>=2.9.9" playwright pymupdf requests pillow;

        python -m playwright install --with-deps chromium;

        Xvfb :99 -screen 0 1366x768x24 &

        exec python app.py'
    healthcheck:
      test: ["CMD-SHELL","python - <<'PY'\nimport urllib.request,sys\ntry:\n  urllib.request.urlopen('http://localhost:8000/healthz',timeout=2)\n  sys.exit(0)\nexcept Exception:\n  sys.exit(1)\nPY"]
      interval: 5s
      timeout: 5s
      retries: 30
      start_period: 40s
    networks: { n8n: { aliases: [python-runner] } }

  n8n:
    image: n8nio/n8n:latest
    container_name: n8n-agent
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
      python-runner:
        condition: service_started
    environment:
      N8N_ENCRYPTION_KEY: "${N8N_ENCRYPTION_KEY}"
      N8N_PROXY_HOPS: "1"
      WEBHOOK_URL: "http://n8n-agent:5678"
      N8N_PORT: "5678"
      N8N_TIMEZONE: "Asia/Jakarta"
      GENERIC_TIMEZONE: "Asia/Jakarta"
      NODE_OPTIONS: "--max-old-space-size=2048"
      N8N_DATABASE_TYPE: "postgresdb"
      N8N_DATABASE_POSTGRESDB_HOST: "postgres"
      N8N_DATABASE_POSTGRESDB_PORT: "5432"
      N8N_DATABASE_POSTGRESDB_DATABASE: "amarthafin"
      N8N_DATABASE_POSTGRESDB_USER: "agent"
      N8N_DATABASE_POSTGRESDB_PASSWORD: "123"
      N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS: "false"
      PGHOST: "postgres"
      PGPORT: "5432"
      PGUSER: "agent"
      PGPASSWORD: "123"
      PGDATABASE: "amarthafin"
    ports: ["5678:5678"]
    volumes:
      - ./n8n-data:/home/node/.n8n
      - ./py:/workspace/py
    healthcheck:
      test: ["CMD-SHELL","sh -lc '(command -v curl >/dev/null && curl -s http://localhost:5678/) || wget -qO- http://localhost:5678/ | grep -qi \"<title>n8n\"'"]
      interval: 10s
      timeout: 5s
      retries: 30
      start_period: 30s
    networks: { n8n: { aliases: [n8n-agent] } }

  waha:
    image: devlikeapro/waha-plus:latest
    container_name: waha
    restart: unless-stopped
    shm_size: 1g
    environment:
      - TZ=Asia/Jakarta
      - WHATSAPP_API_PORT=3000
      - WHATSAPP_DEFAULT_ENGINE=WEBJS
      - WAHA_DASHBOARD_ENABLED=true
      - WAHA_APPS_ENABLED=false
      - WAHA_DASHBOARD_USERNAME=waha
      - WAHA_DASHBOARD_PASSWORD=tNyY5PQF3kllRZDO9UKw
      - WAHA_API_KEY=sha512:0ad6751d8f457e3060ace828f5ceddf51f38b709f6916cacc8dde70e6fc8e307d8d6e702b171cb3156baa21b1de6216b8e256266e3d3b14a84f98b568b48dc94
      - WAHA_API_KEY_PLAIN=4abe04445a8240c78042d65fe9e4a458
      - WAHA_BASE_URL=http://waha:3000
      - WAHA_PUBLIC_URL=http://localhost:3000
      - WHATSAPP_API_SCHEMA=http
      - WHATSAPP_FILES_FOLDER=/app/.media
      - WHATSAPP_FILES_LIFETIME=0
      - WHATSAPP_SWAGGER_ENABLED=true
      - WHATSAPP_SWAGGER_USERNAME=waha
      - WHATSAPP_SWAGGER_PASSWORD=tNyY5PQF3kllRZDO9UKw
    ports: ["3000:3000"]
    volumes:
      - ./waha-sessions:/app/.sessions
      - ./waha-media:/app/.media
    networks: { n8n: { aliases: [waha] } }

networks:
  n8n: {}

volumes:
  pgdata:
YML

# Start stack
echo "[*] Building & starting containers..."
docker compose up -d --build

# Wait health (n8n/python-runner)
echo "[*] Wait n8n / python-runner..."
for _ in {1..120}; do
  ok1=$([ "$(docker inspect -f '{{.State.Health.Status}}' n8n-agent 2>/dev/null || echo starting)" = "healthy" ] && echo 1 || echo 0)
  ok2=$([ "$(docker inspect -f '{{.State.Health.Status}}' python-runner 2>/dev/null || echo starting)" = "healthy" ] && echo 1 || echo 0)
  if [ "$ok1" = "1" ] && [ "$ok2" = "1" ]; then
    echo "[OK] All healthy"
    break
  fi
  sleep 2
done

echo
echo "[OK] n8n UI :   http://localhost:${PORT}"
echo "[OK] Webhooks base :  ${WEBHOOK_URL}"
echo "[OK] Python runner :  http://localhost:8000/healthz"
echo "[OK] WAHA API :  http://localhost:${WAHA_PORT}"
echo
echo "[CREDS] WAHA_DASHBOARD_USERNAME: ${WAHA_USER}"
echo "[CREDS] WAHA_DASHBOARD_PASSWORD: ${WAHA_PASS}"
echo "[CREDS] WAHA_API_KEY (plain; header X-Api-Key): ${WAHA_API_KEY_PLAIN}"
echo "[CREDS] WAHA_API_KEY (hash tersimpan): sha512:${WAHA_API_KEY_SHA512}"