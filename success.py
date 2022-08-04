from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Success:
    id: int
    payment_hash: str
    destination: str
    msatoshi: int
    amount_msat: str
    msatoshi_sent: int
    amount_sent_msat: str
    created_at: float
    status: str
    payment_preimage: str

    @classmethod
    def from_dict(cls, dct) -> Success:
        return Success(**dct)
