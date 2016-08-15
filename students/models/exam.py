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
  group = models.CharField(
    max_length=256,
    verbose_name=u"Група",
    blank=True,
    null=True)
  date = models.DateField(
    blank=True,
    verbose_name=u"Дати")
  def __unicode__(self):
    return u"%s %s" % (self.title, self.group)
