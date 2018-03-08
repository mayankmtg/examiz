from django.contrib import admin
from .models import registerRequests, Assessment, Question, timeRemaining

admin.site.register(registerRequests)
admin.site.register(Assessment)
admin.site.register(Question)
admin.site.register(timeRemaining)
