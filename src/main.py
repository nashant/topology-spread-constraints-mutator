from fastapi import FastAPI, Response, HTTPException
from base64 import b64encode
from json import dumps
from jsonpatch import JsonPatch

from models import AdmissionReview, Patch, TopologySpreadConstraint, Response as ARResponse
from utils import verify_chain

app = FastAPI()
app.host = "0.0.0.0"

@app.get("/")
async def root():
    return {"message": "Nothing to see"}

@app.get("/health", status_code=204, response_class=Response)
async def health() -> None:
    if verify_chain():
        return
    raise HTTPException(status_code=400, detail="Certificate chain not valid")

@app.post("/mutate")
async def mutate(body: dict) -> None:
    ar = AdmissionReview(**body)
    pod = ar.request.object

    constraints = []
    if pod.metadata.annotations is not None:
        constraints.append(TopologySpreadConstraint.fromAnnotations(pod.metadata.annotations))
    patch = dumps([Patch(value=constraints)])
    patch = str(patch).encode()
    response = {
        "uid": ar.request.uid,
        "patch": b64encode(patch).decode()
    }
    response = AdmissionReview(response=response)
    return response
