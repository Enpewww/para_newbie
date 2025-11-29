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
