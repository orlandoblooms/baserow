from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from baserow.api.decorators import validate_body
from baserow.contrib.database.api.custom_actions.handler import ServerFileUploadHandler
from baserow.api.schemas import get_error_schema
from .serializers import UploadSerializer

class ServerFileUploadView(APIView):
    serializer_class = UploadSerializer

    @staticmethod
    def get_uploaded_file_as_list(request):
        return request.FILES.get('data')

    @extend_schema(
        tags=["Server File Upload"],
        operation_id="server_file_upload",
        description=(
            "Allows to upload a file, which will then be proccessed in to the 'server' and 'domain' tables"
        ),
        request=UploadSerializer,
        responses={
            200: ServerFileUploadHandler,
            400: get_error_schema(
                [
                    "ERROR_USER_NOT_IN_GROUP",
                    "ERROR_REQUEST_BODY_VALIDATION",
                    "ERROR_INVALID_INITIAL_TABLE_DATA",
                    "ERROR_INITIAL_TABLE_DATA_LIMIT_EXCEEDED",
                ]
            ),
            404: get_error_schema(["ERROR_APPLICATION_DOES_NOT_EXIST"]),
        },
    )
    @transaction.atomic
    @validate_body(UploadSerializer)
    def post(self, request, data):
        servers = self.get_uploaded_file_as_list(request)
        ServerFileUploadHandler().upload(
            servers = servers,
            user = request.user,
            name = data['name'],
            exploit = data['exploit'])
        return Response()