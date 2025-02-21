from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from api.views import (
    RequestListView, RequestCreateView, RequestUpdateView, RequestDeleteView,
    PictureListView, PictureCreateView, PictureDeleteView,
    LoginView
)
from django.urls import re_path
from api.consumers import AdminNotificationConsumer  # Import your WebSocket consumer

urlpatterns = [
    path('admin/', admin.site.urls),

    # Request URLs
    path('api/requests/', RequestListView.as_view(), name='request-list'),
    path('api/requests/create/', RequestCreateView.as_view(), name='request-create'),
    path('api/requests/<int:pk>/update/', RequestUpdateView.as_view(), name='request-update'),
    path('api/requests/<int:pk>/delete/', RequestDeleteView.as_view(), name='request-delete'),

    # Picture URLs
    path('api/pictures/', PictureListView.as_view(), name='picture-list'),
    path('api/pictures/create/', PictureCreateView.as_view(), name='picture-create'),
    path('api/pictures/<int:pk>/delete/', PictureDeleteView.as_view(), name='picture-delete'),

    # Login URL
    path('api/login/', LoginView.as_view(), name='login'),

    # Authentication Token URL
    path('api/token/', obtain_auth_token, name='api_token_auth'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# WebSocket URL patterns (used by Django Channels)
websocket_urlpatterns = [
    re_path(r'ws/notifications/$', AdminNotificationConsumer.as_asgi()),  # WebSocket route
]
