from enum import Enum


class Recommendation(str, Enum):
    SANGAT_SESUAI = "Sangat Sesuai"
    CUKUP_SESUAI = "Cukup Sesuai"
    DIPERTIMBANGKAN = "Dipertimbangkan"
    TIDAK_SESUAI = "Tidak Sesuai"