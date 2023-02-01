from django.contrib import admin
from django.contrib import admin
from user.models import Citizen, Company, RaceChoiceField, Security, SexChoiceField
from user.models import User, FriendRequest

class UserAdmin(admin.ModelAdmin):
    model = User

class CitizenAdmin(admin.ModelAdmin):
    model = Citizen
    filter_horizontal = ['friends']

admin.site.register(User, UserAdmin)
admin.site.register(RaceChoiceField)
admin.site.register(SexChoiceField)
admin.site.register(Company)
admin.site.register(Citizen, CitizenAdmin)
admin.site.register(Security)
admin.site.register(FriendRequest)