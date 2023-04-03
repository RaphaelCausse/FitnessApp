from django.contrib import admin
from .models import (
    Result, Account, SocialPost, 
)

# Register your models here.
admin.site.register(Result)
admin.site.register(Account)
admin.site.register(SocialPost)
