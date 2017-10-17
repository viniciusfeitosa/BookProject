# -*- coding: utf-8 -*-
import json
import unittest

from app import app
from models import News

from flask_testing import TestCase


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'] is True)


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])


class TestNewsService(BaseTestCase):
    def setUp(self):
        for i in range(20):
            News(
                title='Title test-{}'.format(i),
                content='Content test-{}'.format(i),
                author='Author test-{}'.format(i),
                tags=[
                    'one-{}'.format(i),
                    'two-{}'.format(i),
                ],
            ).save()

    def tearDown(self):
        News.objects().delete()

    def test_add_news(self):
        """Test to insert a News to the database."""
        with self.client:
            response = self.client.post(
                '/famous/news',
                data=json.dumps(dict(
                    title='My Test',
                    content='Just a service test',
                    author='unittest',
                    tags=['Test', 'Functional_test'],
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('My Test', data['news']['title'])

    def test_get_all_news(self):
        """Test to get all News paginated from the database."""
        with self.client:
            test_cases = [
                {'page': 1, 'num_per_page': 10, 'loop_couter': 0},
                {'page': 2, 'num_per_page': 10, 'loop_couter': 10},
                {'page': 1, 'num_per_page': 20, 'loop_couter': 0},
            ]
            for tc in test_cases:
                response = self.client.get(
                    '/famous/news/{}/{}'.format(
                        tc['page'], tc['num_per_page'])
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 200)
                self.assertIn('success', data['status'])
                self.assertEqual(len(data['data']), tc['num_per_page'])
                for d in data['data']:
                    self.assertEqual(
                        d['title'],
                        'Title test-{}'.format(tc['loop_couter'])
                    )
                    self.assertEqual(
                        d['content'],
                        'Content test-{}'.format(tc['loop_couter'])
                    )
                    self.assertEqual(
                        d['author'],
                        'Author test-{}'.format(tc['loop_couter'])
                    )
                    tc['loop_couter'] += 1


if __name__ == '__main__':
    unittest.main()
