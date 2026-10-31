# =============================================================================
# NDH-Reconstruction-Demo Master Orchestration Substrate
# Enforces branchless environmental checking, testing, and formal triggers.
# =============================================================================

.PHONY: all env test verify format clean

all: env format test verify

env:
	@echo "📡 [STAGE 1] Syncing local environment dependencies..."
	pip install -e .[dev]

format:
	@echo "🐍 [STAGE 2] Enforcing vertical formatting constraints..."
	black --check --line-length=100 src/ tests/

test:
	@echo "🧮 [STAGE 3] Executing continuous array invariant test suite..."
	pytest -v tests/

verify:
	@echo "🛡️  [STAGE 4] Triggering deterministic enclave verification gates..."
	ndh-verify

clean:
	@echo "🧹 Purging volatile runtime metadata and cache containers..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.swp" -delete
	find . -type f -name "*.bak" -delete
