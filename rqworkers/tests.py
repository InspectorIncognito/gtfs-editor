import json
import os
from unittest import mock

from django.core.files.base import ContentFile

from rest_api.models import GTFSValidation, Project
from rest_api.tests.test_helpers import BaseTestCase
from rqworkers.jobs import validate_gtfs, create_gtfs_file


class TestValidateGTFS(BaseTestCase):

    def setUp(self):
        self.project_obj = self.create_data()[0]
        GTFSValidation.objects.create(project=self.project_obj, status=GTFSValidation.STATUS_QUEUED)

    def test_project_does_not_have_gtfs_file(self):
        validate_gtfs(self.project_obj.pk)

        self.project_obj.refresh_from_db()
        self.assertEqual(self.project_obj.gtfsvalidation.status, GTFSValidation.STATUS_ERROR)
        self.assertEqual(self.project_obj.gtfsvalidation.message, 'GTFS file does not exist')
        self.assertIsNotNone(self.project_obj.gtfsvalidation.duration)

    @mock.patch('rqworkers.jobs.subprocess')
    @mock.patch('rqworkers.jobs.glob')
    @mock.patch('rqworkers.jobs.open', mock.mock_open(
        read_data=json.dumps({"results": [
            {},
            {"filename": "a.txt", "code": "1", "level": "WARNING",
             "entityId": "no id", "title": "problem", "description": "there is a problem"},
            {"filename": "b.txt", "code": "2", "level": "ERROR",
             "entityId": "no id", "title": "problem", "description": "there is a problem"},
        ]})))
    def test_execution(self, mock_glob, mock_subprocess):
        self.project_obj.gtfs_file.save(self.project_obj.name, ContentFile('fake zip file'))

        mock_glob.glob.return_value = ['fake_filepath']

        validate_gtfs(self.project_obj.pk)

        mock_subprocess.call.assert_called_once()
        self.project_obj.refresh_from_db()
        self.assertEqual(self.project_obj.gtfsvalidation.status, GTFSValidation.STATUS_FINISHED)
        expected_message = 'filename,code,level,entity id,title,description' + os.linesep + \
                           'a.txt,1,WARNING,no id,problem,there is a problem' + os.linesep + \
                           'b.txt,2,ERROR,no id,problem,there is a problem' + os.linesep
        self.assertEqual(self.project_obj.gtfsvalidation.message, expected_message)

        # delete test files
        os.remove(self.project_obj.gtfs_file.path)
        parent_path = os.path.sep.join(self.project_obj.gtfs_file.path.split(os.path.sep)[:-1])
        if len(os.listdir(parent_path)) == 0:
            os.rmdir(parent_path)

    def test_project_does_not_exist(self):
        with self.assertRaises(Project.DoesNotExist):
            validate_gtfs(1000)


class TestCreateGTFSFile(BaseTestCase):

    def setUp(self):
        self.project_obj = self.create_data()[0]

    @mock.patch('rqworkers.jobs.call_command')
    def test_execution(self, mock_call_command):
        create_gtfs_file(self.project_obj.pk)

        self.project_obj.refresh_from_db()
        self.assertEqual(self.project_obj.gtfs_creation_status, Project.GTFS_CREATION_STATUS_FINISHED)
        mock_call_command.assert_called_with('buildgtfs', self.project_obj.name)

    @mock.patch('rqworkers.jobs.call_command')
    def test_execution_raise_error(self, mock_call_command):
        mock_call_command.side_effect = ValueError('error calling call_command')
        create_gtfs_file(self.project_obj.pk)

        self.project_obj.refresh_from_db()
        self.assertEqual(self.project_obj.gtfs_creation_status, Project.GTFS_CREATION_STATUS_ERROR)
        mock_call_command.assert_called_with('buildgtfs', self.project_obj.name)

    def test_project_name_does_not_exist(self):
        with self.assertRaises(ValueError):
            create_gtfs_file('wrong_project_pk')

        with self.assertRaises(Project.DoesNotExist):
            create_gtfs_file(-1)
