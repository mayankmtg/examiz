from django.contrib import admin
from .models import registerRequests, Assessment, Question

admin.site.register(registerRequests)
admin.site.register(Assessment)
admin.site.register(Question)
