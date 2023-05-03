from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
path('', views.LeadListView.as_view(), name='leadList'),
path('create/', views.LeadCreateView.as_view(), name='createLead'),
path('<int:pk>/', views.LeadDetailView.as_view(), name='leadDetail'),
path('<int:pk>/update/', views.LeadUpdateView.as_view(), name='leadUpdate'),
path('<int:pk>/delete/', views.LeadDeleteView.as_view(), name='leadDelete'),

]