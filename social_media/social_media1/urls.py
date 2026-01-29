from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts.views import feed_redirect

urlpatterns = [
     path("admin/", admin.site.urls),

    path("", feed_redirect, name="home"),
    path("feed/", include("posts.urls")),
    # ACCOUNTS
    path("accounts/", include("accounts.urls")),
    path("posts/", include("posts.urls")),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)