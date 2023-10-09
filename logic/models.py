from django.db import models
from django.contrib.auth.models import User
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
    


    

