import unittest
from django.test import TestCase
from .models import Job
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from .tasks import sec3
from selenium import webdriver
import time



class JobTest(TestCase):

    def create_job(self, name="1000", status='started'):
        return Job.object.create(name=name, status=status, created=timezone.now())

    
    def test_job_creation(self):
        j = self.create_job()
        self.assertTrue(isinstance(j, Job))
        self.assertEqual(j.__unicode__(), j.name)


    def test_completed_job(self, name="1", status="completed"):
        """
           Mocking creation dates and celery_id
           as well as result_dict and result_str
        """
        t_create = timezone.now()
        j = self.create_job()
        j.created = t_create
        j.celery_id = 1
        j.result_dict = {'1': 1}
        j.result_str = "The prime factors are 1^(1)"
        self.assertEqual(j.created, t_create)
        self.assertEqual(j.celery_id, 1)
        self.assertEquals(j.result_dict, {'1': 1})
        self.assertEqual(j.result_str, "The prime factors are 1^(1)")


class TestJobsUI(TestCase):

    def create_job(self, name="1000", status='started'):
        return Job.object.create(name=name, status=status, created=timezone.now())


    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(TestJobsUI, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(TestJobsUI, self).tearDown()


    def test_job_view(self):
        j = self.create_job()
        j.name = 12345
        url = reverse('.views.index')
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)
        self.assertInHTML(j.name, resp.content)
        self.assertInHTML(j.status, resp.content)


    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
                       CELERY_ALWAYS_EAGER=True,
                       BROKER_BACKEND='memory')
    def test_run_job(self):
        result = sec3.delay()
        self.assertTrue(result.successful())


    def test_page_layout(self):
        selenium = self.selenium
        self.create_job()
        selenium.get("http://localhost:8000/")
        selenium.find_element_by_id('id_title').send_keys("test title")
        selenium.find_element_by_id('id_body').send_keys("test body")
        selenium.find_element_by_id('task_name').send_keys('1')
        selenium.find_element_by_id('go').click()
        # Selenium runs by default on port 8081 instead of 8000
        # otherwise use LiveServerTestCase
        self.assertIn("http://localhost:8081/", selenium.current_url)
        assert '1' in selenium.page_source
        assert "started" in selenium.page_source
        assert "No result available" in selenium.page_source
        # wait some time and check if completed
        time.sleep(5)
        assert "completed" in selenium.page_source


if __name__ == '__main__':
    unittest.main()
