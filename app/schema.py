from typing import Optional

from pydantic import BaseModel, Field


class InputFeatures(BaseModel):
    """Input features for the mangrove carbon-stock model (XGBRegressor).

    The 14 ``raw_bands`` below are the values the caller is expected to
    provide. The three spectral indices (``NDVI``, ``NDWI``, ``SAVI``) are
    derived from the raw bands by the engine and are therefore optional; pass
    them only to override the computed values. Any field left as ``None`` is
    imputed by the engine using the model's stored feature medians.
    """

    # --- Geolocation -----------------------------------------------------
    longitude: Optional[float] = Field(
        None, ge=-180, le=180, description="Longitude in decimal degrees (EPSG:4326)."
    )
    latitude: Optional[float] = Field(
        None, ge=-90, le=90, description="Latitude in decimal degrees (EPSG:4326)."
    )

    # --- Sentinel-2 surface reflectance bands (0..1) ---------------------
    B2: Optional[float] = Field(None, description="Sentinel-2 Blue reflectance (490 nm).")
    B3: Optional[float] = Field(None, description="Sentinel-2 Green reflectance (560 nm).")
    B4: Optional[float] = Field(None, description="Sentinel-2 Red reflectance (665 nm).")
    B5: Optional[float] = Field(None, description="Sentinel-2 Red-edge 1 reflectance (705 nm).")
    B6: Optional[float] = Field(None, description="Sentinel-2 Red-edge 2 reflectance (740 nm).")
    B7: Optional[float] = Field(None, description="Sentinel-2 Red-edge 3 reflectance (783 nm).")
    B8: Optional[float] = Field(None, description="Sentinel-2 NIR reflectance (842 nm).")
    B8A: Optional[float] = Field(None, description="Sentinel-2 NIR narrow reflectance (865 nm).")
    B11: Optional[float] = Field(None, description="Sentinel-2 SWIR 1 reflectance (1610 nm).")
    B12: Optional[float] = Field(None, description="Sentinel-2 SWIR 2 reflectance (2190 nm).")

    # --- Sentinel-1 SAR backscatter (dB) ---------------------------------
    VV: Optional[float] = Field(None, description="Sentinel-1 VV backscatter in dB.")
    VH: Optional[float] = Field(None, description="Sentinel-1 VH backscatter in dB.")

    # --- Derived spectral indices (computed by the engine if omitted) ----
    NDVI: Optional[float] = Field(
        None, description="Normalized Difference Vegetation Index = (B8 - B4) / (B8 + B4)."
    )
    NDWI: Optional[float] = Field(
        None, description="Normalized Difference Water Index = (B3 - B8) / (B3 + B8)."
    )
    SAVI: Optional[float] = Field(
        None,
        description="Soil-Adjusted Vegetation Index = (B8 - B4) * (1 + L) / (B8 + B4 + L), L=0.5.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "longitude": -6.05,
                "latitude": 4.97,
                "B2": 0.036,
                "B3": 0.054,
                "B4": 0.042,
                "B5": 0.096,
                "B6": 0.211,
                "B7": 0.242,
                "B8": 0.240,
                "B8A": 0.265,
                "B11": 0.125,
                "B12": 0.062,
                "VV": -7.65,
                "VH": -14.51,
            }
        }
    }


class OutputPredicted(BaseModel):
    """Model prediction output."""

    total_carbon_stock: float = Field(
        ..., description="Predicted total carbon stock (target units, back-transformed from log1p)."
    )
    model_version: Optional[str] = Field(
        None, description="Version identifier of the model that produced the prediction."
    )
