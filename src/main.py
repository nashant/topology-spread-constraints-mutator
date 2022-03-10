import logging
from fastapi import FastAPI, Response, HTTPException
from json import loads

from models import AdmissionReview, Patch, Response as ARResponse
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

    spec = pod.metadata.annotations.get("topologySpreadConstraints/spec", None)
    op = pod.metadata.annotations.get("topologySpreadConstraints/op", "add")
    path = pod.metadata.annotations.get("topologySpreadConstraints/path", "/spec/topologySpreadConstraints")

    if spec is None :
        return AdmissionReview(response={"uid": ar.request.uid, "patchType": None}).json()

    patch = Patch(op=op, path=path, value=loads(spec))
    response = ARResponse(uid=ar.request.uid, patch=patch.dump())

    logging.info(msg=f"Applying patch: {patch}")
    return AdmissionReview(response=response).json()
