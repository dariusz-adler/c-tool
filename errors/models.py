from django.db import models


class Error(models.Model):
    slogan = models.CharField(max_length=200)
    issue_id = models.CharField(max_length=200)
    error_code = models.CharField(max_length=200)
    config_id = models.CharField(max_length=200)
    software_label = models.CharField(max_length=200)
    tc_number = models.CharField(max_length=200)
    suite = models.CharField(max_length=200)
    script_label = models.CharField(max_length=200)
    date = models.DateField()
    jenkins_path = models.CharField(max_length=200)

    test_environment = models.CharField(max_length=200, default='', choices=[('ufte', 'ufte'), ('hibiscus',
                                                                                                'hibiscus')])
    fault_area = models.CharField(max_length=200, default='', choices=[('CI Fault', 'CI Fault'), ('Product Fault',
                                                                                                  'Product Fault')])
    state = models.CharField(max_length=200, default='', choices=[('in progress', 'in progress'), ('frozen', 'frozen'),
                                                                  ('solved', 'solved')])

    comment = models.CharField(max_length=1000)
    env_version = models.CharField(max_length=100)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Error._meta.fields]

    def __str__(self):
        return '{} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(self.issue_id,
                                                                  self.issue_id,
                                                                  self.error_code,
                                                                  self.config_id,
                                                                  self.software_label,
                                                                  self.tc_number,
                                                                  self.suite,
                                                                  self.script_label,
                                                                  self.date,
                                                                  self.jenkins_path,
                                                                  self.test_environment,
                                                                  self.fault_area,
                                                                  self.state,
                                                                  self.env_version)
