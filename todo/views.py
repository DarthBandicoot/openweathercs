from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import ListView, FormView, DeleteView, DetailView, CreateView, UpdateView

from todo.forms import AccountForm, AddTaskForm
from todo.models import Tasks, TodoList, Locations
from todo.utils import get_weather


class AccountView(FormView):
    template_name = 'todo/generic_form.html'
    form_class = AccountForm
    todolist = None
    user_exist = None
    pin_code = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def form_valid(self, form):
        self.user_exist = User.objects.get_or_create(username=form.cleaned_data['username'],
                                                     email=form.cleaned_data['email'])
        self.pin_code = form.cleaned_data['pin']
        return super().form_valid(form)

    def get_success_url(self):
        self.get_todolist()
        return reverse_lazy('todo-list:todo_list', kwargs={'todo_list_id': self.todolist.id})

    def get_todolist(self):
        if len(self.user_exist) > 0:
            owner = self.user_exist[0]
        else:
            owner = self.user_exist
        self.todolist = TodoList.objects.filter(owner=owner.id, pin__exact=self.pin_code).first()
        if not self.todolist:
            self.todolist = TodoList.objects.create(owner=owner, title="TODO List", pin=self.pin_code)


class TodoListView(ListView):
    template_name = 'todo/todo_list.html'
    context_object_name = 'tasks_list'
    todo_list = None

    def dispatch(self, request, *args, **kwargs):
        self.todo_list = get_object_or_404(TodoList, pk=self.kwargs['todo_list_id'])

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo_list'] = self.todo_list.id
        context['cold'] = '#0E86D4'
        context['warm'] = '#FF8300'
        context['hot'] = '#FF2511'
        return context

    def get_queryset(self):
        return Tasks.objects.filter(todolist=self.todo_list)


class ParentTaskView:
    model = Tasks
    template_name = 'todo/generic_form.html'
    todo_list = None
    task = None

    def dispatch(self, request, *args, **kwargs):
        self.todo_list = get_object_or_404(TodoList, pk=self.kwargs['todo_list_id'])
        if self.kwargs.get('pk'):
            self.task = get_object_or_404(Tasks, pk=self.kwargs['pk'])

        return super().dispatch(request, *args, **kwargs)

    def set_temperature(self, location):
        city = Locations.objects.get(pk=location.id)
        print("CITY: {}".format(city))
        city.temperature = get_weather(city)
        print("TEMP: {}".format(city.temperature))
        city.save()


class AddTaskView(ParentTaskView, FormView):
    """
    This view allows the user to Add a new Task
    """
    form_class = AddTaskForm

    def form_valid(self, form):
        self.set_temperature(form.cleaned_data['location'])
        self.create_task(form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('todo-list:todo_list', kwargs={'todo_list_id': self.todo_list.id})

    def create_task(self, data):
        Tasks.objects.create(title=data['title'], description=data['description'],
                             location=Locations.objects.get(pk=data['location'].id), owner=self.todo_list.owner,
                             todolist=self.todo_list)


class EditTaskView(ParentTaskView, UpdateView):
    """
    This view allows the user to edit a Task
    """
    form_class = AddTaskForm

    def form_valid(self, form):
        self.set_temperature(form.cleaned_data['location'])
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        if self.task is not None:
            initial['title'] = self.task.title
            initial['description'] = self.task.description
            initial['location'] = self.task.location
            initial['status'] = self.task.status

        return initial

    def get_success_url(self):
        return reverse_lazy('todo-list:todo_list', kwargs={'todo_list_id': self.todo_list.id})


def delete_task(request, todo_list_id, pk):
    """
    This function deletes a selected Task
    """

    Tasks.objects.get(pk=pk).delete()
    return redirect('todo-list:todo_list', todo_list_id=todo_list_id)


class ActiveTaskView(ParentTaskView, DetailView):
    pass
