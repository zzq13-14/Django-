from django.urls import path,include
from apps import views
from apps import views

urlpatterns=[
    # path('hello/',views.index),
    # path('show/',views.show_detail),
    # path('article/',views.show_article)
    path('hello/', views.hello),
    path('show/', views.show_detail),
    path('show_aticle/', views.show_article),
    path('show_aticle2/', views.show_aticle2),
    path('show_aticles/', views.show_aticles),
    path('index/', views.index),
    path('detail/<int:article_id>', views.detail2),
    path('image/', views.show_image),
    # path('detail2/<int:article_id>', views.detail2),
]