from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView
from .forms import ApplicationObjectForm, SortForm, Search
from .models import ApplicationObject
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import psutil

@login_required(login_url='login')
def index(request):
    error = ''
    if request.method == "POST":
        form =ApplicationObjectForm(request.POST)
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
            application_objects_filter = ApplicationObject.objects.filter(completion_date=sort_completion_date, service_area=sort_service_area)
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

def test(request):
    proc_objects = []
    form = Search(request.POST)
    for p in psutil.process_iter(attrs=['pid', 'username', 'cpu_percent', 'memory_percent', 'memory_info', 'name']):
        process_info = [p.pid, p.info['username'], round(p.info['memory_info'].rss), p.info['cpu_percent'],p.info['memory_percent'], p.info['name']]
        proc_objects.append(process_info)
        td_buttons = ['hangup', 'terminate', 'kill']
        if request.method == "POST":
            if form.is_valid():
                if p.name() == form.cleaned_data['comment']:
                    p.kill()

    context_processes = {
        'proc_objects': proc_objects,
        'td_buttons': td_buttons,
        'form': form
    }
    return render(request, 'landing/test.html', context_processes)