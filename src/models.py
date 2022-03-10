from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from enum import Enum
from base64 import b64encode


class Op(str, Enum):
    create = "CREATE"
    update = "UPDATE"


class Metadata(BaseModel):
    name: Optional[str]
    generateName: Optional[str]
    namespace: str = "default"
    labels: Optional[Dict[str, str]]
    annotations: Optional[Dict[str, str]]


class Object(BaseModel):
    metadata: Metadata
    spec: Dict[str, Any]


class Request(BaseModel):
    name: Optional[str]
    namespace: str
    uid: str
    kind: Dict[str, str]
    resource: Dict[str, str]
    requestKind: Dict[str, str]
    requestResource: Dict[str, str]
    operation: Op
    userInfo: Dict[str, Any]
    object: Object
    oldObject: Optional[Dict]
    dryRun: bool
    options: Dict[str, str]


class Patch(BaseModel):
    op: str
    path: str
    value: List[Dict[str, Any]] = []

    def dump(self):
        return b64encode(f"[{self.json()}]".encode()).decode()


class Response(BaseModel):
    allowed: bool = True
    uid: Optional[str]
    patch: Optional[str]
    patchtype: Optional[str] = "JSONPatch"


class AdmissionReview(BaseModel):
    apiVersion: str = "admission.k8s.io/v1beta1"
    kind: str = "AdmissionReview"
    request: Optional[Request]
    response: Optional[Response]
