from django.urls import path
from .views import ProductView, ProductView2, ProductViewDetail2

urlpatterns = [
    path('product/', ProductView.as_view({'get': 'list', 'post': 'create'})),
    path('product/<int:pk>/', ProductView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('product2/', ProductView2.as_view()),
    path('product2/<int:pk>/', ProductViewDetail2.as_view()),
]