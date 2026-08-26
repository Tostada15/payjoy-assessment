from fastapi  import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from typing import Optional



class ConversionResponse(BaseModel):
    amount_usd: float
    currency: str
    converted: float
    rate: float

#load env variables
load_dotenv()

app = FastAPI(title = "PayJoy-Assessment-Exchange-Currency-API")
EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")
EXCHANGERATE_API_URL = os.getenv("EXCHANGERATE_API_URL")

if not EXCHANGERATE_API_KEY:
    raise RuntimeError("EXCHANGERATE_API_KEY not found in .env file")

@app.get("/convert", response_model=ConversionResponse)

async def convert(amount: float, currency: str):
    """
    Convert an amount from USD to a target currency.
    
    Parameters:
    - amount: Amount in USD (must be > 0)
    - currency: Target currency code (e.g., BRL, MXN, COP)
    
    Returns:
    - amount_usd: Original amount in USD
    - currency: Target currency code
    - converted: Converted amount in target currency
    - rate: Exchange rate used
    """
    
    # amount positive
    if amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be greater than 0"
        )
    
    # currency not empty
    if not currency or len(currency) != 3:
        raise HTTPException(
            status_code=400,
            detail="Currency must be a valid 3-letter ISO 4217 code"
        )
    
    try:
        # call ExchangeRate API
        url = f"{EXCHANGERATE_API_URL}/{EXCHANGERATE_API_KEY}/latest/USD"
        response = requests.get(url, timeout=5)
        
        # validate response
        if response.status_code != 200:
            raise HTTPException(
                status_code=502,
                detail="Failed to fetch exchange rates from external API"
            )
        
        data = response.json()
        
        # check currency
        if data.get("result") != "success":
            raise HTTPException(
                status_code=400,
                detail=f"Invalid currency code: {currency}"
            )
        
        rates = data.get("conversion_rates", {})
        if currency not in rates:
            raise HTTPException(
                status_code=400,
                detail=f"Currency '{currency}' is not supported"
            )
        
        # convertion
        rate = rates[currency]
        converted_amount = round(amount * rate, 2)
        
        return ConversionResponse(
            amount_usd=amount,
            currency=currency,
            converted=converted_amount,
            rate=rate
        )
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error connecting to exchange rate service: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)