from django.contrib import admin
from .models import (
    Result, Account, SocialPost, LikedPost, DislikedPost,
)

# Register your models here.

admin.site.register(Result)
admin.site.register(Account)
admin.site.register(SocialPost)
admin.site.register(LikedPost)
admin.site.register(DislikedPost)