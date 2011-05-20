
from django.contrib import admin

from webEval.web_eval__core.models import *

admin.site.register(ForumBoard)
admin.site.register(ForumTopic)
admin.site.register(ForumPost)


admin.site.register(Author)
admin.site.register(Contest)
admin.site.register(Job)
admin.site.register(Problem)
admin.site.register(Test)


admin.site.register(WikiPage)
admin.site.register(WikiRevision)
