
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # Include the seedview app's URLs
    path('userprofile/', include('userprofile.urls')),
    path('investment/', include('investment.urls')),  # Ensure 'investment.urls' is correct
    path('connectwallet/', include('connectwallet.urls')),
]

# Add this at the end to serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

