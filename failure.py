from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FailureData:
    id: int
    payment_hash: str
    destination: str
    msatoshi: int
    amount_msat: str
    msatoshi_sent: int
    amount_sent_msat: str
    created_at: float
    status: str
    created_at: float
    erring_index: int
    failcode: int
    erring_node: str
    erring_channel: str
    erring_direction: int
    failcodename: str


@dataclass
class Failure:
    code: int
    message: str
    data: FailureData

    @classmethod
    def from_dict(cls, dct) -> Failure:
        return Failure(**dct)
