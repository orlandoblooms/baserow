from django.urls import path, include

from .tables import urls as table_urls
from .views import urls as view_urls
from .fields import urls as field_urls
from .rows import urls as row_urls
from .tokens import urls as token_urls
from .custom_actions import urls as custom_actions_urls

app_name = "baserow.contrib.database.api"

urlpatterns = [
    path("tables/", include(table_urls, namespace="tables")),
    path("views/", include(view_urls, namespace="views")),
    path("fields/", include(field_urls, namespace="fields")),
    path("rows/", include(row_urls, namespace="rows")),
    path("tokens/", include(token_urls, namespace="tokens")),
    path("custom_actions/", include(custom_actions_urls, namespace="custom_actions")),
]
