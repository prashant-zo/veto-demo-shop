import logging

from fastapi import FastAPI, HTTPException

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
log = logging.getLogger("pricing")

PRICES = {"tea": 4.50, "coffee": 6.00, "cake": 8.25, "cookie": 2.75}

app = FastAPI()


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.get("/price")
def price(item: str):
    if item not in PRICES:
        log.warning("unknown item=%s", item)
        raise HTTPException(status_code=404, detail="unknown item")
    return {"item": item, "price": PRICES[item]}
