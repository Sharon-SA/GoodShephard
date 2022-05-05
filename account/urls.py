from django.template.defaulttags import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#app_name = 'account'
from .views import export_client_visits_report_csv

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('client_list', views.client_list, name='client_list'),
    path('client/<int:pk>/edit/', views.client_edit, name='client_edit'),
    path('client/<int:pk>/delete/', views.client_delete, name='client_delete'),
    path('client/create/', views.client_new, name='client_new'),
    path('client_search', views.client_search, name='client_search'),
    path('client/<int:pk>/orders/', views.client_orders, name='client_orders'),
    path('inventory_list', views.inventory_list, name='inventory_list'),
    path('order_list', views.order_list, name='order_list'),
    path('order/<int:pk>/create/', views.order_new, name='order_new'),
    path('order/<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('order/<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('inventory/<int:pk>/edit/', views.inventory_edit, name='inventory_edit'),
    path('inventory/<int:pk>/delete/', views.inventory_delete, name='inventory_delete'),
    path('order/<int:pk>/download/', views.download_orderReport, name='download_report'),
    path('orders_list_download', views.download_allorderReport, name='download_all_report'),
    path('reports/',views.viewReport, name='reports'),
    path('reports/clientvisits/', views.client_visits_report, name='client_visit_report'),
    path('reports/ordersfulfilled', views.client_orders_fulfilled, name='orders_report'),
    path('reports/inventory', views.inventory_report, name='inventory_report'),
    path(
        "reports/client_visits/csv",
        views.export_client_visits_report_csv,
        name="export_client_visits_report_csv",
    ),
    path(
        "reports/orders_list/csv",
        views.export_orders_list_report_csv,
        name="export_order_csv",
    ),
    path(
        "reports/inventory_list/csv",
        views.export_inventory_list_report_csv,
        name="export_inventory_report_csv",
    ),

]

urlpatterns += staticfiles_urlpatterns()
