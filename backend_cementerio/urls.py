from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views.users import UserView, login
from .views.dceasced import DceascedView, DocumentView
from .views.grave import GraveView
from .views.locations import RowView, BlockView, SectionView
from .views.reports import GeneralReportView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', UserView)
router.register('dceasced', DceascedView)
router.register('documents', DocumentView)
router.register('graves', GraveView)
router.register('rows', RowView)
router.register('blocks', BlockView)
router.register('sections', SectionView)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/admin/dceasced/docs/', DocumentView.getDocsByDceasced),
    path('api/admin/register/', UserView.register),
    path('api/admin/login/', login),
    path('api/admin/ascend/', UserView.ascend),
    path('api/reports/', GeneralReportView.get),
] 
