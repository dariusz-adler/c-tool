from django import forms
from .models import Error, UserComment, ChangeHistory
from django.core.exceptions import ValidationError
import re


def validate_issue_id(value):
    pattern_list = [r'^CYCLONE-\d+', r'^XFTBEAVER-\d+', r'^EHLIGSM-\d+', r'^LSUMSSIM-\d+', r'^HIBISCUS-\d+',
                    r'^TWOGSIMCS-\d+', r'^[A-Z]{2}\d{5}', r'^[A-Z]{3}-[A-Z]{2}-\d+', r'^TBD$']

    if not any(re.match(pattern, value) for pattern in pattern_list):
        raise ValidationError('%(value)s is not an even number', params={'value': value})


class ErrorForm(forms.ModelForm):

    issue_id = forms.CharField(validators=[validate_issue_id])
    error_code = forms.CharField(required=False)
    suite = forms.CharField(required=False)
    script_label = forms.CharField(required=False)
    jenkins_path = forms.CharField(required=False)
    env_version = forms.CharField(required=False)

    class Meta:
        model = Error
        fields = ['slogan', 'issue_id', 'error_code', 'config_id', 'software_label', 'tc_number', 'suite',
                  'script_label', 'date', 'jenkins_path', 'test_environment', 'fault_area', 'state', 'comment',
                  'env_version']

class EditErrorForm(forms.ModelForm):

    issue_id = forms.CharField(validators=[validate_issue_id])
    error_code = forms.CharField(required=False)
    suite = forms.CharField(required=False)
    script_label = forms.CharField(required=False)
    jenkins_path = forms.CharField(required=False)
    env_version = forms.CharField(required=False)

    class Meta:
        model = Error
        fields = ['slogan', 'issue_id', 'error_code', 'config_id', 'software_label', 'tc_number', 'suite',
                  'script_label', 'date', 'jenkins_path', 'test_environment', 'fault_area', 'state',
                  'env_version', 'change_description']


class SearchForm(forms.ModelForm):
    slogan = forms.CharField(required=False)
    issue_id = forms.CharField(required=False)
    error_code = forms.CharField(required=False)
    config_id = forms.CharField(required=False)
    software_label = forms.CharField(required=False)
    tc_number = forms.CharField(required=False)
    suite = forms.CharField(required=False)
    script_label = forms.CharField(required=False)
    date = forms.DateField(required=False)
    jenkins_path = forms.CharField(required=False)
    test_environment = forms.ChoiceField(required=False, choices=[('',''),('ufte', 'ufte'), ('hibiscus', 'hibiscus')])
    fault_area = forms.ChoiceField(required=False, choices=[('',''),('CI Fault', 'CI Fault'), ('Product Fault', 'Product Fault')])
    state = forms.ChoiceField(required=False, choices=[('',''),('in progress', 'in progress'), ('frozen', 'frozen'), ('solved', 'solved')])
    comment = forms.CharField(required=False)
    env_version = forms.CharField(required=False)

    class Meta:
        model = Error
        fields = ['slogan', 'issue_id', 'error_code', 'config_id', 'software_label', 'tc_number', 'suite',
                  'script_label', 'date', 'jenkins_path', 'test_environment', 'fault_area', 'state', 'comment',
                  'env_version']


class UserCommentForm(forms.ModelForm):

    user_comment = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows':8, 'cols':83}))

    class Meta:
        model = UserComment
        fields = ['user_comment']


class HistoryForm(forms.ModelForm):

    history_record = forms.CharField(required=True)

    class Meta:
        model = ChangeHistory
        fields = ['history_record']