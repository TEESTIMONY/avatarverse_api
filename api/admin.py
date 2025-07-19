from django.contrib import admin
from .models import Avatar
from django.utils.html import format_html
from .models import Reaction

class AvatarAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'seed_text', 'created_at', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

admin.site.register(Avatar, AvatarAdmin)

class ReactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'avatar', 'user', 'reaction', 'created_at')

admin.site.register(Reaction, ReactionAdmin)