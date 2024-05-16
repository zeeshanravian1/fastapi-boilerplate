#!/bin/bash

uvicorn --host 0.0.0.0 --port 8000 --timeout-keep-alive 30 --reload --log-level info main:app
