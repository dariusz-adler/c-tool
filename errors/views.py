from .forms import ErrorForm
from django.shortcuts import render, get_object_or_404
from .models import Error
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    all_errors_list = Error.objects.all()
    paginator = Paginator(all_errors_list, 15)
    page = request.GET.get('page')
    try:
        all_errors = paginator.page(page)
    except PageNotAnInteger:
        all_errors = paginator.page(1)
    except EmptyPage:
        all_errors = paginator.page(paginator.num_pages)
    context = {'all_errors': all_errors}

    return render(request, 'errors/index.html', context)


def detail(request, error_id):
    error = Error.objects.get(pk=error_id)
    return render(request, 'errors/detail.html', {'error': error})


def add_error(request):
    button_role = 'ADD'
    if request.method == "POST":
        form = ErrorForm(request.POST)
        if form.is_valid():
            error = form.save()
            error.save()
            messages.success(request, 'Error has beed added with id: {}'.format(error.id))
            return HttpResponseRedirect(reverse('error:index'))
    else:
        form = ErrorForm()
    return render(request, 'errors/error_form.html', {'form': form, 'button_role': button_role})


def update_error(request, error_id):
    button_role = 'UPDATE'
    error = get_object_or_404(Error, id=error_id)
    form = ErrorForm(request.POST or None, instance=error)
    if form.is_valid():
        error = form.save(commit=False)
        error.save()
        messages.success(request, 'Error with id {} has beed updated'.format(error.id))
        return HttpResponseRedirect(reverse('error:index'))

    context = {
        'error': error,
        'form': form,
        'button_role': button_role
    }
    return render(request, 'errors/error_form.html', context)