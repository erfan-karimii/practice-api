from django.urls import path
from snippets import views

urlpatterns = [
    path('snippets-list/', views.SnippetList.as_view()),
    path('snippets/<int:id>/', views.SnippetDetail.as_view()),
    path('snippets/<int:id>/high/', views.SnippetHighlight.as_view()),
    path('users-list/', views.UserListView.as_view()),
    path('users/<int:id>/', views.UserDetailView.as_view()),
]

