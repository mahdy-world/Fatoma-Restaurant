from django.urls import path
from .views import *


app_name = 'Website'
urlpatterns = [
    path('', HomePage.as_view(), name='HomePage'),
    path('shop/', Shop.as_view(), name='Shop'),
    path('<int:pk>/products/', ProductList.as_view(), name='ProductList'),
    path('product/<int:pk>/', ProductView.as_view(), name='ProductView'),
    path('add_to_cart/', AddToCart.as_view(), name='AddToCart'),
    path('search/', Search.as_view(), name='Search'),
    path('home_page_update/<int:pk>/', HomePageUpdate.as_view(), name='HomePageUpdate'),

    path('about/list', AboutItemsList.as_view(), name='AboutItemsList'),
    path('about/create', AboutItemsCreate.as_view(), name='AboutItemsCreate'),
    path('about/update/<int:pk>', AboutItemsUpdate.as_view(), name='AboutItemsUpdate'),
    path('about/delete/<int:pk>', AboutItemsDelete.as_view(), name='AboutItemsDelete'),

    path('statistics/list', StatisticsItemsList.as_view(), name='StatisticsItemsList'),
    path('statistics/create', StatisticsItemsCreate.as_view(), name='StatisticsItemsCreate'),
    path('statistics/update/<int:pk>', StatisticsItemsUpdate.as_view(), name='StatisticsItemsUpdate'),
    path('statistics/delete/<int:pk>', StatisticsItemsDelete.as_view(), name='StatisticsItemsDelete'),

    path('service/list', ServiceItemsList.as_view(), name='ServiceItemsList'),
    path('service/create', ServiceItemsCreate.as_view(), name='ServiceItemsCreate'),
    path('service/update/<int:pk>', ServiceItemsUpdate.as_view(), name='ServiceItemsUpdate'),
    path('service/delete/<int:pk>', ServiceItemsDelete.as_view(), name='ServiceItemsDelete'),

    path('product/list', ProductItemsList.as_view(), name='ProductItemsList'),
    path('product/create', ProductItemsCreate.as_view(), name='ProductItemsCreate'),
    path('product/update/<int:pk>', ProductItemsUpdate.as_view(), name='ProductItemsUpdate'),
    path('product/delete/<int:pk>', ProductItemsDelete.as_view(), name='ProductItemsDelete'),

    path('team/list', TeamItemsList.as_view(), name='TeamItemsList'),
    path('team/create', TeamItemsCreate.as_view(), name='TeamItemsCreate'),
    path('team/update/<int:pk>', TeamItemsUpdate.as_view(), name='TeamItemsUpdate'),
    path('team/delete/<int:pk>', TeamItemsDelete.as_view(), name='TeamItemsDelete'),
]