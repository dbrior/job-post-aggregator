#!/bin/bash
set -e

SELENIUM_URL="${SELENIUM_REMOTE_URL}/wd/hub/status"

echo "Waiting for Selenium to be ready..."
until curl -s "$SELENIUM_URL" | grep '"ready": true'; do
  echo "Selenium is not ready yet. Retrying in 5 seconds..."
  sleep 5
done

echo "Selenium is up and running!"
exec "$@"