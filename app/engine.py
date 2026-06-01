import asyncio
import pickle
from pathlib import Path
from typing import Optional

import numpy as np

from .schema import InputFeatures, OutputPredicted

MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"


class Engine:
    """Loads the trained mangrove carbon-stock model and serves predictions.

    The pickle is a bundle holding the fitted ``XGBRegressor`` plus the
    metadata needed to reproduce the training-time feature pipeline:
    feature order, the raw bands, per-feature medians for imputation, the
    SAVI soil factor, and the ``log1p`` target transform.
    """

    def __init__(self, model_path: Path = MODEL_PATH):
        with open(model_path, "rb") as f:
            bundle = pickle.load(f)

        self.model = bundle["model"]
        self.feature_order: list[str] = bundle["feature_order"]
        self.raw_bands: list[str] = bundle["raw_bands"]
        self.feature_medians: dict[str, float] = bundle["feature_medians"]
        self.savi_L: float = bundle["savi_L"]
        self.target_transform: Optional[str] = bundle.get("target_transform")
        self.VERSION = str(bundle.get("metadata", {}).get("trained_at_utc", ""))

    # --- Feature engineering ------------------------------------------------
    def _compute_indices(self, values: dict[str, float]) -> dict[str, float]:
        """Fill NDVI/NDWI/SAVI from the raw bands when not supplied."""
        eps = 1e-9
        b3, b4, b8 = values.get("B3"), values.get("B4"), values.get("B8")

        if values.get("NDVI") is None and b8 is not None and b4 is not None:
            values["NDVI"] = (b8 - b4) / (b8 + b4 + eps)
        if values.get("NDWI") is None and b3 is not None and b8 is not None:
            values["NDWI"] = (b3 - b8) / (b3 + b8 + eps)
        if values.get("SAVI") is None and b8 is not None and b4 is not None:
            L = self.savi_L
            values["SAVI"] = (b8 - b4) * (1 + L) / (b8 + b4 + L + eps)
        return values

    def _build_row(self, data: InputFeatures) -> np.ndarray:
        """Assemble a single feature row in the model's expected order.

        Missing values (including indices that could not be derived) fall back
        to the training-time medians stored in the bundle.
        """
        values = data.model_dump()
        values = self._compute_indices(values)

        row = [
            values.get(name)
            if values.get(name) is not None
            else self.feature_medians[name]
            for name in self.feature_order
        ]
        return np.asarray([row], dtype=float)

    # --- Prediction ---------------------------------------------------------
    def _predict(self, data: InputFeatures) -> OutputPredicted:
        X = self._build_row(data)
        pred = float(self.model.predict(X)[0])

        if self.target_transform == "log1p":
            pred = float(np.expm1(pred))

        return OutputPredicted(total_carbon_stock=pred, model_version=self.VERSION)

    def invoke(self, data: InputFeatures) -> OutputPredicted:
        return self._predict(data)

    async def ainvoke(self, data: InputFeatures) -> OutputPredicted:
        # XGBoost predict is CPU-bound and synchronous; off-load to a thread
        # so the event loop is not blocked.
        return await asyncio.to_thread(self._predict, data)

    def __call__(self, data: InputFeatures) -> OutputPredicted:
        return self._predict(data)

    def __repr__(self) -> str:
        return f"Engine(model=XGBRegressor, version={self.VERSION!r})"
