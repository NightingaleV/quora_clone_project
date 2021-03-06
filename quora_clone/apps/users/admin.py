from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from .forms import UserCreationForm

# UserChangeForm

User = get_user_model()


# TODO add TopicsSubscription inline from topics.admin
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    # form = UserChangeForm
    add_form = UserCreationForm
    list_display = ["username", "is_superuser", 'gender', 'profile_image']
    search_fields = ["username"]
