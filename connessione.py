from dataclasses import dataclass

from model.airport import Airport


@dataclass
class Connessione:
    VO: Airport
    V1: Airport
    N: int
