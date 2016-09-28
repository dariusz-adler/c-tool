from django.contrib import admin
from errors.models import Error, UserComment, ChangeHistory
# Register your models here.
admin.site.register(Error)
admin.site.register(UserComment)
admin.site.register(ChangeHistory)