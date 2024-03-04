from django.contrib import admin

from apps.models import *

admin.site.register(QuestionModel)
admin.site.register(QuestionCategory)
admin.site.register(GameMode)
admin.site.register(UserCategoryWeight)