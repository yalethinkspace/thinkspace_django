from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from client.models import *

# Register your models here.

# extend the User admin panel to show extra fields
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('hearts', 'hearted_users', 'is_moderator', 'is_mentor', 'about', 'photo', 'resume')}),
    )

class UserSiteRoleAdmin(admin.ModelAdmin):
    list_display = ["name"]

class CourseAdmin(admin.ModelAdmin):
    list_display = ["code", "name"]

class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name"]

class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]

class ProjectJoinRequestAdmin(admin.ModelAdmin):
    list_display = ["user", "project"]

class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ["comment", "user"]

class ProjectPostAdmin(admin.ModelAdmin):
    list_display = ["post"]

class ProjectTagAdmin(admin.ModelAdmin):
    list_display = ["name"]

class MessageAdmin(admin.ModelAdmin):
    list_display = ["sender"]

class MessageInlineAdmin(admin.TabularInline):
    model = Message

class ConversationAdmin(admin.ModelAdmin):
    list_display = []
    inlines = [MessageInlineAdmin]

class PostAdmin(admin.ModelAdmin):
    list_display = ["title"]

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(UserSiteRole, UserSiteRoleAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(ProjectJoinRequest, ProjectJoinRequestAdmin)
admin.site.register(ProjectComment, ProjectCommentAdmin)
admin.site.register(ProjectPost, ProjectPostAdmin)
admin.site.register(ProjectTag, ProjectTagAdmin)
admin.site.register(Message, MessageAdmin) 
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Post, PostAdmin)