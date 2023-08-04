from rest_framework.routers import DefaultRouter
from .views import ConferenceViewSet


router = DefaultRouter()
router.register('', ConferenceViewSet, basename="api")

urlpatterns = router.urls
