from rest_framework.routers import SimpleRouter
from bartender.drinks import views


router = SimpleRouter()

router.register(r"crate", views.CrateViewSet)
