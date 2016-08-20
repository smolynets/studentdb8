# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
class Exam(models.Model):
  """Exam Model"""
  class Meta(object):
    verbose_name = u"Іспит"
    verbose_name_plural = u"Іспити"
  title = models.CharField(
    max_length=256,
    blank=False,
    verbose_name=u"Назва")
  group = models.OneToOneField('Group',
    verbose_name=u"Староста",
    blank=True,
    null=True,
    on_delete=models.SET_NULL)
  date = models.DateField(
    blank=True,
    verbose_name=u"Дати")
  def __unicode__(self):
    return u"%s %s" % (self.title)
