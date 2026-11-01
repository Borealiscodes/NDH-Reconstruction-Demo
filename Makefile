# =============================================================================
# NDH-Reconstruction-Demo Master Orchestration Substrate
# Enforces branchless environmental checking, testing, and formal triggers.
# Integrates Phase 1 Core, Phase 2 Geometry, and Phase 3 Lean 4 Enclaves.
# =============================================================================

.PHONY: all env test verify format clean lean_init lean_build

all: env format test verify

env:
	@echo "📡 [STAGE 1] Syncing local environment dependencies..."
	pip install -e .[dev]

format:
	@echo "🐍 [STAGE 2] Enforcing vertical formatting constraints..."
	black --check --line-length=100 src/ tests/

test:
	@echo "🧮 [STAGE 3] Executing comprehensive numerical invariant test suite..."
	pytest -v tests/test_geometry.py tests/test_interaction.py

verify: lean_build
	@echo "🛡️  [STAGE 4] Triggering deterministic enclave verification gates..."
	ndh-verify
	@echo "💎 [SUCCESS] Continuous arrays and formal type enclaves match completely."

lean_init:
	@echo "📦 [PHASE 3.1] Synchronizing Lean 4 mathlib packaging dependencies..."
	cd verification/lean && lake update

lean_build: lean_init
	@echo "📐 [PHASE 3.2] Compiling dependent type structures and symplectic invariants..."
	cd verification/lean && lake build

clean:
	@echo "🧹 Purging volatile runtime metadata, build artifacts, and cache containers..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.swp" -delete
	find . -type f -name "*.bak" -delete
	rm -rf verification/lean/.lake/ verification/lean/build/
