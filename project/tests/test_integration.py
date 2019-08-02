import filecmp
import os
import time

from selenium_base import SeleniumTestsBase

from django.conf import settings
from django.urls import reverse

from project.models import Project
from project.models import SystemAllocationRequest
from project.models import ProjectUserMembership
from users.models import CustomUser
from users.models import Profile


class ProjectIntegrationTests(SeleniumTestsBase):

    settings.MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'tmp')
    settings.MEDIA_URL = '/tmp/'

    test_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_file.txt')

    default_allocation_form_fields = {
        "id_start_date": "2018-09-17",
        "id_end_date": "2019-09-17",
        "id_requirements_software": "none",
        "id_requirements_training": "none",
        "id_requirements_onboarding": "none",
        "id_allocation_cputime": "87695464",
        "id_allocation_memory": "1",
        "id_allocation_storage_home": "200",
        "id_allocation_storage_scratch": "1",
        'id_document': test_file,
    }

    default_project_form_fields = {
        "id_title": "Test project",
        "id_description": "This project aims to test the submission of projects",
        "id_department": "SA2C",
        "id_supervisor_name": "Joe Bloggs",
        "id_supervisor_position": "RSE",
        "id_supervisor_email": "joe.bloggs@example2.ac.uk",
    }

    def test_create_project_missing_fields(self):
        """
        Test project creation and project membership workflows
        with missing fields
        """
        self.sign_in(self.user)

        # Fill the project form with a field missing
        missing_fields = [
            'id_title',
            'id_description',
        ]
        for missing_field in missing_fields:
            self.get_url('')
            self.click_link_by_url(reverse('create-project'))
            form_field = dict(self.default_project_form_fields)
            form_field.pop(missing_field)
            self.fill_form_by_id(form_field)
            self.submit_form(self.default_project_form_fields)
            if "This field is required." not in self.selenium.page_source:
                raise AssertionError()

    def test_create_allocation_missing_fields(self):
        """
        Test project creation and project membership workflows
        with missing fields
        """
        self.sign_in(self.user)

        self.get_url('')
        self.click_link_by_url(reverse('create-project'))
        self.fill_form_by_id(self.default_project_form_fields)
        self.submit_form(self.default_project_form_fields)
        project = Project.objects.get(title=self.default_project_form_fields['id_title'])

        # Fill the project form with a field missing
        missing_fields = [
            "id_start_date",
            "id_end_date",
        ]
        for missing_field in missing_fields:
            self.get_url(reverse('project-application-detail', kwargs={'pk': project.id}))
            self.click_link_by_url(reverse('create-allocation', kwargs={'project': project.id}))
            form_field = dict(self.default_allocation_form_fields)
            form_field.pop(missing_field)
            self.fill_form_by_id(form_field)
            # Submitting with the time field fills it, so use a different one
            self.submit_form({"id_allocation_cputime": ""})
            if "This field is required." not in self.selenium.page_source:
                raise AssertionError()

    def test_create_project_and_allocation_missing_fields(self):
        """
        Test project creation and project membership workflows
        with missing fields
        """
        institution = self.user.profile.institution
        institution.separate_allocation_requests = False

        # Also test the funding source creation part without approval
        institution.needs_funding_approval = False

        institution.save()
        self.sign_in(self.user)

        # Fill the project form with a field missing
        missing_fields = [
            'id_title',
            'id_description',
        ]
        for missing_field in missing_fields:
            self.get_url('')
            self.click_link_by_url(reverse('create-project-and-allocation'))
            form_field = dict(self.default_project_form_fields)
            form_field.pop(missing_field)
            self.fill_form_by_id(form_field)
            self.fill_form_by_id(self.default_allocation_form_fields)
            self.submit_form(self.default_project_form_fields)
            if "This field is required." not in self.selenium.page_source:
                raise AssertionError()

        # Fill the allocation form with a field missing
        missing_fields = [
            "id_start_date",
            "id_end_date",
        ]
        for missing_field in missing_fields:
            self.get_url('')
            self.click_link_by_url(reverse('create-project-and-allocation'))
            form_field = dict(self.default_allocation_form_fields)
            form_field.pop(missing_field)
            self.fill_form_by_id(self.default_project_form_fields)
            self.fill_form_by_id(form_field)
            self.submit_form(self.default_project_form_fields)
            if "This field is required." not in self.selenium.page_source:
                raise AssertionError()

    def test_create_project_with_authorised_user(self):
        # Test the workflow for project creation when separate allocations
        # are enabled

        self.sign_in(self.user)

        self.get_url('')
        self.click_link_by_url(reverse('create-project'))

        # Correctly fill the form
        self.fill_form_by_id(self.default_project_form_fields)
        # self.select_from_dropdown_by_id('id_funding_source', 1)

        # Check that the project does not exist yet
        matching_projects = Project.objects.filter(title=self.default_project_form_fields['id_title'])
        assert matching_projects.count() == 0
        # Add a funding source and include it
        self.click_link_by_url(reverse('add-funding-source')+'?_popup=1')

        main_window_handle = self.selenium.current_window_handle
        self.selenium.switch_to.window(self.selenium.window_handles[1])

        identifier_fields = {'id_identifier' : 'Identifier'}
        self.fill_form_by_id(identifier_fields)
        self.submit_form(identifier_fields)

        fundingsource_fields = {
            'id_title': 'Title',
            'id_pi_email': self.user.email,
            'id_amount': 2340983,
        }

        self.fill_form_by_id(fundingsource_fields)
        self.select_from_dropdown_by_id('id_funding_body', 1)

        # click save first time
        self.submit_form(fundingsource_fields)

        # ...need to click save twice (this is the workflow!)
        self.submit_form(fundingsource_fields)

        self.selenium.switch_to.window(main_window_handle)

        # Add a publication and include it
        self.click_link_by_url(reverse('create-publication')+'?_popup=1')

        main_window_handle = self.selenium.current_window_handle
        self.selenium.switch_to.window(self.selenium.window_handles[1])

        publication_fields = {
            'id_title': 'Title',
            'id_url': 'http://arxiv.org/abs/1806.06043',
        }
        self.fill_form_by_id(publication_fields)
        self.submit_form(publication_fields)
        
        self.selenium.switch_to.window(main_window_handle)

        # Submit the form
        self.submit_form(self.default_project_form_fields)

        if "This field is required." in self.selenium.page_source:
            raise AssertionError()
        # if "Successfully submitted a project application." not in self.selenium.page_source:
        #     raise AssertionError()

        # Check that a project was created
        matching_projects = Project.objects.filter(title=self.default_project_form_fields['id_title'])
        if matching_projects.count() != 1:
            raise AssertionError()
        
        project = matching_projects.first()
        
        #create system allocation
        self.click_link_by_url(reverse('create-allocation', kwargs={'project': project.id}))
        form_field = dict(self.default_allocation_form_fields)
        self.fill_form_by_id(self.default_allocation_form_fields)
#Needs to be run twice because selenium seems to get stuck on the date selection otherwise and doesn't submit the form
        self.submit_form(self.default_allocation_form_fields)
        self.submit_form(self.default_allocation_form_fields)
        #Aprove the system alocation
        SystemAllocationRequest.objects.filter(project=project).update(status=1)
        
        #check that allocation was created
        matching_allocations = SystemAllocationRequest.objects.filter(project=project)
        if matching_allocations.count() != 1:
            raise AssertionError()

        # Check the project status
        self.get_url(reverse('project-application-list'))
        self.click_link_by_url(reverse('project-application-detail', kwargs={'pk': project.id}))
        if self.default_project_form_fields["id_title"] not in self.selenium.page_source:
            raise AssertionError()

        # Check that the technical lead is the user
        tech_lead_id = project.tech_lead.id
        user_id = self.user.id
        if tech_lead_id != user_id:
            raise AssertionError()

        # Check that the user was added to project_owners
        if not self.user.groups.filter(name='project_owner').exists():
            raise AssertionError()

        # Try the Project Applications and Project Memberships pages
        self.get_url(reverse('project-application-list'))
        if self.default_project_form_fields["id_title"] not in self.selenium.page_source:
            raise AssertionError()

        self.click_link_by_url(reverse('project-application-detail', kwargs={'pk': project.id}))
        if self.default_project_form_fields["id_description"] not in self.selenium.page_source:
            raise AssertionError()

        self.get_url(reverse('project-membership-list'))
        if self.default_project_form_fields["id_title"] not in self.selenium.page_source:
            raise AssertionError()
        if 'Project Owner' not in self.selenium.page_source:
            raise AssertionError()

        # Login with a different user (student) and add the project
        self.log_out()
        self.sign_in(self.student)

        self.fill_form_by_id({'project_code': project.code})
        self.submit_form({'project_code': project.code})

        assert ProjectUserMembership.objects.filter(project=project, user=self.student).exists()
        if 'Successfully submitted a project membership request' not in self.selenium.page_source:
            raise AssertionError()

        # Try an incorrect code
        self.get_url('')
        self.fill_form_by_id({'project_code': 'Invalidcode1'})
        self.submit_form({'project_code': project.code})
        if 'Invalid Project Code' not in self.selenium.page_source:
            raise AssertionError()

        # Check that the project membership is visible
        self.get_url('')
        self.click_link_by_url(reverse('project-membership-list'))
        if 'Awaiting Authorisation' not in self.selenium.page_source:
            raise AssertionError()

        # Login with as the tech lead and authorize the new user
        self.log_out()
        self.sign_in(self.user)
        self.get_url(reverse('project-user-membership-request-list'))

        if self.student.email not in self.selenium.page_source:
            raise AssertionError()
        self.select_from_first_dropdown(1)

        # Login with student again and check authorisation
        self.log_out()
        self.sign_in(self.student)
        self.get_url('')
        self.click_link_by_url(reverse('project-membership-list'))

        if 'Authorised' not in self.selenium.page_source:
            raise AssertionError()

        # Log in as tech lead and invite a different user
        self.log_out()
        self.sign_in(self.user)
        self.get_url("")
        self.click_link_by_url(reverse('project-application-list'))
        self.click_link_by_url(reverse('project-application-detail',kwargs={'pk': project.id}))
        self.click_link_by_url(reverse('project-membership-invite',kwargs={'pk': project.id}))
        self.fill_form_by_id({'email': self.external.email})
        self.submit_form({'email': self.external.email})

        assert 'Successfully submitted an invitation.' in self.selenium.page_source
        project_membership = ProjectUserMembership.objects.filter(project=project, user=self.external)
        assert project_membership.exists()
        project_membership = project_membership.first()

        # Check that the request is visible in user-requests
        self.get_url('')
        self.click_link_by_url(reverse('project-user-membership-request-list'))
        assert self.external.email in self.selenium.page_source
        assert 'Authorised' in self.selenium.page_source

        # Login as external and authorise the invitation
        self.log_out()
        self.sign_in(self.external)
        self.click_link_by_url(reverse('project-membership-list'))
        assert project.code in self.selenium.page_source
        self.select_from_first_dropdown(1)

        # test disabled due to issues in development with serving js files
        # assert project_membership.status == ProjectUserMembership.AUTHORISED

        # Delete the project and check the user was deleted from project_owners
        project.delete()
        if self.user.groups.filter(name='project_owner').exists():
            raise AssertionError()

    def test_create_project_and_allocation(self):
        # Test the workflow for project creation when separate allocations
        # are not enabled
        institution = self.user.profile.institution
        institution.separate_allocation_requests = False

        # Also test the funding source creation part without approval
        institution.needs_funding_approval = False

        institution.save()

        self.sign_in(self.user)

        self.get_url('')
        self.click_link_by_url(reverse('create-project-and-allocation'))

        # Correctly fill the form
        self.fill_form_by_id(self.default_project_form_fields)
        self.fill_form_by_id(self.default_allocation_form_fields)
        # self.select_from_dropdown_by_id('id_funding_source', 1)

        # Check that the project does not exist yet
        matching_projects = Project.objects.filter(title=self.default_project_form_fields['id_title'])
        assert matching_projects.count() == 0

        # Add a funding source and include it
        self.click_link_by_url(reverse('add-funding-source')+'?_popup=1')

        main_window_handle = self.selenium.current_window_handle
        self.selenium.switch_to.window(self.selenium.window_handles[1])

        identifier_fields = {'id_identifier' : 'Identifier'}
        self.fill_form_by_id(identifier_fields)
        self.submit_form(identifier_fields)

        fundingsource_fields = {
            'id_title': 'Title',
            'id_pi_email': self.user.email,
            'id_amount': 2340983,
        }

        self.fill_form_by_id(fundingsource_fields)
        self.select_from_dropdown_by_id('id_funding_body', 1)

        # click save
        self.submit_form(fundingsource_fields)

        self.selenium.switch_to.window(main_window_handle)

        # Add a publication and include it
        self.click_link_by_url(reverse('create-publication')+'?_popup=1')

        main_window_handle = self.selenium.current_window_handle
        self.selenium.switch_to.window(self.selenium.window_handles[1])

        publication_fields = {
            'id_title': 'Title',
            'id_url': 'http://arxiv.org/abs/1806.06043',
        }
        self.fill_form_by_id(publication_fields)
        self.submit_form(publication_fields)

        self.selenium.switch_to.window(main_window_handle)

        # Submit the form
        self.submit_form(self.default_project_form_fields)

        if "This field is required." in self.selenium.page_source:
            raise AssertionError()
        if "Successfully submitted a project application." not in self.selenium.page_source:
            raise AssertionError()

        # Check that a project and an allocation was created
        matching_projects = Project.objects.filter(title=self.default_project_form_fields['id_title'])
        
        if matching_projects.count() != 1:
            raise AssertionError()
        
        project = matching_projects.first()
        matching_allocations = SystemAllocationRequest.objects.filter(project=project)
        if matching_allocations.count() != 1:
            raise AssertionError()

        #Aprove the system alocation
        SystemAllocationRequest.objects.filter(project=project).update(status=1)
        
        # Check the project status
        self.get_url(reverse('project-application-list'))
        self.click_link_by_url(reverse('project-application-detail', kwargs={'pk': project.id}))
        if self.default_project_form_fields["id_title"] not in self.selenium.page_source:
            raise AssertionError()
        
        #check the system allocation has been aproved
        if 'Awaiting Approval' in self.selenium.page_source:
            raise AssertionError()
        
        # Check that the technical lead is the user
        tech_lead_id = project.tech_lead.id
        user_id = self.user.id
        if tech_lead_id != user_id:
            raise AssertionError()

        # Check that the user was added to project_owners
        if not self.user.groups.filter(name='project_owner').exists():
            raise AssertionError()

        # Try the Project Applications and Project Memberships pages
        self.get_url(reverse('project-application-list'))
        if self.default_project_form_fields["id_title"] not in self.selenium.page_source:
            raise AssertionError()

        self.click_link_by_url(reverse('project-application-detail', kwargs={'pk': project.id}))
        if self.default_project_form_fields["id_description"] not in self.selenium.page_source:
            raise AssertionError()

        self.get_url(reverse('project-membership-list'))
        if self.default_project_form_fields["id_title"] not in self.selenium.page_source:
            raise AssertionError()
        if 'Project Owner' not in self.selenium.page_source:
            raise AssertionError()

        # Login with a different user (student) and add the project
        self.log_out()
        self.sign_in(self.student)

        self.fill_form_by_id({'project_code': project.code})
        self.submit_form({'project_code': project.code})

        assert ProjectUserMembership.objects.filter(project=project, user=self.student).exists()
        if 'Successfully submitted a project membership request' not in self.selenium.page_source:
            raise AssertionError()

        # Try an incorrect code
        self.get_url('')
        self.fill_form_by_id({'project_code': 'Invalidcode1'})
        self.submit_form({'project_code': project.code})
        if 'Invalid Project Code' not in self.selenium.page_source:
            raise AssertionError()

        # Check that the project membership is visible
        self.get_url('')
        self.click_link_by_url(reverse('project-membership-list'))
        if 'Awaiting Authorisation' not in self.selenium.page_source:
            raise AssertionError()

        # Login with as the tech lead and authorize the new user
        self.log_out()
        self.sign_in(self.user)
        self.get_url(reverse('project-user-membership-request-list'))

        if self.student.email not in self.selenium.page_source:
            raise AssertionError()
        self.select_from_first_dropdown(1)

        # Login with student again and check authorisation
        self.log_out()
        self.sign_in(self.student)
        self.get_url('')
        self.click_link_by_url(reverse('project-membership-list'))

        if 'Authorised' not in self.selenium.page_source:
            raise AssertionError()

        # Log in as tech lead and invite a different user
        self.log_out()
        self.sign_in(self.user)
        self.get_url("")
        self.click_link_by_url(reverse('project-application-list'))
        self.click_link_by_url(reverse('project-application-detail',kwargs={'pk': project.id}))
        self.click_link_by_url(reverse('project-membership-invite',kwargs={'pk': project.id}))
        self.fill_form_by_id({'email': self.external.email})
        self.submit_form({'email': self.external.email})

        assert 'Successfully submitted an invitation.' in self.selenium.page_source
        project_membership = ProjectUserMembership.objects.filter(project=project, user=self.external)
        assert project_membership.exists()
        project_membership = project_membership.first()

        # Check that the request is visible in user-requests
        self.get_url('')
        self.click_link_by_url(reverse('project-user-membership-request-list'))
        assert self.external.email in self.selenium.page_source
        assert 'Authorised' in self.selenium.page_source

        # Login as external and authorise the invitation
        self.log_out()
        self.sign_in(self.external)
        self.click_link_by_url(reverse('project-membership-list'))
        assert project.code in self.selenium.page_source
        self.select_from_first_dropdown(1)

        # test disabled due to issues in development with serving js files
        # assert project_membership.status == ProjectUserMembership.AUTHORISED

        # Delete the project and check the user was deleted from project_owners
        project.delete()
        if self.user.groups.filter(name='project_owner').exists():
            raise AssertionError()

    def test_create_project_external(self):
        """
        Try to create a project as an external user
        """
        self.sign_in(self.external)
        self.get_url('')

        if "Create Project Application" in self.selenium.page_source:
            raise AssertionError()

    def test_create_project_unauthorized(self):
        """
        Try to create a project without signing in
        """
        # Navigate to the new project form
        self.get_url(reverse('create-project-and-allocation'))

        # This should throw us to the login page
        if "accounts/login" not in self.selenium.current_url:
            raise AssertionError()

    def test_project_supervisor_authorisation(self):
        project = Project.objects.get(code="scw0001")
        project.approved_by_supervisor = False
        project.save()

        # Click the link in the email without signing in (using external, shibboleth used in email)
        self.get_url('/accounts/external/login/?next=/en/projects/applications/2/supervisor-approve/')

        # Sign in at the login page
        form_fields = {
            "id_username": self.user.email,
            "id_password": self.user_password,
        }
        self.fill_form_by_id(form_fields)
        self.submit_form(form_fields)

        self.click_button()

        project.refresh_from_db()

        if not project.approved_by_supervisor:
            raise AssertionError()
