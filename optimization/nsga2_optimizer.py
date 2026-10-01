"""pymoo NSGA-II driven by forecast-derived risk."""
import numpy as np
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

class ColdProblem(Problem):
    def __init__(self, current, ambient, future_risk):
        super().__init__(n_var=3, n_obj=2, xl=[0.1, 0.2, 0.0], xu=[1.0, 1.0, 1.0])
        self.current = current
        self.ambient = ambient
        self.future_risk = future_risk

    def _evaluate(self, x, out, *args, **kwargs):
        cooling = 3.2 * x[:, 0] * x[:, 1]
        risk = np.maximum(0.0, self.future_risk - cooling * 18.0) + np.maximum(0.0, self.current - cooling - 5.0) * 5.0
        energy = (0.25 + 0.035 * np.maximum(self.ambient - self.current, 0.0)) * (0.35 + 0.65 * x[:, 0]) * x[:, 1]
        out['F'] = np.column_stack([risk, energy])

def run_nsga2(current, ambient, future_risk, population=48, generations=30):
    problem = ColdProblem(current, ambient, future_risk)
    algorithm = NSGA2(pop_size=population)
    r = minimize(problem, algorithm, ('n_gen', generations), seed=42, verbose=False)
    
    if r.X is None or len(r.X) == 0:
        default_x = np.array([[0.1, 0.2, 0.0]])
        cooling = 3.2 * default_x[:, 0] * default_x[:, 1]
        default_risk = np.maximum(0.0, future_risk - cooling * 18.0) + np.maximum(0.0, current - cooling - 5.0) * 5.0
        default_energy = (0.25 + 0.035 * np.maximum(ambient - current, 0.0)) * (0.35 + 0.65 * default_x[:, 0]) * default_x[:, 1]
        X = default_x
        F = np.column_stack([default_risk, default_energy])
    else:
        X = np.atleast_2d(r.X)
        F = np.atleast_2d(r.F)

    rows = [
        {
            'cooling_intensity': float(x[0]),
            'compressor_duty_cycle': float(x[1]),
            'target_temperature_offset': float(x[2]),
            'safety_risk': float(f[0]),
            'estimated_energy_kwh': float(f[1])
        }
        for x, f in zip(X, F)
    ]
    max_risk = max(a['safety_risk'] for a in rows)
    max_energy = max(a['estimated_energy_kwh'] for a in rows)
    rec = min(
        rows,
        key=lambda z: 0.65 * z['safety_risk'] / (max_risk + 1e-9) + 0.35 * z['estimated_energy_kwh'] / (max_energy + 1e-9)
    )
    return rows, rec
