from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_home.urls')),
    path('app-account/', include('app_account.urls')),
    path('setting/', include('app_site_setting.urls')),
    path('blog/', include('app_blog.urls')),
    path('product/', include('app_product.urls')),
    path('cart/', include('app_cart.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    path('dashboard/', include('app_dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
