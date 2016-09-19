from .forms import ErrorForm
from django.shortcuts import get_object_or_404
from .forms import SearchForm
from django.shortcuts import render
from .models import Error
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


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
    query = request.GET.get("q")
    if query:
        fields = ['slogan', 'issue_id', 'error_code', 'config_id', 'software_label', 'tc_number', 'suite',
                  'script_label', 'jenkins_path', 'test_environment', 'state']
        values = []
        for i in range(len(fields)):
            values.append(query)
        query_result = dynamic_query(request, Error, fields, values, 'or')
        return query_result
    else:
        context = {'all_errors': all_errors,
                   'fields': Error().get_fields()}

    return render(request, 'errors/index.html', context)


def detail(request, error_id):
    error = Error.objects.get(pk=error_id)
    return render(request, 'errors/detail.html', {'error': error})


def sorting(request, column, direction):
    errors = Error.objects.all()

    if direction == 'asc':
        sorted_errors = errors.order_by(column)
    elif direction == 'desc':
        sorted_errors = errors.order_by('-' + column)
    else:
        sorted_errors = errors

    paginator = Paginator(sorted_errors, 15)
    page = request.GET.get('page')

    try:
        sorted_errors = paginator.page(page)
    except PageNotAnInteger:
        sorted_errors = paginator.page(1)
    except EmptyPage:
        sorted_errors = paginator.page(paginator.num_pages)

    context = {'all_errors': sorted_errors,
               'fields': Error().get_fields(),
               'column': column,
               'direction': direction}
    return render(request, 'errors/index.html', context)


def add_error(request):
    button_role = 'ADD'
    window_role = 'ADD ERROR'
    if request.method == "POST":
        form = ErrorForm(request.POST)
        if form.is_valid():
            error = form.save()
            error.save()
            messages.success(request, 'Error has beed added with id: {}'.format(error.id))
            return HttpResponseRedirect(reverse('error:index'))
    else:
        form = ErrorForm()
    return render(request, 'errors/error_form.html', {'form': form, 'button_role': button_role,
                                                      'window_role': window_role})


def advanced_search(request):
    window_role = "ADVANCED SEARCH"
    button_role = 'SEARCH'
    if request.method == "POST":
        slogan = request.POST.get("slogan")
        issue_id = request.POST.get("issue_id")
        error_code = request.POST.get("error_code")
        config_id = request.POST.get("config_id")
        software_label = request.POST.get("software_label")
        tc_number = request.POST.get("tc_number")
        suite = request.POST.get("suite")
        script_label = request.POST.get("script_label")
        date = request.POST.get("date")
        jenkins_path = request.POST.get("jenkins_path")
        test_environment = request.POST.get("test_environment")
        state = request.POST.get("state")

        fields = ['slogan', 'issue_id', 'error_code', 'config_id', 'software_label', 'tc_number', 'suite',
                  'script_label', 'date', 'jenkins_path', 'test_environment', 'state']
        values = [slogan, issue_id, error_code, config_id, software_label, tc_number, suite, script_label, date,
                  jenkins_path, test_environment, state]
        query_result = dynamic_query(request, Error, fields, values, 'and')
        return query_result
    else:
        form = SearchForm()
        return render(request, 'errors/error_form.html', {'form': form, 'window_role': window_role,
                                                          'button_role': button_role})


def dynamic_query(request, model, fields, values, operator):
    queries = []
    for (f, v) in zip(fields, values):
        if v != "":
            kwargs = {str('%s__exact' % f): str('%s' % v)}
            queries.append(Q(**kwargs))
    if len(queries) > 0:
        print(queries)
        q = Q()
        for query in queries:
            if operator == "and":
                q = q & query
            elif operator == "or":
                q = q | query
            else:
                q = None
        if q:
            context = {'all_errors': model.objects.filter(q),
                       'fields': Error().get_fields()}
            return render(request, 'errors/index.html', context)
    else:
        all_errors = model.objects.all()
        context = {'all_errors': all_errors,
                   'fields': Error().get_fields()}
        return render(request, 'errors/index.html', context)


def update_error(request, error_id):
    button_role = 'UPDATE'
    window_role = 'UPDATE ERROR'
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
        'button_role': button_role,
        'window_role': window_role,
    }
    return render(request, 'errors/error_form.html', context)
