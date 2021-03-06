from .forms import ErrorForm, UserCommentForm, EditErrorForm, HistoryForm, SearchForm
from django.shortcuts import get_object_or_404, render
from .models import Error
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from ctool import settings
from django.core import serializers
from copy import deepcopy
from django.contrib.auth.models import User


def post_errors_to_session(request, errors):
    request.session['errors'] = serializers.serialize("json", errors)


def get_errors_from_session(request):
    if "errors" in request.session:
        keys = []
        for obj in serializers.deserialize("json", request.session['errors']):
            keys.append(obj.object.pk)

        errors = Error.objects.filter(pk__in=keys)
    else:
        errors = Error.objects.all()

    return errors


@login_required
def change_password(request):
    if request.method == "POST":
        old_pass = request.POST['old_password']
        new_pass = request.POST['new_password']
        new_pass_repeat = request.POST['new_password_repeat']
        user = User.objects.get(username__exact=request.user)
        if new_pass != new_pass_repeat:
            messages.warning(request, 'New password fields are different! ')
        if not user.check_password(old_pass):
            messages.warning(request, 'Old password is wrong')
        if user.check_password(old_pass) and new_pass == new_pass_repeat:
            user.set_password(new_pass)
            user.save()
            user = authenticate(username=request.user, password=new_pass)
            auth.login(request, user)
            messages.success(request, 'Password has been changed')
            return HttpResponseRedirect(reverse('error:index'))

    return render(request, 'errors/change_password.html')


def index(request):
    all_errors_list = Error.objects.order_by('-id')
    post_errors_to_session(request, all_errors_list)
    paginator = Paginator(all_errors_list, 50)
    page = request.GET.get('page')
    try:
        all_errors = paginator.page(page)
    except PageNotAnInteger:
        all_errors = paginator.page(1)
    except EmptyPage:
        all_errors = paginator.page(paginator.num_pages)
    query = request.GET.get("q")
    if query:
        fields = ['created_by', 'slogan', 'issue_id', 'error_code', 'config_id', 'software_label', 'tc_number', 'suite',
                  'script_label', 'date', 'jenkins_path', 'test_environment', 'fault_area', 'state', 'env_version']
        values = []
        for i in range(len(fields)):
            values.append(query)
        query_result = dynamic_query(request, Error, fields, values, 'or')
        return query_result
    else:
        context = {'all_errors': all_errors,
                   'fields': Error().get_fields(),}

    return render(request, 'errors/index.html', context)


def detail(request, error_id):
    error = Error.objects.get(pk=error_id)
    all_comments = error.main_error.all().order_by('-date', '-time')
    all_history = error.history_error.all().order_by('-date', '-time')

    form = UserCommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save()
        comment.error = error
        comment.user = request.user
        comment.save()
        messages.success(request, 'Comment has been added')
        return HttpResponseRedirect('/details/{}'.format(error_id))

    context = {'error': error,
               'form': form,
               'all_comments': all_comments,
               'all_history': all_history,}

    return render(request, 'errors/detail.html', context)


def sorting(request, column, direction):
    errors = get_errors_from_session(request)

    if direction == 'asc':
        sorted_errors = errors.order_by(column)
        direction = 'desc'
        icon = 'fa fa-sort-asc'
    elif direction == 'desc':
        sorted_errors = errors.order_by('-' + column)
        direction = 'asc'
        icon = 'fa fa-sort-desc'
    else:
        sorted_errors = errors
        icon = 'fa fa-sort'

    post_errors_to_session(request, sorted_errors)

    paginator = Paginator(sorted_errors, 50)
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
               'direction': direction,
               'icon': icon}

    return render(request, 'errors/index.html', context)


def add_error(request):
    button_role = 'ADD'
    window_role = 'ADD ERROR'
    if request.method == "POST":
        form = ErrorForm(request.POST)
        if form.is_valid():
            error = form.save(commit=False)
            error.created_by = request.user
            error.issue_id = error.parse_issue_id_to_url_address()
            error.save()
            messages.success(request, 'Error has beed added with id: {}'.format(error.id))
            return HttpResponseRedirect(reverse('error:index'))
        else:
            messages.warning(request, form.errors)
    else:
        form = ErrorForm()
    return render(request, 'errors/error_form.html', {'form': form, 'button_role': button_role,
                                                      'window_role': window_role,})


def create_copy(request, error_id):
    button_role = 'CREATE'
    window_role = 'CREATE COPY'
    error = Error.objects.get(id=error_id)
    form = ErrorForm(request.POST or None, instance=error)

    if request.method == "POST":

        if form.is_valid():
            error_copy = deepcopy(error)
            error_copy.id = None
            error_copy.created_by = request.user
            error_copy.issue_id = error.parse_issue_id_to_url_address()
            error_copy.save()
            messages.success(request, 'Error copy has beed created with id: {}'.format(error_copy.id))
            return HttpResponseRedirect(reverse('error:index'))
        else:
            messages.warning(request, form.errors)

    context = {
        'error': error,
        'form': form,
        'button_role': button_role,
        'window_role': window_role,
    }
    return render(request, 'errors/error_form.html', context)


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
                                                          'button_role': button_role,})


def dynamic_query(request, model, fields, values, operator):
    queries = []
    for (f, v) in zip(fields, values):
        if v != "":
            kwargs = {str('%s__icontains' % f): str('%s' % v)}
            queries.append(Q(**kwargs))
    if len(queries) > 0:
        q = Q()
        for query in queries:
            if operator == "and":
                q = q & query
            elif operator == "or":
                q = q | query
            else:
                q = None
        if q:
            errors = model.objects.filter(q)
            post_errors_to_session(request, errors)
            context = {'all_errors': errors,
                       'fields': Error().get_fields(),}
            return render(request, 'errors/index.html', context)
    else:
        all_errors = model.objects.all()
        post_errors_to_session(request, all_errors)
        context = {'all_errors': all_errors,
                   'fields': Error().get_fields(),}
        return render(request, 'errors/index.html', context)


@login_required
def update_error(request, error_id):
    button_role = 'UPDATE'
    window_role = 'UPDATE ERROR'
    error = get_object_or_404(Error, id=error_id)
    form = EditErrorForm(request.POST or None, instance=error)
    form2 = HistoryForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            error = form.save(commit=False)
            error.issue_id = error.parse_issue_id_to_url_address()
            error.save()

            history = form2.save()
            history.error = error
            history.user = request.user
            history.save()
            messages.success(request, 'Error with id {} has beed updated'.format(error.id))
            return HttpResponseRedirect('/details/{}'.format(error_id))
        else:
            messages.warning(request, form.errors)

    context = {
        'error': error,
        'form': form,
        'form2': form2,
        'button_role': button_role,
        'window_role': window_role,
    }
    return render(request, 'errors/error_form.html', context)


def login_user(request):
    next = request.GET.get('next', 'index/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(next)
            else:
                return render(request, 'errors/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'errors/login.html', {'error_message': 'Invalid login'})
    return render(request, "errors/login.html", {'redirect_to': next})


def logout_user(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('error:index'))
