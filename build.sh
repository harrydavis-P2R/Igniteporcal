#!/bin/sh
# Wraps src/calculator.html in a full HTML document as index.html (open in any browser, works offline apart from fonts).
set -e
cd "$(dirname "$0")"
{
  printf '<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n<meta name="apple-mobile-web-app-capable" content="yes">\n</head>\n<body>\n'
  cat src/calculator.html
  printf '\n</body>\n</html>\n'
} > index.html
