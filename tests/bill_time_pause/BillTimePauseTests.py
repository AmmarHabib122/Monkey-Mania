from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from base import models


class TestBillTimePause(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = models.User.objects.create(
            username='pause-manager',
            phone_number='01000000000',
            role='manager',
        )
        cls.branch = models.Branch.objects.create(
            name='Pause Test Branch',
            address='Test address',
            allowed_age=5,
            created_by=cls.user,
            delay_allowed_time=60,
            delay_fine_interval=30,
            delay_fine_value=Decimal('0.50'),
        )
        cls.user.branch = cls.branch
        cls.user.save(update_fields=['branch', 'updated'])

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.bill = models.Bill.objects.create(
            branch=self.branch,
            created_by=self.user,
            hour_price=Decimal('70.00'),
            half_hour_price=Decimal('40.00'),
        )

    def create_pause(self, reason='Lunch break'):
        return self.client.post(
            reverse('Create_Bill_Time_Pause'),
            {'bill': self.bill.pk, 'reason': reason},
            format='json',
        )

    def test_create_pause_and_prevent_duplicate_active_pause(self):
        response = self.create_pause()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pause = models.BillTimePause.objects.get()
        self.assertEqual(pause.created_by, self.user)
        self.assertIsNone(pause.finished)
        self.assertIsNone(pause.finished_by)
        self.assertTrue(pause.is_active)

        duplicate = self.create_pause('Another reason')
        self.assertEqual(duplicate.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.BillTimePause.objects.count(), 1)

    def test_empty_reason_is_rejected(self):
        response = self.create_pause('   ')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_pause_for_closed_bill_is_rejected(self):
        models.Bill.objects.filter(pk=self.bill.pk).update(
            is_active=False,
            finished=timezone.now(),
            finished_by=self.user,
        )

        response = self.create_pause()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data['message'],
            "You cannot add a time pause to a closed bill",
        )
        self.assertFalse(models.BillTimePause.objects.exists())

    def test_close_pause_and_reject_second_close(self):
        pause_id = self.create_pause().data['id']
        url = reverse('Close_Bill_Time_Pause', kwargs={'pk': pause_id})

        response = self.client.patch(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_active'])

        pause = models.BillTimePause.objects.get(pk=pause_id)
        self.assertEqual(pause.finished_by, self.user)
        self.assertIsNotNone(pause.finished)

        duplicate = self.client.patch(url, {}, format='json')
        self.assertEqual(duplicate.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fetch_pause_by_id_includes_computed_fields(self):
        pause_id = self.create_pause().data['id']
        response = self.client.get(
            reverse('Get_Bill_Time_Pause', kwargs={'pk': pause_id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bill'], self.bill.pk)
        self.assertTrue(response.data['is_active'])
        self.assertIn('duration_in_seconds', response.data)
        self.assertEqual(response.data['created_by'], self.user.username)

    def test_get_bill_includes_pauses(self):
        pause_id = self.create_pause().data['id']
        response = self.client.get(
            reverse('Get_Bill', kwargs={'pk': self.bill.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['pauses']), 1)
        self.assertEqual(response.data['pauses'][0]['id'], pause_id)
        self.assertEqual(response.data['pauses'][0]['bill'], self.bill.pk)

    def test_bill_close_rejects_active_pause(self):
        now = timezone.now()
        models.Bill.objects.filter(pk=self.bill.pk).update(
            created=now - timedelta(hours=2, seconds=5)
        )
        pause = models.BillTimePause.objects.create(
            bill=self.bill,
            reason='One hour pause',
            created_by=self.user,
        )
        models.BillTimePause.objects.filter(pk=pause.pk).update(
            created=now - timedelta(hours=1)
        )

        response = self.client.patch(
            reverse('Close_Bill', kwargs={'pk': self.bill.pk}),
            {'visa': '70.00'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.bill.refresh_from_db()
        pause.refresh_from_db()
        self.assertTrue(self.bill.is_active)
        self.assertTrue(pause.is_active)
        self.assertIsNone(pause.finished_by)

        close_pause_response = self.client.patch(
            reverse('Close_Bill_Time_Pause', kwargs={'pk': pause.pk}),
            {},
            format='json',
        )
        self.assertEqual(close_pause_response.status_code, status.HTTP_200_OK)

        response = self.client.patch(
            reverse('Close_Bill', kwargs={'pk': self.bill.pk}),
            {'visa': '70.00'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.bill.refresh_from_db()
        self.assertFalse(self.bill.is_active)
        self.assertEqual(self.bill.spent_time, 60)
        self.assertEqual(self.bill.time_price, Decimal('70.00'))
