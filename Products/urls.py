from .views import *
from django.urls import path



app_name = 'Products'
urlpatterns = [
    path('main_categories/', MainCategoryList.as_view(), name='MainCategoryList'),
    path('main_categories/new/', MainCategoryCreate.as_view(), name='MainCategoryCreate'),
    path('main_categories/trash/', MainCategoryTrashList.as_view(), name='MainCategoryTrashList'),
    path('main_categories/<int:pk>/edit/', MainCategoryUpdate.as_view(), name='MainCategoryUpdate'),
    path('main_categories/<int:pk>/delete/', MainCategoryDelete.as_view(), name='MainCategoryDelete'),
    path('main_categories/xls', MainCategoryXls , name='MainCategoryXls'),
    
    path('sub_categories/', SubCategoryList.as_view(), name='SubCategoryList'),
    path('sub_categories/new/', SubCategoryCreate.as_view(), name='SubCategoryCreate'),
    path('sub_categories/trash/', SubCategoryTrashList.as_view(), name='SubCategoryTrashList'),
    path('sub_categories/<int:pk>/edit/', SubCategoryUpdate.as_view(), name='SubCategoryUpdate'),
    path('sub_categories/<int:pk>/delete/', SubCategoryDelete.as_view(), name='SubCategoryDelete'),
    path('sub_categories/xls', SubCategoryXls , name='SubCategoryXls'),

    path('manufactures/', ManufactureList.as_view(), name='ManufactureList'),
    path('manufactures/new/', ManufactureCreate.as_view(), name='ManufactureCreate'),
    path('manufactures/trash/', ManufactureTrashList.as_view(), name='ManufactureTrashList'),
    path('manufactures/<int:pk>/edit/', ManufactureUpdate.as_view(), name='ManufactureUpdate'),
    path('manufactures/<int:pk>/delete/', ManufactureDelete.as_view(), name='ManufactureDelete'),
    path('manufactures/xls', ManufactureXls , name='ManufactureXls'),

    path('brands/', BrandList.as_view(), name='BrandList'),
    path('brands/new/', BrandCreate.as_view(), name='BrandCreate'),
    path('brands/trash/', BrandTrashList.as_view(), name='BrandTrashList'),
    path('brands/<int:pk>/edit/', BrandUpdate.as_view(), name='BrandUpdate'),
    path('brands/<int:pk>/delete/', BrandDelete.as_view(), name='BrandDelete'),
    path('brands/xls', BrandXls , name='BrandXls'),

    path('units/', UnitList.as_view(), name='UnitList'),
    path('units/new/', UnitCreate.as_view(), name='UnitCreate'),
    path('units/<int:pk>/edit/', UnitUpdate.as_view(), name='UnitUpdate'),
    path('units/<int:pk>/delete/', UnitDelete.as_view(), name='UnitDelete'),

    path('products/', ProductList.as_view(), name='ProductList'),
    path('products/new/', ProductCreate.as_view(), name='ProductCreate'),
    path('products/trash/', ProductTrashList.as_view(), name='ProductTrashList'),
    path('products/<int:pk>/edit/', ProductUpdate.as_view(), name='ProductUpdate'),
    path('products/<int:pk>/delete/', ProductDelete.as_view(), name='ProductDelete'),
    path('products/<int:pk>/show/', ProductCard.as_view(), name='ProductCard'),
    path('products/<int:pk>/add_content/', GroupedProductCreate.as_view(), name='GroupedProductCreate'),
    path('product/xls', ProductXls, name='ProductXls'),

    path('grouped_product/<int:pk>/edit/', GroupedProductUpdate.as_view(), name='GroupedProductUpdate'),
    path('grouped_product/<int:pk>/delete/', GroupedProductDelete, name='GroupedProductDelete'),

    path('taxes/', TaxesList.as_view(), name='TaxesList'),
    path('tax/new/', TaxCreate.as_view(), name='TaxCreate'),
    path('tax/<int:pk>/edit/', TaxUpdate.as_view(), name='TaxUpdate'),
    path('tax/delete/<int:id>/', TaxDelete , name='TaxDelete'),
    path('tax/xls', TaxXls , name='TaxXls'),

    path('prices_product/<int:pk>/<int:ppk>/edit/', PricesProductUpdate.as_view(), name='PricesProductUpdate'),
    path('prices_product/<int:pk>/<int:ppk>/delete/', PricesProductDelete.as_view(), name='PricesProductDelete'),
    path('prices_product/<int:pk>/<int:ppk>/stop/', PricesProductStop.as_view(), name='PricesProductStop'),
    path('prices_product/<int:pk>/<int:ppk>/active/', PricesProductActive.as_view(), name='PricesProductActive'),

]
