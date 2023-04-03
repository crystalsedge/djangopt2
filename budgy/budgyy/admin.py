from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Sing
#unregister groups
admin.site.unregister(Group)

#remixing profile and users info
class ProfileInline(admin.StackedInline):
    model = Profile


#extend user model  
class UserAdmin(admin.ModelAdmin):
    model = User
    #this is to display username fields on admin page
    fields = ["username"]
    inlines = [ProfileInline]

#unregistering initial user
admin.site.unregister(User)
#registering new user and profile
admin.site.register(User, UserAdmin)
 
 #---admin.site.register(Profile)[Kept!! incase]


#posting sings!
admin.site.register(Sing)


