from django.test import TestCase
from django.db.models import Value, CharField, Count, When, Case

from .models import Person, QuantitativeAttribute


class QuantitativeTestCase(TestCase):
    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        cls.p1 = Person.objects.create(name='p1')

        QuantitativeAttribute.objects.create(
            person=cls.p1,
            value=27,
            name='age',
        )

    def test_annotate_fail(self):
        """This test is successfull with sqlite"""
        expected_qs = [{'alarm': 'warning', 'number': 1, 'pk': 1}]

        qs = Person.objects \
            .all() \
            .annotate(number=Count('quantitativeattribute'))

        qs = qs.annotate(alarm=Case(
            When(id__in=[], then=Value('danger', output_field=CharField())),
            default=Value('warning')

        ))

        # print(qs.query)
        self.assertQuerysetEqual(qs.values('pk', 'number', 'alarm'), expected_qs)
        # => raises django.db.utils.ProgrammingError: non-integer constant in GROUP BY
        # LINE 1: ...ibute"."person_id") GROUP BY "argent_person"."id", 'warning'

    def test_annotate_success(self):
        """This test is successfull with sqlite and postgres"""
        expected_qs = [{'alarm': 'warning', 'number': 1, 'pk': 1}]

        qs = Person.objects\
            .all()\
            .annotate(number=Count('quantitativeattribute'))

        qs = qs.annotate(alarm=Case(
            # When(id__in=[], then=Value('danger', output_field=models.CharField())),
            default=Value('warning')

        ))

        self.assertQuerysetEqual(qs.values('pk', 'number', 'alarm'), expected_qs)
