from django.conf.urls import url

from .views import ServerFileUploadView


app_name = "baserow.contrib.database.api.custom_actions"

urlpatterns = [
    url(r"server_file_upload/$", ServerFileUploadView.as_view(), name="list"),
]
