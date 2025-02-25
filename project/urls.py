from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from api.views import (
    RequestListView, RequestCreateView, RequestUpdateView, RequestDeleteView,
    PictureListView, PictureCreateView, PictureDeleteView,
    LoginView ,index
)


urlpatterns = [

    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    path('api/adminpanel00/', admin.site.urls),

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

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
