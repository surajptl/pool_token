from rest_framework import status
from rest_framework.response import Response


class RestResponse(Response):
    def __init__(self, data=None, message=None, data_status=True, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None, lead_counts=0, agent_counts=0, count=0):
        data_content = {
            'status': data_status,
            'message': message,
            'data': data
        }
        if lead_counts:
            data_content = {
                'status': data_status,
                'message': message,
                'data': data,
                'lead_counts': lead_counts
            }
        elif agent_counts:
            data_content = {
                'status': data_status,
                'message': message,
                'data': data,
                'agent_counts': agent_counts
            }
        elif count:
            data_content = {
                'status': data_status,
                'message': message,
                'data': data,
                'count': count
            }
        super(RestResponse, self).__init__(
            data=data_content
        )


class AccessDeniedResponse(RestResponse):
    status_code = status.HTTP_401_UNAUTHORIZED


class BadRequestResponse(RestResponse):
    status_code = status.HTTP_400_BAD_REQUEST


class SuccessResponse(RestResponse):
    status_code = status.HTTP_200_OK


class CreateResponse(RestResponse):
    status_code = status.HTTP_201_CREATED


class NotFoundResponse(RestResponse):
    status_code = 404


class NotImplemented(RestResponse):
    status_code = 501

class ErrorResponse(RestResponse):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

class NoContentResponse(RestResponse):
    status_code = status.HTTP_204_NO_CONTENT


class UnauthorizedResponse(RestResponse):
    status_code = status.HTTP_401_UNAUTHORIZED


class ForbiddenErrorResponse(RestResponse):
    status_code = status.HTTP_403_FORBIDDEN


class UnprocessableEntityResponse(RestResponse):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class NotAcceptableResponse(RestResponse):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
