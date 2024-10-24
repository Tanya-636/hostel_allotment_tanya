from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='hostel/', permanent=False)),  # Redirect root to hostel/
    path('hostel/', include('hostel.urls')),  # Include the hostel app URLs
]
