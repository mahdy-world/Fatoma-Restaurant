from .views import *
from django.urls import path

app_name = 'Branches'
urlpatterns = [
    path('branches/', BranchList.as_view(), name='BranchList'),
    path('branches/new/', BranchCreate.as_view(), name='BranchCreate'),
    path('branches/trash/', BranchTrashList.as_view(), name='BranchTrashList'),
    path('branches/<int:pk>/edit/', BranchUpdate.as_view(), name='BranchUpdate'),
    path('branches/<int:pk>/delete/', BranchDelete.as_view(), name='BranchDelete'),
    path('branches/xls', BranchXls, name='BranchXls'),

    path('treasuries/', TreasuryList.as_view(), name='TreasuryList'),
    path('treasuries/new/', TreasuryCreate.as_view(), name='TreasuryCreate'),
    path('treasuries/trash/', TreasuryTrashList.as_view(), name='TreasuryTrashList'),
    path('treasuries/<int:pk>/edit/', TreasuryUpdate.as_view(), name='TreasuryUpdate'),
    path('treasuries/<int:pk>/delete/', TreasuryDelete.as_view(), name='TreasuryDelete'),
    path('treasuries/xls', TreasuryXls, name='TreasuryXls'),
    ]