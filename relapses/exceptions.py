from rest_framework import status
from rest_framework.exceptions import APIException

class NoDataForReport(APIException):
    status_code = status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
    default_detail = 'No data for report'
