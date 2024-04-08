from django.urls import path
from product import views

urlpatterns = [
    path('product-list/', views.ListProductView.as_view()),
    path('product-detail/<id>/', views.DetailProductView.as_view()),
    path('product-class-list/', views.ListProductClassView.as_view()),
    path('product-attr-list/', views.ListProductAttribute.as_view()),

    
    # path('product-cat-list/<id>/', views.ListProductCategoryView.as_view()),
    
]

