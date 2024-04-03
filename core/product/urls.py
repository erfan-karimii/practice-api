from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from product import views

urlpatterns = [
    path('product-list/', views.ListProductView.as_view()),
    path('product-detail/<id>/', views.DetailProductView.as_view()),
    path('product-cat-list/<id>/', views.ListProductCategoryView.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)