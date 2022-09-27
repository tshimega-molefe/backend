from django.contrib import admin
from django.contrib import admin
from user.models import Citizen, Company, RaceChoiceField, Security, SexChoiceField
from user.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    model = User

admin.site.register(User, UserAdmin)
admin.site.register(RaceChoiceField)
admin.site.register(SexChoiceField)
admin.site.register(Company)
admin.site.register(Citizen)
admin.site.register(Security)