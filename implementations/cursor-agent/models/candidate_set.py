from dataclasses import dataclass


@dataclass
class CandidateSet:
    flights: list
    activities: list
    stays: list
    transportation: list
