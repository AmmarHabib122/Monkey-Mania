from django.apps import apps
from django.core.management.color import no_style
from django.db import connection
from django.test import TestCase as DjangoTestCase


class TestCase(DjangoTestCase):
    """Keep legacy fixture IDs stable across PostgreSQL test cases."""

    @staticmethod
    def reset_base_sequences():
        if connection.vendor == 'postgresql':
            models = apps.get_app_config('base').get_models()
            statements = connection.ops.sequence_reset_sql(no_style(), models)
            with connection.cursor() as cursor:
                for statement in statements:
                    cursor.execute(statement)

    @classmethod
    def setUpClass(cls):
        cls.reset_base_sequences()
        super().setUpClass()

    def _pre_setup(self):
        super()._pre_setup()
        self.reset_base_sequences()
