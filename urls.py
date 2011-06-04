from django.conf.urls.defaults import *
from webEval import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^webEval/', include('webEval.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
    (r'^api/', include('webEval.api.urls')),
    
    (r'^$', 'webEval.web_eval__core.wiki__controller.dashboard'),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    (r'^favicon.ico$', 'django.views.generic.simple.redirect_to', {'url': '%s/images/favicon.ico' % settings.MEDIA_URL}),
    
    (r'^blog/new-entry/$', 'webEval.web_eval__core.blog__controller.new_entry'),
    (r'^blog/comments/posted/$', 'webEval.web_eval__core.blog__controller.comment_posted'),
    (r'^blog/comments/', include('django.contrib.comments.urls')),
    (r"^blog/delete_comment/(\d+)/$", "webEval.web_eval__core.blog__controller.delete_comment"),
    (r"^blog/delete_comment/(\d+)/(\d+)/$", "webEval.web_eval__core.blog__controller.delete_comment"),
    
    (r'^blog/(?P<username>[\w_.-@]+)/(?P<permalink>[\w-]+)/edit/$', 'webEval.web_eval__core.blog__controller.edit_entry'),
    (r'^blog/(?P<username>[\w_.-@]+)/(?P<permalink>[\w-]+)/delete/$', 'webEval.web_eval__core.blog__controller.delete_entry'),
    (r'^blog/(?P<username>[\w_.-@]+)/(?P<permalink>[\w-]+)/toogle-dashboard/$', 'webEval.web_eval__core.blog__controller.toogle_dashboard'),
    (r'^blog/(?P<username>[\w_.-@]+)/(?P<permalink>[\w-]+)/$', 'webEval.web_eval__core.blog__controller.display_entry'),
    (r'^blog/(?P<username>[\w_.-@]+)/$', 'webEval.web_eval__core.blog__controller.index'),
    (r'^blog/$', 'webEval.web_eval__core.blog__controller.index'),
    
    (r'^contests/$', 'webEval.web_eval__core.grader__controller.display_all_contests'),
    (r'^contest/(?P<contest_code>\w+)/$', 'webEval.web_eval__core.grader__controller.display_contest'),
    (r'^contest/(?P<contest_code>\w+)/toogle-registration/$', 'webEval.web_eval__core.grader__controller.toogle_contest_registration'),
    (r'^contest/(?P<contest_code>\w+)/edit/$', 'webEval.web_eval__core.grader__controller.edit_contest_statement'),
    (r'^contest/(?P<contest_code>\w+)/configure/$', 'webEval.web_eval__core.grader__controller.configure_contest'),
    (r'^contest/(?P<contest_code>\w+)/users-registered/$', 'webEval.web_eval__core.grader__controller.display_contest_registered_users'),
    (r'^contest/(?P<contest_code>\w+)/standings/$', 'webEval.web_eval__core.grader__controller.display_contest_standings'),
    
    (r'^forum/board/(?P<board_id>\d+)/$', 'webEval.web_eval__core.forum__controller.display_board'),
    (r'^forum/topic/(?P<topic_id>\d+)/$', 'webEval.web_eval__core.forum__controller.display_topic'),
    (r'^forum/topic/(?P<topic_id>\d+)/reply/$', 'webEval.web_eval__core.forum__controller.reply'),
    (r'^forum/board/(?P<board_id>\d+)/new-topic/$', 'webEval.web_eval__core.forum__controller.new_topic'),
    (r'^forum/post/(?P<post_id>\d+)/edit/$', 'webEval.web_eval__core.forum__controller.edit_post'),
    (r'^forum/post/(?P<post_id>\d+)/move/$', 'webEval.web_eval__core.forum__controller.move_post'),
    (r'^forum/post/(?P<post_id>\d+)/delete/$', 'webEval.web_eval__core.forum__controller.delete_post'),
    (r'^forum/private-messages/new/', 'webEval.web_eval__core.user__controller.new_private_message'),
    (r'^forum/private-messages/$', 'webEval.web_eval__core.user__controller.private_messages'),
    
    (r'^admin/$', 'webEval.web_eval__core.grader__controller.admin_page'),
    (r'^admin/create-problem/', 'webEval.web_eval__core.grader__controller.create_problem'),
    (r'^admin/create-contest/', 'webEval.web_eval__core.grader__controller.create_contest'),
    
    (r'^problem/(?P<problem_code>\w+)/$', 'webEval.web_eval__core.grader__controller.display_problem'),
    (r'^problem/(?P<problem_code>\w+)/edit/$', 'webEval.web_eval__core.grader__controller.edit_problem_statement'),
    (r'^problem/(?P<problem_code>\w+)/configure/$', 'webEval.web_eval__core.grader__controller.configure_problem'),
    (r'^problem/(?P<problem_code>\w+)/edit-tags/$', 'webEval.web_eval__core.grader__controller.edit_problem_tags'),
    (r'^problems-by-author/(?P<author_code>\w+)/$', 'webEval.web_eval__core.grader__controller.display_problems_by_author'),
    
    (r'^status/$', 'webEval.web_eval__core.grader__controller.status'),
    (r'^status/job/(?P<job_id>\d+)/details/$', 'webEval.web_eval__core.grader__controller.display_job'),
    (r'^status/job/(?P<job_id>\d+)/source-code/$', 'webEval.web_eval__core.grader__controller.display_job_source_code'),
    
    (r'^submit/$', 'webEval.web_eval__core.grader__controller.submit'),
    
    (r'^tickets/$', 'webEval.web_eval__core.utils__controller.tickets'),
    (r'^tickets/new/$', 'webEval.web_eval__core.utils__controller.new_ticket'),
    (r"^tickets/(?P<ticket_id>\d+)/delete_comment/$", "webEval.web_eval__core.utils__controller.delete_comment"),
    (r"^tickets/(?P<ticket_id>\d+)/delete_comment/(?P<comment_id>\d+)/$", "webEval.web_eval__core.utils__controller.delete_comment"),
    (r'^ticket/(?P<ticket_id>\d+)/$', 'webEval.web_eval__core.utils__controller.display_ticket'),
    (r'^ticket/(?P<ticket_id>\d+)/edit/$', 'webEval.web_eval__core.utils__controller.edit_ticket'),
    
    (r'^captcha/', include('captcha.urls')),
    (r'^auth/successful-login/$', 'webEval.web_eval__core.auth__controller.successful_login'),
    (r'^auth/login/$', 'webEval.web_eval__core.auth__controller.login'),
    (r'^auth/facebook-login/$', 'webEval.web_eval__core.auth__controller.facebook_login'),
    
   # (r'^openid/', include('django_openid_auth.urls')),
    url(r'^auth/openid-login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
    url(r'^auth/openid-login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^auth/openid-logout/$', 'django.contrib.auth.views.logout', {'next_page': '/',}, name='logout'),
    (r'^auth/logout/$', 'webEval.web_eval__core.auth__controller.logout'),
    
    (r'^auth/twitter-login/$', 'webEval.web_eval__core.auth__controller.twitter_login'),
    (r'^auth/twitter-login/return/$', 'webEval.web_eval__core.auth__controller.twitter_return'),
    
    (r'^auth/register/$', 'webEval.web_eval__core.auth__controller.register'),
    (r'^auth/succesful-register/', 'webEval.web_eval__core.auth__controller.successful_register'),
    
    (r'^user/(?P<user_name>[\w_.]+)/$', 'webEval.web_eval__core.user__controller.display_user'),
    (r'^user/(?P<user_name>[\w_.]+)/edit/$', 'webEval.web_eval__core.user__controller.edit_user_description'),
    (r'^user/(?P<user_name>[\w_.]+)/edit-account/$', 'webEval.web_eval__core.user__controller.edit_user_account'),
    (r'^user/(?P<user_name>[\w_.]+)/get-avatar/$', 'webEval.web_eval__core.user__controller.get_avatar'),
    (r'^user/(?P<user_name>[\w_.]+)/rating/$', 'webEval.web_eval__core.user__controller.display_user_rating'),
    (r'^user/(?P<user_name>[\w_.]+)/statistics/$', 'webEval.web_eval__core.user__controller.display_user_statistics'),
    (r'^user/(?P<user_name>[\w_.]+)/validate-key/(?P<validation_key>\w+)/$', 'webEval.web_eval__core.auth__controller.validate_user'),
    
    (r'^api/get_rounds_for_problem', 'webEval.web_eval__core.grader__controller.get_rounds_for_problem'),
    (r'^api/search_tags/$', 'webEval.web_eval__core.blog__controller.get_tags_ajax'),
    (r'^api/register_form/$', 'webEval.web_eval__core.auth__controller.register_remote_form'),
    (r'^api/login_form/$', 'webEval.web_eval__core.auth__controller.login_remote_form'),
    
    (r'^ranks/$', 'webEval.web_eval__core.grader__controller.ranks'),
    
    (r'^wiki/$', 'webEval.web_eval__core.wiki__controller.wiki_index'),
    (r'^wiki/create-wiki-page/$', 'webEval.web_eval__core.wiki__controller.create_wiki_page'),
    (r'^(?P<page_url>[\w_.,-@/]+)/attach/$', 'webEval.web_eval__core.wiki__controller.attach'),
    (r'^(?P<page_url>[\w_.,-@/]+)/attachments/$', 'webEval.web_eval__core.wiki__controller.attachments'),
    (r'^(?P<page_url>[\w_.,-@/]+)/attachment/(?P<hash>\w+)/rename/$', 'webEval.web_eval__core.wiki__controller.rename_attachment'),
    (r'^(?P<page_url>[\w_.,-@/]+)/attachment/(?P<hash>\w+)/delete/$', 'webEval.web_eval__core.wiki__controller.delete_attachment'),
    (r'^(?P<page_url>[\w_.,-@/]+)/attachment/(?P<hash>\w+)/$', 'webEval.web_eval__core.wiki__controller.display_attachment'),
    (r'^(?P<page_url>[\w_.,-@/]+)/download-attachments/$', 'webEval.web_eval__core.wiki__controller.download_attachments'),
    (r'^(?P<page_url>[\w_.,-@/]+)/copy/$', 'webEval.web_eval__core.wiki__controller.copy_page'),
    (r'^(?P<page_url>[\w_.,-@/]+)/diff/$', 'webEval.web_eval__core.wiki__controller.diff'),
    (r'^(?P<page_url>[\w_.,-@/]+)/edit/$', 'webEval.web_eval__core.wiki__controller.edit_page'),
    (r'^(?P<page_url>[\w_.,-@/]+)/history/$', 'webEval.web_eval__core.wiki__controller.history'),
    (r'^(?P<page_url>[\w_.,-@/]+)/move/$', 'webEval.web_eval__core.wiki__controller.move_page'),
    (r'^(?P<page_url>[\w_.,-@/]+)/restore/(?P<revision_id>\d+)/$', 'webEval.web_eval__core.wiki__controller.restore'),
    (r'^(?P<page_url>[\w_.,-@/]+)/revision/(?P<revision_id>\d+)/$', 'webEval.web_eval__core.wiki__controller.display_page'),
    (r'^(?P<page_url>[\w_.,-@/]+)/$', 'webEval.web_eval__core.wiki__controller.display_page'),
)
