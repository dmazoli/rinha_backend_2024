from django.urls import include, path
from core import routers

from users.views import UserViewSet

router = routers.CustomRouter()
router.register(r'clientes', UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
