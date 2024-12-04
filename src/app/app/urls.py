from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from core.api.views import SentFormView, FormsByUserView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',),
    # path('api/user/', include('user.urls')),
    path('', include('web.urls')),
    path('api/sent-form/<int:user_id>/<int:sent_form_id>/', SentFormView.as_view(), name='sent_form_detail'),
    path('api/user-forms/<int:user_id>/', FormsByUserView.as_view(), name='user_forms_detail'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
