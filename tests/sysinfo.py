#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the system information collector."""

import unittest

from dfwinreg import definitions as dfwinreg_definitions
from dfwinreg import fake as dfwinreg_fake
from dfwinreg import registry as dfwinreg_registry

from winregrc import sysinfo

from tests import test_lib


class SystemInfoCollectorTest(test_lib.BaseTestCase):
  """Tests for the system information collector."""

  # pylint: disable=protected-access

  _CSD_VERSION = 'Service Pack 1'
  _CURRENT_BUILD_NUMBER = '7601'
  _CURRENT_TYPE = 'Multiprocessor Free'
  _CURRENT_VERSION = '6.1'
  _INSTALLATION_DATE = 1289406535
  _PATH_NAME = 'C:\\Windows'
  _PRODUCT_IDENTIFIER = '00426-067-1817155-86250'
  _PRODUCT_NAME = 'Windows 7 Ultimate'
  _REGISTERED_ORGANIZATION = ''
  _REGISTERED_OWNER = 'Windows User'
  _SYSTEM_ROOT = 'C:\\Windows'

  def _CreateTestRegistry(self):
    """Creates Registry keys and values for testing.

    Returns:
      dfwinreg.WinRegistry: Windows Registry for testing.
    """
    key_path_prefix = 'HKEY_LOCAL_MACHINE\\Software'

    registry_file = dfwinreg_fake.FakeWinRegistryFile(
        key_path_prefix=key_path_prefix)

    registry_key = dfwinreg_fake.FakeWinRegistryKey('CurrentVersion')
    registry_file.AddKeyByPath('\\Microsoft\\Windows NT', registry_key)

    value_data = self._CSD_VERSION.encode('utf-16-le')
    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'CSDVersion', data=value_data, data_type=dfwinreg_definitions.REG_SZ)
    registry_key.AddValue(registry_value)

    value_data = self._CURRENT_BUILD_NUMBER.encode('utf-16-le')
    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'CurrentBuildNumber', data=value_data,
        data_type=dfwinreg_definitions.REG_SZ)
    registry_key.AddValue(registry_value)

    value_data = self._CURRENT_TYPE.encode('utf-16-le')
    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'CurrentType', data=value_data,
        data_type=dfwinreg_definitions.REG_SZ)
    registry_key.AddValue(registry_value)

    value_data = self._CURRENT_VERSION.encode('utf-16-le')
    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'CurrentVersion', data=value_data,
        data_type=dfwinreg_definitions.REG_SZ)
    registry_key.AddValue(registry_value)

    value_data = b'\x47\xc8\xda\x4c'
    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'InstallDate', data=value_data,
        data_type=dfwinreg_definitions.REG_DWORD)
    registry_key.AddValue(registry_value)

    value_data = self._PRODUCT_IDENTIFIER.encode('utf-16-le')
    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'ProductId', data=value_data, data_type=dfwinreg_definitions.REG_SZ)
    registry_key.AddValue(registry_value)

    value_data = self._PRODUCT_NAME.encode('utf-16-le')
    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'ProductName', data=value_data, data_type=dfwinreg_definitions.REG_SZ)
    registry_key.AddValue(registry_value)

    # TODO: add more values.

    registry_file.Open(None)

    registry = dfwinreg_registry.WinRegistry()
    registry.MapFile(key_path_prefix, registry_file)
    return registry

  def testParseInstallDate(self):
    """Tests the _ParseInstallDate function."""
    collector_object = sysinfo.SystemInfoCollector()

    date_time = collector_object._ParseInstallDate(None)
    self.assertIsNone(date_time)

    value_data = b'\x47\xc8\xda\x4c'
    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'InstallDate', data=value_data,
        data_type=dfwinreg_definitions.REG_DWORD)

    date_time = collector_object._ParseInstallDate(registry_value)
    self.assertIsNotNone(date_time)

    value_data = b'\x00\x00\x00\x00'
    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'InstallDate', data=value_data,
        data_type=dfwinreg_definitions.REG_DWORD)

    date_time = collector_object._ParseInstallDate(registry_value)
    self.assertIsNotNone(date_time)

  def testCollect(self):
    """Tests the Collect function."""
    registry = self._CreateTestRegistry()

    test_output_writer = test_lib.TestOutputWriter()
    collector_object = sysinfo.SystemInfoCollector(
        output_writer=test_output_writer)

    result = collector_object.Collect(registry)
    self.assertTrue(result)

    test_output_writer.Close()

    self.assertIsNotNone(collector_object.system_information)

    self.assertEqual(
        collector_object.system_information.csd_version, self._CSD_VERSION)
    self.assertEqual(
        collector_object.system_information.current_build_number,
        self._CURRENT_BUILD_NUMBER)
    self.assertEqual(
        collector_object.system_information.current_type, self._CURRENT_TYPE)
    self.assertEqual(
        collector_object.system_information.current_version,
        self._CURRENT_VERSION)
    self.assertIsNotNone(collector_object.system_information.installation_date)
    self.assertEqual(
        collector_object.system_information.product_identifier,
        self._PRODUCT_IDENTIFIER)
    self.assertEqual(
        collector_object.system_information.product_name, self._PRODUCT_NAME)

    # TODO: add more values.

  def testCollectEmpty(self):
    """Tests the Collect function on an empty Registry."""
    registry = dfwinreg_registry.WinRegistry()

    test_output_writer = test_lib.TestOutputWriter()
    collector_object = sysinfo.SystemInfoCollector(
        output_writer=test_output_writer)

    result = collector_object.Collect(registry)
    self.assertFalse(result)

    test_output_writer.Close()

    self.assertIsNone(collector_object.system_information)


if __name__ == '__main__':
  unittest.main()
