from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import (PostModel, LikeModel, DislikeModel)

class RegisterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True}
        }
    def create(self, validated_data):
        try:
            user_fields = User.objects.create_user(username=validated_data["username"],
                        email=validated_data["email"],
                        password=validated_data["password"])
        
            return user_fields
        except IntegrityError as e:
            raise e

class LoginModelSerializer(TokenObtainPairSerializer):
   def validate(self, attrs):
        data = super().validate(attrs)
        data["username"] = self.user.username
        return data

class PostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        exclude = ('liked_model', 'disliked_model')

class LikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = "__all__"

class DislikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DislikeModel
        fields = "__all__"
        
class AnalyticsPostModelSerializer(serializers.ModelSerializer):
    liked_model = LikeModelSerializer()
    disliked_model = DislikeModelSerializer()
    class Meta:
        model = PostModel
        fields = "__all__"
    def get_liked_model(self, obj):
        return obj.liked_model
    
    def get_disliked_model(self, obj):
        return obj.disliked_model
        
        