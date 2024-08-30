from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
	SpectacularAPIView,
	SpectacularRedocView,
	SpectacularSwaggerView,
)


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
    path('payment/', include('app_payment.urls')),
	path('api/', include('api_product.urls')),
	path('api-auth/', include('rest_framework.urls')),
	path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
	path('api/dj-rest-auth/registration/',
		 include('dj_rest_auth.registration.urls')),

	path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
	path("api/schema/redoc/", SpectacularRedocView.as_view(
		url_name="schema"), name="redoc",),
	path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(
		url_name="schema"), name="swagger-ui"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
