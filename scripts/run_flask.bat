@echo off
setlocal
set MODEL_NAME=gpt2
set DEVICE=cpu
set MAX_TOKENS=256
python -m app.server_flask
