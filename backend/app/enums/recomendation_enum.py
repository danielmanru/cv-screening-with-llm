from enum import Enum
from subprocess import HIGH_PRIORITY_CLASS


class Recommendation(str, Enum):
    HIGHLY_SUITABLE = "Highly Suitable"
    SUITABLE = "Suitable"
    CONSIDER = "Consider"
    NOT_SUITABLE = "Not Suitable"