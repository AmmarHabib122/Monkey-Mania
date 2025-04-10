# from rest_framework import status
# from django.urls import reverse
# from django.utils.http import urlencode

# from base import models
# from .SetUpSubscriptionInstanceTests import SetUpDataClass





# class TestSubscriptionInstanceListRetrieve(SetUpDataClass):
#     def test_subscription_instance_with_no_branch_get_all_subscription_instances(self):
#         url = reverse('Create_SubscriptionInstance')
#         resverse_url = reverse('List_SubscriptionInstance') 
#         self.authenticate(self.admin_user_1)
#         self.client.post(url, self.test_child_1, format = 'json')
#         self.client.post(url, self.test_child_2, format = 'json')
#         self.client.post(url, self.test_child_3, format = 'json')


        

                              
#         query_params = {                           #admin get all SubscriptionInstanceren with name contain child1
#             'search': 'child1',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)

#         query_params = {                           #admin get all SubscriptionInstanceren with phone starts with 1234
#             'search': '1234',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)

#         query_params = {                           #admin get all SubscriptionInstanceren with phone = 12335678912
#             'search': '12335678912',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#         self.assertEqual(response.data[0]['name'], 'testchild2')


#         query_params = {                            #admin get all SubscriptionInstanceren
#             'search': '',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 5)


        

#     def test_subscription_instance_with_a_branch_get_child(self):
#         self.authenticate(self.reception_user_1)

#         resverse_url = reverse('List_SubscriptionInstance')       #recepiton get all SubscriptionInstanceren
#         query_params = {
#             'search': '',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)




#     def test_subscription_instance_with_no_permission_get_child(self):
#         self.authenticate(self.waiter_user_1)

#         resverse_url = reverse('List_SubscriptionInstance')       #waiter get all SubscriptionInstanceren
#         query_params = {
#             'search': '',  
#         }
#         query_string = urlencode(query_params, doseq=True)
#         url = f"{resverse_url}?{query_string}"
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        

    

