from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^login/$', 'webEval.api.views.login'),
    (r'^get-job/$', 'webEval.api.views.return_job'),
    (r'^update-job/$', 'webEval.api.views.update_job'),
    (r'^create-eval/$', 'webEval.api.views.create_eval'),
    (r'^get-your-score/$', 'webEval.api.views.get_your_score'),
    (r'^check_if_username-exists/$', 'webEval.api.views.check_if_username_exists')
)
