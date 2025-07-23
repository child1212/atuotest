from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('devices/', views.device_list_view,name='devices'),
    path('devices/<str:pk>',views.device_list_view_plt,name='devices_pl'),
    path('devices_oversea/',views.DeviceListViewOversea.as_view(),name='devices_oversea'),
    path('devices_iOS/',views.DeviceListViewIOS.as_view(),name='devices_iOS'),
    path('devices/search/',views.search_device, name='deviceSearch'),
    path('genre/',views.GenreListView.as_view(), name='genre'),
    path('genre/<int:pk>',views.GenreDetailView.as_view(), name='genre-detail'),
    path('genre/<int:pk>/refresh/',views.init_device_status, name='genre-refresh'),
    path('device/borrow/',views.borrow_device, name='borrow'),
    path('device/<str:pk>/lendhistory/',views.lend_history, name='device-lendhistory'),
    path('lendhistory/',views.LendHistoryListView.as_view(), name='lendhistory'),
    path('lendhistory/<str:pk>',views.LendHistoryDetailView.as_view(), name='lendhistory-detail'),
    path('device/<str:pk>',views.device_detail, name='device-detail'),
    path('logout/',views.logout_view, name='logouta')
]