from django.urls import path
from product import views

urlpatterns = [
    path('product-list/', views.ListProductView.as_view()),
    path('product-detail/<id>/', views.DetailProductView.as_view()),
    path('product-class-list/', views.ListProductClassView.as_view()),
    path('product-attr-list/', views.ListProductAttributeView.as_view()),
    path('product-attr-detail/<int:id>/', views.DetailProductAttributeView.as_view()),
    path('product-attr-value-list/<int:product_id>/', views.ListRelatedProductAttributeValue.as_view()),
    path('product-attr-value-list/', views.ListProductAttributeValue.as_view()),
    path('product-attr-value-detail/<int:id>', views.DetailProductValueAttribute.as_view()),

    
    
    # path('product-cat-list/<id>/', views.ListProductCategoryView.as_view()),
    
]

