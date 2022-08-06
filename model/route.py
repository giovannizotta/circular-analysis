from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class RouteHop:
    id: str
    alias: str
    short_channel_id: str
    millisatoshi: int
    delay: int
    fee: int
    ppm: int

    @classmethod
    def from_dict(cls, dct) -> RouteHop:
        return RouteHop(**dct)


@dataclass
class Route:
    payment_hash: str
    source_id: str
    destination_id: str
    source_alias: str
    destination_alias: str
    amount_sat: int
    fee_msat: int
    ppm: int
    hops: List[RouteHop]

    @classmethod
    def from_dict(cls, dct) -> Route:
        return Route(**dct)
