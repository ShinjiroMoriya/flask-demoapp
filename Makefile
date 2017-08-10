.PHONY: all
.PHONY: server
.PHONY: help
.PHONY: sass
.PHONY: sass-min

scssFromPath = app/static/assets/scss/
scssToPath   = app/static/assets/css/

all: server sass

server: ## サーバーを立ち上げる
	@sudo python dev.py server

dbinit: ## DBセット
	@python dev.py db init

migrate: ## DBマイグレーション
	@python dev.py db migrate

upgrade: ## DBマイグレート更新
	@python dev.py db upgrade

sass: ## scssコンパイル
	@sass --sourcemap=none --no-cache --watch $(scssFromPath):$(scssToPath) --style expanded

sass-min: ## scssコンパイル圧縮バージョン
	@sass --sourcemap=none --no-cache --watch $(scssFromPath):$(scssToPath) --style compressed

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
