from django.contrib import admin
from .models import registerRequests, Assessment, Question, timeRemaining, Response

admin.site.register(registerRequests)
admin.site.register(Assessment)
admin.site.register(Question)
admin.site.register(timeRemaining)
admin.site.register(Response)
