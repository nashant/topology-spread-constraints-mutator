from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from enum import Enum


class Op(str, Enum):
    create = "CREATE"
    update = "UPDATE"


class Unsatisfiable(str, Enum):
    doNotSchedule = "DoNotSchedule"
    scheduleAnyway = "ScheduleAnyway"


class TopologySpreadConstraint(BaseModel):
    labelSelector: Optional[Dict[str, str]]
    maxSkew: int
    topologyKey: str
    whenUnsatisfiable: Unsatisfiable = Unsatisfiable.doNotSchedule

    @classmethod
    def fromAnnotations(cls, annotations: Dict[str, str]):
        """Generate from `topologySpreadConstraint/` prefixed annotations

        Example:
        topologySpreadConstraint/labelSelector: app=redis,type=master
        topologySpreadConstraint/maxSkew: 3
        topologySpreadConstraint/topologyKey: zone
        topologySpreadConstraint/whenUnsatisfiable: ScheduleAnyway
        """
        annotations = {
            k.lstrip("topologySpreadConstraint/"): v
            for k, v in annotations.items()
            if k.startswith("topologySpreadConstraint/")
        }
        args = {
            "labelSelector": annotations["labelSelector"],
            "maxSkew": int(annotations.get("maxSkew", 1)),
            "topologyKey": annotations["topologyKey"],
            "whenUnsatisfiable": annotations.get("whenUnsatisfiable", Unsatisfiable.doNotSchedule)
        }
        if args["labelSelector"] != "":
            labels = args["labelSelector"].split(",")
            args["labelSelector"] = {
                l.split("=")[0]: l.split("=")[1]
                for l in labels
            }
        return cls(**args)


class Metadata(BaseModel):
    name: Optional[str]
    generateName: Optional[str]
    namespace: str = "default"
    labels: Optional[Dict[str, str]]
    annotations: Optional[Dict[str, str]]


class Pod(BaseModel):
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
    object: Pod
    oldObject: Optional[Dict]
    dryRun: bool
    options: Dict[str, str]


class Response(BaseModel):
    allowed: bool = True
    uid: str
    patch: str
    patchtype: str = "JSONPatch"


class AdmissionReview(BaseModel):
    apiVersion: str = "admission.k8s.io/v1beta1"
    kind: str = "AdmissionReview"
    request: Optional[Request]
    response: Optional[Response]


class Patch(BaseModel):
    op: str = "add"
    path: str = "/spec/topologySpreadConstraints"
    value: List[Dict[str, Any]] = []
