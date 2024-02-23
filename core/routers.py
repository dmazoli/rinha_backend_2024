from rest_framework.routers import DefaultRouter


class CustomRouter(DefaultRouter):
    def __init__(self, *args, **kwargs):
        super(CustomRouter, self).__init__(*args, **kwargs)
        self.trailing_slash = '/?'
