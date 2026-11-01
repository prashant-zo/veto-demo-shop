import logging
import os
import uuid

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
log = logging.getLogger("checkout")

PRICING_URL = os.environ.get("PRICING_URL", "http://pricing:8080")
PAYMENTS_URL = os.environ.get("PAYMENTS_URL", "http://payments:8080")

app = FastAPI()
client = httpx.Client(timeout=2.0)


class Order(BaseModel):
    item: str
    qty: int = 1


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.post("/checkout")
def checkout(order: Order):
    r = client.get(f"{PRICING_URL}/price", params={"item": order.item})
    if r.status_code != 200:
        log.warning("price lookup failed item=%s status=%s", order.item, r.status_code)
        raise HTTPException(status_code=502, detail="pricing unavailable")
    total = round(r.json()["price"] * order.qty, 2)

    p = client.post(f"{PAYMENTS_URL}/charge", json={"amount": total})
    if p.status_code != 200:
        log.error("payment failed item=%s total=%s status=%s", order.item, total, p.status_code)
        raise HTTPException(status_code=502, detail="payment failed")

    order_id = uuid.uuid4().hex[:8]
    log.info("order confirmed id=%s item=%s total=%s", order_id, order.item, total)
    return {"order_id": order_id, "status": "confirmed", "total": total}
