import logging
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
log = logging.getLogger("payments")

app = FastAPI()
charges = {"count": 0, "amount": 0.0}


class Charge(BaseModel):
    amount: float


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.get("/stats")
def stats():
    return charges


@app.post("/charge")
def charge(c: Charge):
    if c.amount <= 0:
        log.warning("rejected charge amount=%s", c.amount)
        raise HTTPException(status_code=400, detail="bad amount")
    charge_id = uuid.uuid4().hex[:8]
    charges["count"] += 1
    charges["amount"] = round(charges["amount"] + c.amount, 2)
    log.info("charged id=%s amount=%s", charge_id, c.amount)
    return {"charge_id": charge_id, "status": "ok"}
