from rest_framework.response import Response
from rest_framework.generics import (CreateAPIView, RetrieveUpdateDestroyAPIView,
                                     ListAPIView)
from rest_framework_simplejwt.views import TokenObtainPairView
#from rest_framework.permissions import IsAuthenticated
#from rest_framework_simplejwt.authentication import JWTAuthentication
#to work properly need to provide headers in request(frontend)
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework_tracking.mixins import LoggingMixin
from django.contrib.auth.models import User
from .serializers import (RegisterModelSerializer, LoginModelSerializer, 
                          PostModelSerializer, LikeModelSerializer, 
                          DislikeModelSerializer, AnalyticsPostModelSerializer)
from .models import PostModel, LikeModel, DislikeModel
from datetime import datetime

class RegisterUserView(LoggingMixin, CreateAPIView):
    logging_methods = ['POST']
    queryset = User.objects.all()
    serializer_class = RegisterModelSerializer


class LoginUserView(LoggingMixin, TokenObtainPairView):
    logging_methods = ['POST']
    serializer_class = LoginModelSerializer
    

class CreatePostModelView(LoggingMixin, CreateAPIView):
    logging_methods = ['POST']
    queryset = PostModel.objects.all()
    serializer_class = PostModelSerializer

    def perform_create(self, serializer):
        post = serializer.save()
        like_model = LikeModel.objects.create(related_post=post)
        dislike_model = DislikeModel.objects.create(related_post=post)
        post.liked_model = like_model
        post.disliked_model = dislike_model
        post.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class LikeModelView(LoggingMixin, RetrieveUpdateDestroyAPIView):
    logging_methods = ['PUT']
    lookup_url_kwarg = "id"
    serializer_class = LikeModelSerializer
    
    def get_object(self):
        id = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(LikeModel.objects.select_related(
            "related_post"
            ), related_post__id=id)
    
    def update(self, request, *args, **kwargs):
        id = self.kwargs.get(self.lookup_url_kwarg)
        current_model = self.get_object()
        current_user = self.request.query_params.get("current_user")
        #or current_user = request.user
        opposite_model = DislikeModel.objects.select_related("related_post").get(id=id)
        if_in_opposite_model = opposite_model.users_amount.filter(username=
                                                    request.user.username)
        if not if_in_opposite_model:
            current_model.users_amount.add(current_user)
            current_model.save()
            return Response({"action": "liked"}, status=status.HTTP_200_OK)
        return Response({"action:" "disallowed"}, status=status.HTTP_403_FORBIDDEN)
        

class DislikeModelView(LoggingMixin, RetrieveUpdateDestroyAPIView):
    logging_methods = ['PUT']
    lookup_url_kwarg = "id"
    serializer_class = DislikeModelSerializer
    
    def get_object(self):
        id = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(DislikeModel.objects.select_related("related_post")
                                 ,related_post__id=id)
    def update(self, request, *args, **kwargs):
        id = self.kwargs.get(self.lookup_url_kwarg)
        current_model = self.get_object()
        current_user = self.request.query_params.get("current_user")
        opposite_model = LikeModel.objects.select_related("related_post").get(id=id)
        if_in_opposite_model = opposite_model.users_amount.filter(username=
                                                    request.user.username)
        if not if_in_opposite_model:
            current_model.users_amount.add(current_user)
            current_model.save()
            return Response({"action": "disliked"}, status=status.HTTP_200_OK)
        return Response({"action:" "disallowed"}, status=status.HTTP_403_FORBIDDEN)
    
class ActionPostModelView(LoggingMixin, RetrieveUpdateDestroyAPIView):
    logging_methods = ['GET', 'PUT']
    serializer_class = PostModelSerializer
    lookup_url_kwarg = "id"
    
    def get_object(self):
        id=self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(PostModel, id=id)
        
class AnalyticsPostModelView(LoggingMixin, ListAPIView):
    logging_methods = ['GET']
    serializer_class = AnalyticsPostModelSerializer
    
    def get_queryset(self):
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        if date_from and date_to:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d')
                date_to = datetime.strptime(date_to, '%Y-%m-%d')
            except ValueError:
                return Response({"error: Invalid data format"}, 
                                status=status.HTTP_400_BAD_REQUEST)
            queryset = PostModel.objects.filter(created_time__range=(date_from, date_to))
            return queryset
        return PostModel.objects.all()




    
    
