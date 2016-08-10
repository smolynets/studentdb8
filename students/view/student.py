# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from ..models.student import Student
from ..models.group import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.contrib import messages
from PIL import Image
def students_list(request):
   students = Student.objects.all()
   # try to order students list
   order_by = request.GET.get('order_by', '')
   if order_by in ('last_name', 'first_name', 'ticket', '#'):
     students = students.order_by(order_by)
     if request.GET.get('reverse', '') == '1':
       students = students.reverse()
   # paginate students
   paginator = Paginator(students, 3)
   page = request.GET.get('page')
   try:
     students = paginator.page(page)
   except PageNotAnInteger:
   # If page is not an integer, deliver first page.
     students = paginator.page(1)
   except EmptyPage:
     # If page is out of range (e.g. 9999), deliver
     # last page of results.
     students = paginator.page(paginator.num_pages)
   return render(request, 'students/stud.html',
     {'students': students})

def stud_add(request):
  # was form posted?
  if request.method == "POST":
    # was form add button clicked?
    if request.POST.get('add_button') is not None:
      # errors collection
      errors = {}
      # data for student object
      data = {'middle_name': request.POST.get('middle_name'),'notes': request.POST.get('notes')}
      # validate user input
      first_name = request.POST.get('first_name', '').strip()
      if not first_name:
        errors['first_name'] = u"Ім'я є обов'язковим"
      else:
        data['first_name'] = first_name
      last_name = request.POST.get('last_name', '').strip()
      if not last_name:
        errors['last_name'] = u"Прізвище є обов'язковим"
      else:
        data['last_name'] = last_name
      birthday = request.POST.get('birthday', '').strip()
      if not birthday:
        errors['birthday'] = u"Дата народження є обов'язковою"
      else:
        try:
          datetime.strptime(birthday, '%Y-%m-%d')
        except Exception:
          errors['birthday'] = u"Введіть коректний формат дати (напр. 1986-03-23)"
        else:
          data['birthday'] = birthday
      ticket = request.POST.get('ticket', '').strip()
      if not ticket:
        errors['ticket'] = u"Номер білета є обов'язковим"
      else:
        data['ticket'] = ticket
      student_group_id = request.POST.get('student_group_id', '').strip()
      if not student_group_id:
        errors['student_group_id'] = u"Оберіть групу для студента"
      else:
        groups = Group.objects.filter(pk=student_group_id)
        if len(groups) != 1:
          errors['student_group'] = u"Оберіть коректну групу"
        else:
          data['student_group_id'] = groups[0]
      photo = request.FILES.get('photo')
      if photo:
        if photo.name.split(".")[-1].lower() not in ('jpg', 'jpeg', 'png', 'gif'):
           errors['photo'] = u"Файл має бути одного з наступних типів: jpg, jpeg, png, gif"
        else:
           try:
             Image.open(photo)
           except Exception:
             errors['photo'] = u"Завантажений файл не є файлом зображення або пошкоджений"
           else:
             if photo.size > 2 * 1024 * 1024:
                errors['photo'] = u"Фото занадто велике (розмір файлу має бути менше 2Мб)"
             else:
                data['photo'] = photo
           
      # save student
      if not errors:
        student = Student(**data)
        student.save()
        # redirect to students list
        return HttpResponseRedirect( u'%s?status_message=Студента успішно додано!'  % reverse('main'))
      else:
        # render form with errors and previous user input
        return render(request, 'students/students_add.html',
        {'groups': Group.objects.all().order_by('title'),'errors': errors})
    elif request.POST.get('cancel_button') is not None:
      # redirect to home page on cancel button
      return HttpResponseRedirect( u'%s?status_message=Додавання студента скасовано!' % reverse('main'))
  else:
   # initial form render
   return render(request, 'students/students_add.html',
   {'groups': Group.objects.all().order_by('title')})



def student_edit(request, pk):
    students = Student.objects.filter(pk=pk)
    groups = Group.objects.all()

    
    if request.method == "POST":
        data = Student.objects.get(pk=pk)
        if request.POST.get('add_button') is not None:
            data.middle_name = request.POST.get('middle_name', '').strip()
            data.notes = request.POST.get('notes', '').strip()
            errors = {}

            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Імʼя є обовʼязковим."
            else:
                data.first_name = first_name

            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = u"Прізвище є обовʼязковим."
            else:
                data.last_name = last_name

            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обовʼязковою."
            else:
                try:
                    bd = datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коректний формат дати (напр. 1987-12-30)"
                else:
                    data.birthday = bd
           
            photo = request.FILES.get('photo')
            if photo:
             if len(photo) > (10 * 1024):
               errors['photo'] = u"Файл завеликий"
             else:
               data.photo = photo

            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обовʼязковим."
            else:
                data.ticket = ticket

            student_group_id = request.POST.get('student_group_id', '').strip()
            if not student_group_id:
                errors['student_group_id'] = u"Група є обовʼязковою"
            else:
                gr = Group.objects.filter(pk=student_group_id)
                if len(gr) != 1:
                    errors['student_group_id'] = u"Оберіть коректну групу"
                else:
                    grps = Group.objects.filter(leader=Student.objects.get(pk=pk))
                    if len(grps) > 0 and int(student_group_id) != grps[0].pk:
                        errors['student_group'] = u"Студент є старостою іншої групи"
                    else:
                        data.student_group_id = gr[0]

            if errors:
                return render(request, 'students/students_edit.html', {'pk': pk, 'student': data, 'errors': errors, 'groups': groups})
            else:
                data.save()
                return HttpResponseRedirect( reverse('main'))
        elif request.POST.get('cancel_button') is not None:

            return HttpResponseRedirect(u'%s?status_message=Редагування студента скасовано!' % reverse('main'))
        
    else:
        return render(request,
                      'students/students_edit.html',
                      {'pk': pk, 'student': students[0], 'groups': groups})






def student_delete(request, pk):
    students = Student.objects.filter(pk=pk)
    
    if request.method == "POST":
        if request.POST.get('yes') is not None:
          students.delete()
          return HttpResponseRedirect( u'%s?status_message=Студента успішно видалено!'  % reverse('main'))
        elif request.POST.get('cancel_button') is not None:
          return HttpResponseRedirect( u'%s?status_message=Видалення  студента  скасовано!'  % reverse('main'))
        
    else:
        return render(request,
                      'students/students_delete.html',
                      {'pk': pk, 'student': students[0]})



