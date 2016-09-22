from django import forms
from .models import Error


class ErrorForm(forms.ModelForm):

    error_code = forms.CharField(required=False)
    suite = forms.CharField(required=False)
    script_label = forms.CharField(required=False)
    jenkins_path = forms.CharField(required=False)
    env_version = forms.CharField(required=False)

    class Meta:
        model = Error
        fields = ['user','slogan', 'issue_id', 'error_code', 'config_id', 'software_label', 'tc_number', 'suite',
                  'script_label', 'date', 'jenkins_path', 'test_environment', 'fault_area', 'state', 'comment',
                  'env_version']


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

