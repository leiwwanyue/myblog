from django.contrib import admin
# from django.contrib.auth import get_user_model
#
# User = get_user_model()

# 注册你的模型到 admin
# admin.site.register(User)

# insert post
from .models import Post

admin.site.register(Post)

# insert customuser
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)

# insert carousel
from .models import Carousel
# @admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('title', 'active')
    list_filter = ('active',)

admin.site.register(Carousel, CarouselAdmin)