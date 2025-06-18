from typing import Set
import httpx
from fastapi import HTTPException
from starlette import status
from app.config import settings

# cache for supported codes
_supported_codes: Set[str] | None = None

def get_supported_codes() -> Set[str]:
    # Fetch and cache a list of supported currency codes just one time in the beginning.
    global _supported_codes
    if _supported_codes is None:
        res = httpx.get(settings.ER_SUPPORTED_URL)
        res.raise_for_status()
        data = res.json()
        _supported_codes = { code for code, _ in data["supported_codes"] }
    return _supported_codes


def validate_currency_code(code: str):
    # Raise 400 if a currency code isn't in the supported list.
    if code not in get_supported_codes():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Currency '{code}' is not supported."
        )

def get_conversion_rate(frm: str, to: str = 'USD') -> float:
    validate_currency_code(frm); validate_currency_code(to)
    url = f"{settings.ER_CONVERSION_URL}/{frm}/{to}"
    resp = httpx.get(url); resp.raise_for_status()
    return resp.json()["conversion_rate"]