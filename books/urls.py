from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, BookListView

router = DefaultRouter()
router.register(r"books", BookViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
]