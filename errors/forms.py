from django import forms
from .models import Error


class ErrorForm(forms.ModelForm):

    class Meta:
        model = Error
        fields = ['slogan', 'issue_id', 'error_code', 'config_id', 'software_label', 'tc_number', 'suite',
                  'script_label', 'date', 'jenkins_path', 'test_environment', 'fault_area', 'state', 'comment',
                  'env_version']

