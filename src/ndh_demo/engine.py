"""
NDH Master Runtime Ecosystem
Orchestrates the continuous simulation loop by coupling directional steering 
with radial diffusion and safety interception gates.
"""

import sys
import numpy as np
from ndh_demo.geometry import evaluate_manifold_state
from ndh_demo.conservation import ConservationEngine
from ndh_demo.interceptor import SafetyInterceptor


def execute_runtime_cycle(steps: int = 5) -> None:
    """
    Runs a sequential tracking cycle over simulated manifold state updates.
    Integrates geometry adjustments and checks safety constraints at each step.
    """
    print("🚀 Initializing NDH Master Runtime Engine...")
    
    # Instantiate memory conservation components and safety guardrails
    conservation = ConservationEngine()
    interceptor = SafetyInterceptor(trace_threshold=50.0)
    
    # Set an initial 80D state vector profile
    current_coordinates = np.ones(80) * 0.5
    conservation.initialize_active_surface(current_coordinates)
    
    # Mock derivatives for the 9D radial Laplacian calculations
    r_distance = 2.5
    f_prime = -0.1
    f_double_prime = 0.05

    for cycle in range(1, steps + 1):
        print(f"🌀 [Cycle {cycle}/{steps}] Evaluating trajectory elements...")
        
        # Simulate local geometric changes and vector excitations
        mock_gradient = np.random.randn(80) * 0.2
        apex_grad, radial_diff = evaluate_manifold_state(
            mock_gradient, r_distance, f_prime, f_double_prime
        )
        
        # Adjust state position coordinates along the steepest ascent axis
        current_coordinates += apex_grad * 0.1
        
        # Check security compliance limits before continuing execution paths
        if not interceptor.verify_geometric_stability(current_coordinates):
            interceptor.enforce_abort(
                f"Metric collapse or curvature explosion caught at cycle {cycle}."
            )
            
        print(f"   Stability Bounds: Norm = {np.linalg.norm(current_coordinates):.4f}")
        print(f"   Laplacian Curvature Diffusion Scalar: {radial_diff:.4f}")
        
    # Project final states to deep memory storage partitions (Lambda)
    success, volume = conservation.project_to_conservation(state_id="final_epoch")
    print(f"💾 Saving state trace. Symplectic volume preserved: {success} (Trace: {volume:.4f})")
    print("✅ System trajectory execution completed cleanly.")


def main() -> None:
    """CLI Entrypoint wrapper for running operational processing tasks."""
    try:
        execute_runtime_cycle()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        sys.exit(1)
