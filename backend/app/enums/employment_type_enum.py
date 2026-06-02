from enum import Enum


class EmploymentType(str, Enum):
    FULLTIME = "fulltime"
    PARTTIME = "parttime"
    INTERNSHIP = "internship"
    CONTRACT = "contract"
    FREELANCE = "freelance"