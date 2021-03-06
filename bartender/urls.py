from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from .routers import ExtendableRouter

from .users.api import router as users_router
from .drinks.api import router as drinks_router
from .users.views import retrieve_token

router = ExtendableRouter()
router.extend(users_router)
router.extend(drinks_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/v1/", include(router.urls)),
    path("api/v1/token/", retrieve_token),
    path(r"^api/hijack/", include("hijack.urls", namespace="hijack")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
