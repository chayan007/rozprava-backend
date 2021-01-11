from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from .models import Case


# Create your views here.
class CaseListView(ListView):
    paginate_by = 30

    def get_queryset(self):
        queryset=Case.objects.all()
        if self.kwargs.get('category'):
            queryset=queryset.filter(category=self.kwargs.get('category'))
        return queryset

# class CaseView(View):
