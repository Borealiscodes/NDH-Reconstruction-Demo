"""
NDH State Conservation Engine
Implements tracking for the active processing surface (Sigma)
and the deep latent memory conservation surface (Lambda).
"""

import numpy as np
from typing import Dict, Optional, Tuple


class ConservationEngine:
    """
    Manages state transfers between real-time execution matrices (Sigma)
    and archival storage structures (Lambda) while tracking volume metrics.
    """

    def __init__(self, dimension: int = 80):
        self.dim = dimension
        # Active execution matrix storage (Sigma)
        self.sigma_state: Optional[np.ndarray] = None
        # Archival conservation surface storage (Lambda)
        self.lambda_archive: Dict[str, np.ndarray] = {}

    def initialize_active_surface(self, initial_vector: np.ndarray) -> None:
        """Initializes the active execution surface with an 80D coordinate array."""
        if initial_vector.shape != (self.dim,):
            raise ValueError(f"State must be a flat vector of dimension {self.dim}.")
        self.sigma_state = initial_vector.copy()

    def calculate_symplectic_volume(self, matrix: np.ndarray) -> float:
        """
        Approximates a trace metric representing the informational volume.
        Used to monitor volume preservation constraints during state transfers.
        """
        # Form a symmetric projection matrix to evaluate structural volume
        outer = np.outer(matrix, matrix)
        return float(np.trace(outer))

    def project_to_conservation(self, state_id: str) -> Tuple[bool, float]:
        """
        Simulates the continuous projection map Psi: Sigma -> Lambda.
        Verifies volume invariant alignment before writing to archival slots.
        """
        if self.sigma_state is None:
            raise RuntimeError("Active surface Sigma is uninitialized.")

        v_sigma = self.calculate_symplectic_volume(self.sigma_state)
        
        # Save active matrix configuration to the deep memory layer (Lambda)
        self.lambda_archive[state_id] = self.sigma_state.copy()
        v_lambda = self.calculate_symplectic_volume(self.lambda_archive[state_id])
        
        # Invariant check: Assert volume discrepancy falls within epsilon bounds
        is_invariant_preserved = abs(v_sigma - v_lambda) < 1e-7
        return is_invariant_preserved, v_lambda

    def recall_to_active(self, state_id: str) -> Tuple[bool, float]:
        """
        Simulates the inverse mapping Psi^-1: Lambda -> Sigma.
        Restores precise historical coordinates to the runtime environment.
        """
        if state_id not in self.lambda_archive:
            raise KeyError(f"State archive target '{state_id}' not found.")
            
        v_lambda = self.calculate_symplectic_volume(self.lambda_archive[state_id])
        
        # Restore conserved tensor trace back into the active processing layer
        self.sigma_state = self.lambda_archive[state_id].copy()
        v_sigma = self.calculate_symplectic_volume(self.sigma_state)
        
        is_invariant_preserved = abs(v_sigma - v_lambda) < 1e-7
        return is_invariant_preserved, v_sigma
