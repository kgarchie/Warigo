from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('apply/', views.apply, name='apply'),

    path('history/', views.history, name='history'),
    path('history/pending/', views.view_pending, name='view_pending'),
    path('history/approved/', views.view_approved, name='view_approved'),
    path('history/rejected/', views.view_rejected, name='view_rejected'),
    path('history/appealed/', views.view_appealed, name='view_appealed'),

    path('about/', views.about, name='about'),
    path('login/', views.login_function, name='login'),
    path('logout/', views.logout_function, name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('application/<int:pk>/', views.application_detail, name='application_detail'),
    path('application/<int:pk>/update/', views.application_update, name='application_update'),
    path('application/<int:pk>/delete/', views.application_delete, name='application_delete'),
    path('application/<int:pk>/approve/', views.application_approve, name='application_approve'),
    path('application/<int:pk>/reject/', views.application_reject, name='application_reject'),
    path('application/<int:pk>/appeal/', views.application_appeal, name='application_appeal'),

    path('search/', views.search, name='search'),
    path('search/history/', views.search_history, name='search_history'),
    path('search/pending/', views.search_pending, name='search_pending'),
    path('search/approved/', views.search_approved, name='search_approved'),
    path('search/rejected/', views.search_rejected, name='search_rejected'),
    path('search/appealed/', views.search_appealed, name='search_appealed'),

    path('events/', views.events, name='events'),
    path('events/<int:pk>/', views.event_details, name='event_details'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('events/create/', views.create_event, name='create_event'),
]
