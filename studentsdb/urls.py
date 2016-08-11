"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, include,url
from django.contrib import admin
from .settings import MEDIA_ROOT, DEBUG

urlpatterns = patterns('',
# Students urls
url(r'^$', 'students.view.student.students_list', name='main'),
url(r'^vid$', 'students.view.journal.vid', name='journal'),
url(r'^stud_add$', 'students.view.student.stud_add', name='s_add'),
url(r'^students/(?P<pk>\d+)/edit/$','students.view.student.student_edit',
name='students_edit'),
url(r'^students/(?P<pk>\d+)/delete/$','students.view.student.student_delete',name='students_delete'),
#Groups urls
url(r'^grup$', 'students.view.groups.grup', name='groups'),
url(r'^groups_add$', 'students.view.group.groups_add', name='groups_add'),
url(r'^groups/(?P<pk>\d+)/edit/$',
'students.view.group.groups_edit', name='groups_edit'),
url(r'^groups/(?P<pk>\d+)/delete/$',
'students.view.group.groups_delete', name='groups_delete'),
url(r'^groups/(?P<pk>\d+)/one/$',
'students.view.group.groups_one', name='groups_one'),
url(r'^admin/', include(admin.site.urls)),
#exams url
url(r'^exams$', 'students.view.exams.exams_list', name='exams'),
url(r'^exam_add$', 'students.view.exams.exam_add', name='exam_add'),
# Contact Admin Form
url(r'^contact-admin/$', 'students.view.contact_admin.contact_admin',
name='contact_admin'),
)
if DEBUG:
 # serve files from media folder
 urlpatterns += patterns('',
 url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
 'document_root': MEDIA_ROOT}))
