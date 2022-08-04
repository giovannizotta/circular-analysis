import json
from typing import Dict, Tuple, List

from failure import Failure
from route import Route
from success import Success


def get_dict_from_file(filename) -> Dict[str, any]:
    with open(filename) as f:
        return json.load(f)


def parse_data(filename) -> Tuple[List[Success], List[Failure], List[Route]]:
    data = get_dict_from_file(filename)
    successes: List[Success] = []
    for s in data['successes']:
        success = Success.from_dict(s)
        successes.append(success)

    failures: List[Failure] = []
    for s in data['failures']:
        failure = Failure.from_dict(s)
        failures.append(failure)

    routes: List[Route] = []
    for s in data['routes']:
        route = Route.from_dict(s)
        routes.append(route)

    return successes, failures, routes
