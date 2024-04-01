from typing import Any
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task, TaskGroup
from .forms import TaskForm


def index(request):
    return HttpResponse('Hello World')


def task_list(request):
    tasks = Task.objects.all()
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = Task()
            task.name = form.cleaned_data.get('name')
            task.due_date = form.cleaned_data.get('due_date')
            task.taskgroup = form.cleaned_data.get('taskgroup')
            task.save()
    ctx = { "tasks": tasks, 
            "taskgroups": TaskGroup.objects.all(),
            "form": form # if post -> have form data else no form data
    }
    return render(request, 'task_list.html', ctx)


def task_detail(request, pk):
    task = Task.objects.get(pk=pk)
    ctx = {
        'task' : task
    }
    return render(request, 'task_detail.html', ctx)


class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            ctx = super().get_context_data(**kwargs)
            ctx['taskgroups'] = TaskGroup.objects.all()
            ctx['form'] = TaskForm()
            return ctx
        

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = Task()
            task.name = form.cleaned_data.get('name')
            task.due_date = form.cleaned_data.get('due_date')
            task.taskgroup = form.cleaned_data.get('taskgroup')
            task.save()
            return self.get(request, *args, **kwargs)
        else:
            self.object_list = self.get_queryset(**kwargs)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_create.html'
    # success_url = reverse('tasks:list)

    def get_success_url(self):
        return super().get_success_url()


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_detail.html'