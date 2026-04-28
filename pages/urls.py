from django.urls import path
from .views import AboutPageView, dashboard_view, HomePageView, LoginPageView, LogoutPageView, TimesheetUpdateView, TimesheetDeleteView 

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),   
    path('about/', AboutPageView.as_view(), name='about'), 
    path('login/', LoginPageView.as_view(), name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path('timesheet/<int:pk>/edit/', TimesheetUpdateView.as_view(), name='edit_timesheet'),
    path('timesheet/<int:pk>/delete/', TimesheetDeleteView.as_view(), name='delete_timesheet'),
] 