from django.contrib import admin
from .models import (LikeModel, DislikeModel, 
                     PostModel)

admin.site.register(LikeModel)
admin.site.register(DislikeModel)
admin.site.register(PostModel)
