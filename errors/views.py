from .forms import ErrorForm
from django.shortcuts import render
from .models import Error
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def index(request):
    all_errors = Error.objects.all()
    context = {'all_errors': all_errors,
               'fields': Error().get_fields()}
    return render(request, 'errors/index.html', context)


def detail(request, error_id):
    error = Error.objects.get(pk=error_id)
    return render(request, 'errors/detail.html', {'error': error})


def asc_sorting(request, column):
    sorted_errors = Error.objects.order_by(column)
    context = {'all_errors': sorted_errors,
               'fields': Error().get_fields(),
               'column': column,
               'ordered': 'asc'}
    return render(request, 'errors/index.html', context)


def desc_sorting(request, column):
    sorted_errors = Error.objects.order_by('-'+column)
    context = {'all_errors': sorted_errors,
               'fields': Error().get_fields(),
               'column': column,
               'ordered': 'desc'}
    return render(request, 'errors/index.html', context)


def add_error(request):
    if request.method == "POST":
        form = ErrorForm(request.POST)
        if form.is_valid():
            error = form.save()
            error.save()
            return HttpResponseRedirect(reverse('error:index'))
    else:
        form = ErrorForm()
    return render(request, 'errors/error_form.html', {'form': form})
