from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .validators import validate_img_format

class UserBehaviourModel(models.Model):
    related_post = models.OneToOneField("PostModel", on_delete=models.CASCADE)
    users_amount = models.ManyToManyField(User, blank=True)
    
    def get_users_reaction(self):
        return self.users_amount.count()
    
    class Meta:
        abstract = True
        
class LikeModel(UserBehaviourModel):
    class Meta:
        db_table = "logic_likemodel"
        
class DislikeModel(UserBehaviourModel):
    class Meta:
        db_table = "logic_dislikemodel"
        
class PostModel(models.Model):
    text_field = models.CharField(max_length=2200)
    author_user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_field = models.ImageField(upload_to="images/", validators=[validate_img_format])
    liked_model = models.OneToOneField(LikeModel, on_delete=models.SET_NULL, 
                related_name="liked_model", null=True, blank=True)
    disliked_model = models.OneToOneField(DislikeModel, on_delete=models.SET_NULL,
                    related_name="disliked_model", null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    
CREATE, READ, UPDATE, DELETE = "Create", "Read", "Update", "Delete"
LOGIN, LOGOUT, LOGIN_FAILED = "Login", "Logout", "Login Failed"
ACTION_TYPES = [
    (CREATE, CREATE),
    (READ, READ),
    (UPDATE, UPDATE),
    (DELETE, DELETE),
    (LOGIN, LOGIN),
    (LOGOUT, LOGOUT),
    (LOGIN_FAILED, LOGIN_FAILED),
]

SUCCESS, FAILED = "Success", "Failed"
ACTION_STATUS = [(SUCCESS, SUCCESS), (FAILED, FAILED)]

class ActionLogModel(models.Model):
    actor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    action_type = models.CharField(choices=ACTION_TYPES, max_length=15)
    action_time = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(choices=ACTION_STATUS, max_length=7, default=SUCCESS)
    data = models.JSONField(default=dict)
    content_type = models.ForeignKey(
        ContentType, models.SET_NULL, blank=True, null=True
        )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()
    
    def __str__(self):
        return f"{self.action_type} by {self.actor} on {self.action_time}"

    

