from django.contrib import admin

from .models import TaskGroup, Task


class TaskInline(admin.TabularInline):
    model = Task


class TaskGroupAdmin(admin.ModelAdmin):
    model = TaskGroup


class TaskAdmin(admin.ModelAdmin):
    model = Task

    search_fields = ['name',]
    list_display = ['name', 'due_date',]
    list_filter = ['due_date', 'taskgroup',]
    
    fieldsets = [
        ('Details', {
            'fields':[
                ('name', 'due_date'), 'taskgroup'
            ]
        })
    ]

admin.site.register(Task, TaskAdmin)


# pass is testingdjango