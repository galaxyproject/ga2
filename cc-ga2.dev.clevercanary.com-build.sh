#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -e

echo \"Deleting ./out/\"
rm -rf ./out

# install node version 20.10.0
n 20.10.0
npm ci
export NEXT_PUBLIC_BASE_PATH=""

# Build catalog
npm run build:local

export BUCKET=s3://wn0-ga2.dev/
export SRCDIR=out/

aws s3 sync  $SRCDIR $BUCKET --delete --profile excira
aws cloudfront create-invalidation --distribution-id E2FPRWW4KQ5FCL --paths "/*" --profile excira
