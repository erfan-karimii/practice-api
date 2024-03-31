from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views

urlpatterns = [
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:id>/', views.SnippetDetail.as_view()),
    path('snippets/<int:id>/high/', views.SnippetHighlight.as_view()),
    path('users/', views.UserListView.as_view()),
    path('users/<int:id>/', views.UserDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)