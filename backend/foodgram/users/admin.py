from django.contrib import admin
from django.contrib.auth import get_user_model, models

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email',)


admin.site.unregister(models.Group)
