"""
NDH Interaction Geometry Test Suite
Validates dynamic metric evolution, Lie-symmetrized perturbations,
and finite-time transformer capacity tracking invariants.
"""

import pytest
import numpy as np
from ndh_demo.interaction import InteractionGeometryEngine
from ndh_demo.transformer_bound import TransformerBoundEngine


def test_metric_symmetry_invariant():
    """Asserts that the metric tensor maintains perfect geometric index symmetry."""
    engine = InteractionGeometryEngine(dimension=80)
    mock_perturbation = np.random.randn(80) * 2.0
    
    # Execute metric evolution update step
    updated_g, _ = engine.update_metric_evolution(mock_perturbation)
    
    # Symmetric check: Assert that g_ij identically equals g_ji
    assert np.allclose(updated_g, updated_g.T, atol=1e-8)


def test_susceptibility_scalar_bounds():
    """Confirms that the stability scalar tracks local functional variation trace metrics."""
    engine = InteractionGeometryEngine(dimension=80)
    mock_perturbation = np.random.randn(80) * 1.5
    
    _, stability_scalar = engine.update_metric_evolution(mock_perturbation)
    
    assert stability_scalar >= 0.0
    assert not np.isnan(stability_scalar)


def test_attention_mimicry_scaling():
    """Validates inner product matrix scaling bounds under token query-key checks."""
    bound_engine = TransformerBoundEngine(dimension=80)
    q = np.ones(80) * 0.5
    k = np.ones(80) * 0.5
    
    # Expected: dot(q, k) = 80 * 0.25 = 20.0. Scaling factor = sqrt(80) = 8.9442719
    # Expected scalar = 20.0 / 8.9442719 = 2.23606797
    expected_scalar = 20.0 / np.sqrt(80)
    calculated_scalar = bound_engine.calculate_attention_mimicry(q, k)
    
    assert np.isclose(calculated_scalar, expected_scalar, atol=1e-7)


def test_finite_time_capacity_exhaustion():
    """Models finite-time collapse sequences under high continuous linear load steps."""
    # Set a tiny capacity floor to guarantee rapid execution limits checking
    bound_engine = TransformerBoundEngine(dimension=80, capacity_ceiling=5.0)
    q = np.ones(80) * 2.0
    k = np.ones(80) * 2.0
    
    # Loop continuous interaction iterations until the engine registers a threshold breach
    breached = False
    for _ in range(10):
        breached, _ = bound_engine.evaluate_capacity_step(q, k, drift_coeff=2.0)
        if breached:
            break
            
    assert breached is True
