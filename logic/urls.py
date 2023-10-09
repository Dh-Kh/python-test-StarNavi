from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import (RegisterUserView, LoginUserView, 
                    CreatePostModelView, ActionPostModelView,
                    AnalyticsPostModelView, LikeModelView, 
                    DislikeModelView)

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view()),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view()),
    path("register_model/", RegisterUserView.as_view()),
    path("login_model/", LoginUserView.as_view()),
    path("create_post/", CreatePostModelView.as_view()),
    path("modify_post/<int:id>/", ActionPostModelView.as_view()),
    path("analitics/", AnalyticsPostModelView.as_view()),
    path("like_action/<int:id>/", LikeModelView.as_view()),
    path("dislike_action/<int:id>/", DislikeModelView.as_view()),
]
