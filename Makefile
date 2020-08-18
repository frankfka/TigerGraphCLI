.PHONY: docs
docs:
	# Generate docs - typer-cli must be referenced to the venv installation
	typer tgcli utils docs --name tgcli --output docs/USAGE.md

.PHONY: build
build:
	# Build the project
	poetry build

.PHONY: publish
publish:
	# Publish to PyPi
	poetry publish --build