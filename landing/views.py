from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView
from .forms import ApplicationObjectForm, SortForm
from .models import ApplicationObject
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import View
from django.http import HttpResponse
import datetime
import xlwt


@login_required(login_url='login')
def index(request):
    error = ''
    if request.method == "POST":
        form = ApplicationObjectForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('about')
        else:
            error = 'Не верно заполнена форма'
    form = ApplicationObjectForm()
    data = {
        'title': 'Создание новой заявки',
        'form': form,
        'error': error
    }
    return render(request, 'landing/index.html', data)


class ApplicationDetailView(DetailView):
    model = ApplicationObject
    template_name = 'landing/details_view.html'
    context_object_name = 'application'


class ApplicationUpdateView(UpdateView):
    model = ApplicationObject
    template_name = 'landing/index.html'
    form_class = ApplicationObjectForm


class ApplicationDeleteView(DeleteView):
    model = ApplicationObject
    template_name = 'landing/application-delete.html'
    success_url = '/about'


@login_required(login_url='login')
def about(request):
    query = request.GET.get('search', None)
    if query:
        application_objects = ApplicationObject.objects.filter(
            Q(name_object__icontains=query) | Q(address_object__icontains=query) | Q(id__icontains=query) | Q(
                number_object__icontains=query))
    else:
        application_objects = ApplicationObject.objects.all()
    application_paginator = Paginator(application_objects, 7)
    page_num = request.GET.get('page')
    page = application_paginator.get_page(page_num)
    data = {
        'count': application_paginator.count,
        'page': page,
    }
    return render(request, 'landing/about.html', data)


@login_required(login_url='login')
def application(request):
    application_objects_filter = ApplicationObject.objects.all()
    form = SortForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            sort_service_area = form.cleaned_data['sort_form']
            sort_completion_date = form.cleaned_data['completion_date']
            application_objects_filter = ApplicationObject.objects.filter(completion_date=sort_completion_date,
                                                                          service_area=sort_service_area)
    data = {
        'form': form,
        'application_objects_filter': application_objects_filter
    }
    return render(request, 'landing/application.html', data)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Имя или пароль не корректные')

    data = {
    }
    return render(request, 'landing/login.html', data)


def logoutUser(request):
    logout(request)
    return redirect('login')


class Report(View):
    model = ApplicationObject

    def get(self, request):
        form = SortForm(request.POST)
        application_objects = []
        query = request.GET.get('completion_date', None)
        query_2 = request.GET.get('completion_date_2', None)
        if (query and query_2):
            application_objects = ApplicationObject.custom_manager.get_date_range(query, query_2)
        else:
            pass
        data = {
            'form': form,
            'application_objects': application_objects,
        }
        return render(request, 'landing/report.html', data)


def export_excel(request):
    objects_filter = ApplicationObject.objects.filter(id__in='1').values_list('id', 'number_object',
                                                                              'urgency_application',
                                                                              'completion_date',
                                                                              'name_object', 'address_object',
                                                                              'comment', 'type_of_problem',
                                                                              'initiator_of_the_application')
    selected_list = request.GET.get('search', None).split(',')
    print(selected_list)
    if selected_list and selected_list != ['']:
        objects_filter = ApplicationObject.objects.filter(id__in=selected_list).values_list('id', 'number_object',
                                                                                            'urgency_application',
                                                                                            'completion_date',
                                                                                            'name_object',
                                                                                            'address_object',
                                                                                            'comment',
                                                                                            'type_of_problem',
                                                                                            'initiator_of_the_application')
    print(objects_filter)
    print(objects_filter.count())
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Report' + str(datetime.datetime.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Report')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['ID', 'Номер объекта', 'Срочность', 'Время', 'Имя объекта', 'Адрес', 'Комментарий', 'Неисправность',
               'ФИО источника']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    for row in objects_filter:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
            print(str(row[col_num]))
    wb.save(response)
    print(response)
    return response
