#!/usr/bin/env bash
set -e # halt script on error

# If this is the publish branch, push it up to gh-pages
if [ $TRAVIS_PULL_REQUEST = "false" ] && [ $TRAVIS_BRANCH = "master" ]; then
  echo "Get ready, we're publishing!"
  npm install -g aglio
  mkdir -p dist
  aglio -t slate -i docs/docs.md -o dist/output.html
  cd dist
  echo ".DS_Store" > .gitignore
  git init
  git config user.name "Travis-CI"
  git config user.email "travis@somewhere.com"
  git add .
  git commit -m "CI deploy to gh-pages"
  git push --force --quiet "https://${GH_TOKEN}@${GH_REF}" master:gh-pages
  rm -rf .git/
else
  echo "Not a publishable branch so we're all done here"
fi
