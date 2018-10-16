from django.urls import path
from . import views

urlpatterns = [
    path('systems/', views.SystemList.as_view()),
    path('types/', views.TypeList.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('items/', views.CategoryList.as_view()),
    path('portableholes/', views.PortableHoleList.as_view()),
]
