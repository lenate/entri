from itertools import product
from django.contrib import admin
from .models import *

admin.site.register(InterviewTimeslot)
admin.site.register(UserProfile)
admin.site.register(InterviewSchedule)
