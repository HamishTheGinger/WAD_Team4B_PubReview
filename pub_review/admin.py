from django.contrib import admin
from pub_review.models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Pub)
admin.site.register(FavoritePubs)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Review)


