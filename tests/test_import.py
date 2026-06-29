# -*- coding: utf-8 -*-
import os
import tempfile

from django.core.management import call_command
from django.test import TestCase

from django_postalcodes_mexico.models import PostalCode


FIXTURE_XML = """<?xml version="1.0" encoding="utf-8"?>
<NewDataSet xmlns="NewDataSet">
  <table>
    <d_codigo>06700</d_codigo>
    <d_asenta>Roma Norte</d_asenta>
    <D_mnpio>Cuauhtémoc</D_mnpio>
    <d_ciudad>Ciudad de México</d_ciudad>
    <d_CP>06700</d_CP>
    <c_estado>09</c_estado>
    <c_oficina>06700</c_oficina>
    <c_tipo_asenta>09</c_tipo_asenta>
    <c_mnpio>015</c_mnpio>
    <id_asenta_cpcons>0001</id_asenta_cpcons>
    <d_zona>Urbano</d_zona>
    <c_cve_ciudad>01</c_cve_ciudad>
  </table>
  <table>
    <d_codigo>06700</d_codigo>
    <d_asenta>Condesa</d_asenta>
    <D_mnpio>Cuauhtémoc</D_mnpio>
    <d_ciudad>Ciudad de México</d_ciudad>
    <d_CP>06700</d_CP>
    <c_estado>09</c_estado>
    <c_oficina>06700</c_oficina>
    <c_tipo_asenta>09</c_tipo_asenta>
    <c_mnpio>015</c_mnpio>
    <id_asenta_cpcons>0002</id_asenta_cpcons>
    <d_zona>Urbano</d_zona>
    <c_cve_ciudad>01</c_cve_ciudad>
  </table>
</NewDataSet>
"""


class ImportPostalCodesIdempotencyTest(TestCase):

    def _write_fixture(self):
        fd, path = tempfile.mkstemp(suffix=".xml")
        with os.fdopen(fd, "w", encoding="utf-8") as xml_file:
            xml_file.write(FIXTURE_XML)
        self.addCleanup(os.remove, path)
        return path

    def test_import_skips_when_already_loaded(self):
        path = self._write_fixture()

        call_command("importpostalcodesmx", file=path)
        self.assertEqual(PostalCode.objects.count(), 2)

        call_command("importpostalcodesmx", file=path)
        self.assertEqual(PostalCode.objects.count(), 2)

    def test_force_refreshes_without_duplicating(self):
        path = self._write_fixture()

        call_command("importpostalcodesmx", file=path)
        PostalCode.objects.filter(d_asenta="Condesa").delete()
        self.assertEqual(PostalCode.objects.count(), 1)

        call_command("importpostalcodesmx", file=path, force=True)
        self.assertEqual(PostalCode.objects.count(), 2)
