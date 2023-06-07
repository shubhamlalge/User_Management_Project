
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework.utils import json
from rest_framework import status

from user.models import User


class UserTestCases(APITestCase):

    '''This class is used for write api test case'''

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            first_name='first',
            last_name='last',
            username='testuser',
            email='testuser@gmail.com',
            password='testpassword',
            phone_Number='243245251',
            date_of_birth='2001-04-24',
            street='karve nagar',
            zip_code=411052,
            city='pune',
            state='maharastra',
            country='India'
        )
        self.data1 = {
            'first_name': 'second',
            'last_name': 'lastperson',

            'username': 'shiv',
            'email': 'shiv@gmail.com',
            'password': 'password',

            'phone_Number': '29845251',
            'date_of_birth': '2001-04-24',
            'street': 'karve nagar',
            'zip_code': 411052,
            'city': 'pune',
            'state': 'maharastra',
            'country': 'India',

        }

    def test_create_user_pass(self):
        '''This function is used for create test case passed'''
        response = self.client.post((reverse('user_post')), self.data1, format='json')
        self.assertEqual(response.status_code, 201)

    def test_create_user_fail(self):
        ''' This function is used for create test case failed'''

        self.data2 = {

            'date_of_birth': '21-03-2412',
            'street': ' nagar2',
            'zip_code': '41132'

        }
        response = self.client.post(reverse('user_post'), self.data2, format='json')
        self.assertEqual(response.status_code, 400)

    def test_delete_user_succes(self):
        ''' This function is used for delete test case which is  passed'''
        self.client.login(username='testuser', email='testuser@gmail.com', password='testpassword')
        response = self.client.delete(reverse('user_delete', kwargs={'pk': self.user.id}), format='json')
        self.assertEqual(response.status_code, 204)

    def test_delete_user_fail(self):
        ''' This function is used for delete test case which is fail purpose'''
        self.client.login(username='testuser', email='testuser@gmail.com', password='testpassword')
        response = self.client.delete(reverse('user_delete', kwargs={'pk': 43}), format='json')
        self.assertEqual(response.status_code, 404)

    def test_retrive_user_succes(self):
        '''This function is used for retrive test case success'''
        self.client.login(username='testuser', email='testuser@gmail.com', password='testpassword')
        response = self.client.get(reverse('user_list_id', kwargs={'pk': self.user.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_update_user_fail(self):
        ''' This function is used for update test case fail purpose'''
        self.data2 = {

            'date_of_birth': '21-03-2412',
            'street': ' nagar2',
            'zip_code': '41132'

        }
        self.client.login(username='testuser', email='testuser@gmail.com', password='testpassword')
        response = self.client.patch(reverse('user_update_id', kwargs={'pk': 44}), self.data2 ,format ='json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.user.email, 'testuser@gmail.com')

    def test_update_user_pass(self):
        '''This function is used for update test case which is passed'''
        self.data2 = {

            'first_name': 'second',
            'last_name': 'lastperson',

            'username': 'shiv',
            'email': 'shiv@gmail.com',
            'password': 'password',

            'phone_Number': '29845251',
            'date_of_birth': '2001-04-24',
            'street': 'karve nagar',
            'zip_code': 411052,
            'city': 'pune',
            'state': 'maharastra',
            'country': 'India',

        }
        self.client.login(username='testuser',  password='testpassword')
        response = self.client.patch(reverse('user_update_id', kwargs={'pk': self.user.id}), self.data2 , format= 'json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.email, 'testuser@gmail.com')
