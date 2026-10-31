"""
NDH Geometry Engine Test Suite
Validates numerical invariants, drift neutrality, and curvature bounds.
"""

import pytest
import numpy as np
from ndh_demo.geometry import compute_apex_gradient, compute_9d_radial_laplacian

def test_apex_gradient_normalization():
    """Asserts that the apex gradient enforces strict unit-length scaling."""
    # Test a typical non-zero gradient vector
    mock_gradient = np.random.randn(80) * 5.0
    apex_grad = compute_apex_gradient(mock_gradient)
    
    # The magnitude of a normalized vector must be identically 1.0
    assert np.isclose(np.linalg.norm(apex_grad), 1.0, atol=1e-7)

def test_apex_gradient_zero_edge_case():
    """Confirms that a dead gradient field safely drops to a null vector."""
    zero_gradient = np.zeros(80)
    apex_grad = compute_apex_gradient(zero_gradient)
    
    assert np.all(apex_grad == 0.0)

def test_9d_radial_laplacian_diffusion():
    """Validates the exact mathematical output of the curvature diffusion operator."""
    r = 2.0
    f_prime = 0.5
    f_double_prime = 1.2
    
    # Expected: 1.2 + (8 / 2.0) * 0.5 = 1.2 + 2.0 = 3.2
    expected_output = 3.2
    calculated_output = compute_9d_radial_laplacian(r, f_prime, f_double_prime)
    
    assert np.isclose(calculated_output, expected_output, atol=1e-7)

def test_9d_radial_laplacian_boundary_violation():
    """Asserts that non-positive radial inputs trigger immediate runtime boundary errors."""
    with pytest.raises(ValueError, match="Radial distance 'r' must be strictly positive"):
        compute_9d_radial_laplacian(0.0, 1.0, 1.0)
        
    with pytest.raises(ValueError, match="Radial distance 'r' must be strictly positive"):
        compute_9d_radial_laplacian(-1.5, 1.0, 1.0)
