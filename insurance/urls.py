from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, PolicyProductViewSet, CustomerPolicyViewSet


router = DefaultRouter()
router.register("customers", CustomerViewSet, basename="customer")
router.register("products", PolicyProductViewSet, basename="product")
router.register("policies", CustomerPolicyViewSet, basename="policy")


urlpatterns = router.urls