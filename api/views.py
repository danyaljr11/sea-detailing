import os
from django.contrib.auth import authenticate, login
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .models import Request, Picture
from .serializers import Request_Serializer, Picture_Serializer


# Custom response format
def custom_response(state, message, data=None):
    return {'state': state, 'message': message, 'data': data}


# WebSocket Notification Helper
def send_admin_notification(event_type, data):
    """ Sends a WebSocket notification to the admin panel """
    channel_layer = get_channel_layer()
    try:
        async_to_sync(channel_layer.group_send)(
            "admin_notifications",
            {
                "type": event_type,
                "message": json.dumps(data),
            }
        )
    except Exception as e:
        print(f"WebSocket Error: {str(e)}")


class RequestListView(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = Request_Serializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(custom_response(True, "Request list retrieved successfully", serializer.data))


class RequestCreateView(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = Request_Serializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            response_data = serializer.data

            # Send WebSocket notification
            send_admin_notification("new_request", response_data)

            return Response(custom_response(True, "Request created successfully", response_data), status=status.HTTP_201_CREATED)
        return Response(custom_response(False, "Request creation failed", serializer.errors), status=status.HTTP_400_BAD_REQUEST)


class RequestUpdateView(generics.UpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = Request_Serializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(custom_response(True, "Request updated successfully", serializer.data), status=status.HTTP_200_OK)
        return Response(custom_response(False, "Request update failed", serializer.errors), status=status.HTTP_400_BAD_REQUEST)


class RequestDeleteView(generics.DestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = Request_Serializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(custom_response(True, "Request deleted successfully"), status=status.HTTP_204_NO_CONTENT)


# Login View with custom response
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(custom_response(False, "Username and password are required"), status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            if user.is_superuser:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response(custom_response(True, "Login successful", {"token": token.key}), status=status.HTTP_200_OK)
            return Response(custom_response(False, "Not authorized"), status=status.HTTP_403_FORBIDDEN)

        return Response(custom_response(False, "Invalid credentials"), status=status.HTTP_401_UNAUTHORIZED)


class PictureListView(generics.ListAPIView):
    queryset = Picture.objects.all()
    serializer_class = Picture_Serializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(custom_response(True, "Picture list retrieved successfully", serializer.data))


class PictureCreateView(generics.CreateAPIView):
    queryset = Picture.objects.all()
    serializer_class = Picture_Serializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            image_url = request.build_absolute_uri(instance.image.url)
            response_data = {"id": instance.id, "picture_title": instance.picture_title, "image_url": image_url}
            return Response(custom_response(True, "Picture uploaded successfully", response_data), status=status.HTTP_201_CREATED)
        return Response(custom_response(False, "Picture upload failed", serializer.errors), status=status.HTTP_400_BAD_REQUEST)


class PictureDeleteView(generics.DestroyAPIView):
    queryset = Picture.objects.all()
    serializer_class = Picture_Serializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()  # Get the Picture object
        except Picture.DoesNotExist:
            return Response(custom_response(False, "Picture not found"), status=status.HTTP_404_NOT_FOUND)

        # Attempt to delete the file from the server
        if instance.image:
            image_path = instance.image.path
            if os.path.exists(image_path):
                os.remove(image_path)
            else:
                return Response(custom_response(False, "Picture record deleted, but file not found on server"), status=status.HTTP_200_OK)

        # Delete the database record
        instance.delete()
        return Response(custom_response(True, "Picture deleted successfully"), status=status.HTTP_200_OK)  # Changed from 204 to 200