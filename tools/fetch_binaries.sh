#!/usr/bin/env bash
# tools/bin/ (gitignored) me yq + crane wapas laata hai — GitHub releases se, bina token.
set -euo pipefail
mkdir -p "$(dirname "$0")/bin" && cd "$(dirname "$0")/bin"
[ -x yq ]    || { curl -sL -o yq.tar.gz "https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64.tar.gz"; tar -xzf yq.tar.gz ./yq_linux_amd64; mv yq_linux_amd64 yq; chmod +x yq; rm -f yq.tar.gz; }
[ -x crane ] || { curl -sL -o crane.tar.gz "https://github.com/google/go-containerregistry/releases/latest/download/go-containerregistry_Linux_x86_64.tar.gz"; tar -xzf crane.tar.gz crane; chmod +x crane; rm -f crane.tar.gz; }
./yq --version && ./crane version
echo "OK — ab export PATH=\"$PWD:\$PATH\" karo"
