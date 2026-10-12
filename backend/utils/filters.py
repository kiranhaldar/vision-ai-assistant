"""Signal filters for smoothing hand landmark coordinates."""
import math


class OneEuroFilter:
    """Adaptive low-pass filter.

    Reduces jitter during slow movement while minimizing lag during fast
    gestures (e.g., swipes). Reference: Casiez et al., CHI 2012.
    """

    def __init__(self, min_cutoff: float = 1.0, beta: float = 0.007,
                 d_cutoff: float = 1.0):
        self.min_cutoff = min_cutoff
        self.beta = beta
        self.d_cutoff = d_cutoff
        self.x_prev: float | None = None
        self.dx_prev: float = 0.0

    def __call__(self, x: float, dt: float) -> float:
        if self.x_prev is None:
            self.x_prev = x
            return x

        dx = (x - self.x_prev) / dt
        edx = self._smoothing_factor(dx, self.dx_prev, self.d_cutoff, dt)
        cutoff = self.min_cutoff + self.beta * abs(edx)
        filtered_x = self._smoothing_factor(x, self.x_prev, cutoff, dt)

        self.x_prev = filtered_x
        self.dx_prev = edx
        return filtered_x

    @staticmethod
    def _smoothing_factor(x: float, x_prev: float, cutoff: float, dt: float) -> float:
        alpha = 1.0 / (1.0 + (1.0 / (2 * math.pi * cutoff * dt)))
        return alpha * x + (1 - alpha) * x_prev


class KalmanFilter1D:
    """Simple 1D Kalman filter (fallback / alternative to OneEuro)."""

    def __init__(self, process_noise: float = 1e-5, measurement_noise: float = 1e-3):
        self.q = process_noise
        self.r = measurement_noise
        self.x = 0.0
        self.p = 1.0

    def __call__(self, measurement: float) -> float:
        # Predict
        self.p += self.q
        # Update
        k = self.p / (self.p + self.r)
        self.x = self.x + k * (measurement - self.x)
        self.p = (1 - k) * self.p
        return self.x