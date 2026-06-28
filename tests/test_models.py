#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-postalcodes-mexico
------------

Tests for `django-postalcodes-mexico` models module.
"""
import json

from django.test import TestCase
from django.urls import reverse

from django_postalcodes_mexico.models import PostalCode


class TestDjango_postalcodes_mexico(TestCase):

    def setUp(self):
        PostalCode.objects.get_or_create(
            d_codigo='01000',
            d_asenta='San Ángel',
            D_mnpio='Álvaro Obregón',
            d_ciudad='Ciudad de México',
            d_CP='01001',
            c_estado='09',
            c_oficina='01001',
            c_tipo_asenta='09',
            c_mnpio='010',
            id_asenta_cpcons='0001',
            d_zona='Urbano',
            c_cve_ciudad='01'
        )

    def test_api_returns_postal_code_data(self):
        retrieve_postal_code_data = reverse("django_postalcodes_mexico:get-postal-code-data", args=("01000",))
        response = self.client.get(retrieve_postal_code_data)
        self.assertEqual(response.status_code, 200)
        postal_code_data = json.loads(response.content)
        self.assertIsInstance(postal_code_data, dict)
        self.assertIn("colonias", postal_code_data)
        self.assertIn("municipio", postal_code_data)
        self.assertIn("estado", postal_code_data)
        self.assertIsInstance(postal_code_data.get('colonias'), list)

    def test_api_returns_404_on_not_found_postal_code(self):
        retrieve_postal_code_data = reverse("django_postalcodes_mexico:get-postal-code-data", args=("99999",))
        response = self.client.get(retrieve_postal_code_data)
        self.assertEqual(response.status_code, 404)
        postal_code_data = json.loads(response.content)
        self.assertEqual(len(postal_code_data), 0)

    def test_api_returns_400_on_alpha_input(self):
        retrieve_postal_code_data = reverse("django_postalcodes_mexico:get-postal-code-data", args=("ABCDE",))
        response = self.client.get(retrieve_postal_code_data)
        self.assertEqual(response.status_code, 400)
        postal_code_data = json.loads(response.content)
        self.assertNotIn("colonia", postal_code_data)
        self.assertIn("postal_code", postal_code_data)

    def test_api_returns_400_on_long_digit_input(self):
        retrieve_postal_code_data = reverse("django_postalcodes_mexico:get-postal-code-data", args=("999999999999",))
        response = self.client.get(retrieve_postal_code_data)
        self.assertEqual(response.status_code, 400)
        postal_code_data = json.loads(response.content)
        self.assertNotIn("colonia", postal_code_data)
        self.assertIn("postal_code", postal_code_data)

    def test_colonias_are_deduplicated_when_sepomex_has_multiple_segments_per_asenta(self):
        for i in range(5):
            PostalCode.objects.create(
                d_codigo='03103',
                d_asenta='Del Valle Norte',
                D_mnpio='Benito Juárez',
                d_ciudad='Ciudad de México',
                d_CP='03103',
                c_estado='09',
                c_oficina='03103',
                c_tipo_asenta='09',
                c_mnpio='014',
                id_asenta_cpcons=f'{i:04d}',
                d_zona='Urbano',
                c_cve_ciudad='01',
            )

        retrieve_postal_code_data = reverse(
            "django_postalcodes_mexico:get-postal-code-data", args=("03103",)
        )
        response = self.client.get(retrieve_postal_code_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['colonias'], ['Del Valle Norte'])

    def tearDown(self):
        pass
