from django.urls import include, path
from rest_framework import routers

from users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'clientes', UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
