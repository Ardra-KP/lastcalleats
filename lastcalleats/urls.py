from django.contrib import admin
from django.urls import path, include
from hotels import views

# ✅ ADD THESE TWO LINES
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Hotels app
    path('hotels/', include('hotels.urls')),
]

# ✅ VERY IMPORTANT FOR IMAGE LOADING
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    