from rest_framework.routers import SimpleRouter
from .views import UserViewSet, TransactionViewSet, InviteViewSet

router = SimpleRouter()

router.register(r"user", UserViewSet)
router.register(r"transaction", TransactionViewSet)
router.register(r"invite", InviteViewSet)
