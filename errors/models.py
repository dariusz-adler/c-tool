from django.db import models
from django.contrib.auth.models import Permission, User
import re


class Error(models.Model):
    user = models.ForeignKey(User, default=1)
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

    test_environment = models.CharField(max_length=200, blank=False,
                                        choices=[('ufte', 'ufte'), ('hibiscus', 'hibiscus')],
                                        null=False)

    fault_area = models.CharField(max_length=200, blank=False,
                                  choices=[('CI Fault', 'CI Fault'), ('Product Fault', 'Product Fault')],
                                  null=False)

    state = models.CharField(max_length=200, blank=False,
                             choices=[('in progress', 'in progress'), ('frozen', 'frozen'), ('solved', 'solved')],
                             null=False)

    comment = models.TextField(max_length=1000)
    env_version = models.CharField(max_length=100)

    def get_fields(self):
        return [(field.name, field.value_to_string(self)) for field in Error._meta.fields]

    def __str__(self):
        return '{} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(self.slogan,
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

    def parse_issue_id_to_url_address(self):
        pattern = r'[a-zA-Z]{2}\d{5}'
        matcher = re.match(pattern, self.issue_id)

        if matcher:
            self.issue_id = "https://mhweb.ericsson.se/TREditWeb/faces/oo/object.xhtml?eriref={}&mode=VIEW".format(self.issue_id)

        pattern = r'[a-zA-Z]{3}-[a-zA-Z]{2}-\d{3}'
        matcher = re.match(pattern, self.issue_id)

        if matcher:
            self.issue_id = "http://fht.lmera.ericsson.se/edit_report.php?report={}".format(self.issue_id)

        pattern = r'EHLIGSM-\d+'
        matcher = re.match(pattern, self.issue_id)

        if matcher:
            self.issue_id = "https://jira.lmera.ericsson.se/browse/{}".format(self.issue_id)

        pattern = r'LSUMSSIM-\d+'
        matcher = re.match(pattern, self.issue_id)

        if matcher:
            self.issue_id = "https://track.lineserver.net/browse/{}".format(self.issue_id)

        pattern = r'(CYCLONE-\d+)?(XFTBEAVER-\d+)?(HIBISCUS-\d+)?(TWOGSIMCS-\d+)?'
        matcher = re.match(pattern, self.issue_id)

        if matcher:
            self.issue_id = "https://wcdma-jira.rnd.ki.sw.ericsson.se/browse/{}".format(self.issue_id)

    def parse_url_address_to_issue_id(self):
        pattern = r'.*eriref=([A-Z]{2}\d{5})'
        matcher = re.match(pattern, self.issue_id)

        if matcher:
            return matcher.group(1)

        pattern = r'.*report=([a-zA-Z]{3}-[a-zA-Z]{2}-\d+)'
        matcher = re.match(pattern, self.issue_id)

        if matcher:
            return matcher.group(1)

        pattern = r'.*browse\/(.+)'
        matcher = re.match(pattern, self.issue_id)

        if matcher:
            return matcher.group(1)
