version=$(cat trans_rss/version)
docker build . -t liyihc/trans-rss:$version -t liyihc/trans-rss:latest
