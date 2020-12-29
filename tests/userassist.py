#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the Windows User Assist collector."""

import unittest

from dfwinreg import definitions as dfwinreg_definitions
from dfwinreg import fake as dfwinreg_fake
from dfwinreg import registry as dfwinreg_registry

from winregrc import userassist

from tests import test_lib


_ENTRY_DATA_V3 = bytes(bytearray([
    0x01, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0xb0, 0xe3, 0x6e, 0x4b,
    0x17, 0x15, 0xca, 0x01]))

_ENTRY_DATA_V5 = bytes(bytearray([
    0x00, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00,
    0x20, 0x30, 0x05, 0x00, 0x00, 0x00, 0x80, 0xbf, 0x00, 0x00, 0x80, 0xbf,
    0x00, 0x00, 0x80, 0xbf, 0x00, 0x00, 0x80, 0xbf, 0x00, 0x00, 0x80, 0xbf,
    0x00, 0x00, 0x80, 0xbf, 0x00, 0x00, 0x80, 0xbf, 0x00, 0x00, 0x80, 0xbf,
    0x00, 0x00, 0x80, 0xbf, 0x00, 0x00, 0x80, 0xbf, 0xff, 0xff, 0xff, 0xff,
    0x04, 0xa8, 0x92, 0xd2, 0xab, 0x80, 0xcb, 0x01, 0x00, 0x00, 0x00, 0x00]))


class UserAssistDataParserTest(test_lib.BaseTestCase):
  """Tests for the User Assist data parser."""

  def testParseEntry(self):
    """Tests the ParseEntry function."""
    data_parser = userassist.UserAssistDataParser()

    data_parser.ParseEntry(3, _ENTRY_DATA_V3)

    data_parser.ParseEntry(5, _ENTRY_DATA_V5)


class UserAssistCollectorTest(test_lib.BaseTestCase):
  """Tests for the Windows User Assist collector."""

  _GUID = '{5E6AB780-7743-11CF-A12B-00AA004AE837}'

  _UEME_CTLSESSION_VALUE_DATA = bytes(bytearray([
      0xb0, 0xa8, 0x50, 0x0e, 0x01, 0x00, 0x00, 0x00]))

  _ENTRY_VALUE_DATA = bytes(bytearray([
      0x01, 0x00, 0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x54, 0x4b, 0xf6, 0xd3,
      0x15, 0x15, 0xca, 0x01]))

  def _CreateTestRegistry(self):
    """Creates Registry keys and values for testing.

    Returns:
      dfwinreg.WinRegistry: Windows Registry for testing.
    """
    key_path_prefix = 'HKEY_CURRENT_USER'

    registry_file = dfwinreg_fake.FakeWinRegistryFile(
        key_path_prefix=key_path_prefix)

    registry_key = dfwinreg_fake.FakeWinRegistryKey(self._GUID)
    registry_file.AddKeyByPath(
        '\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\UserAssist',
        registry_key)

    value_data = b'\x03\x00\x00\x00'
    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'Version', data=value_data, data_type=dfwinreg_definitions.REG_DWORD)
    registry_key.AddValue(registry_value)

    subkey = dfwinreg_fake.FakeWinRegistryKey('Count')
    registry_key.AddSubkey('Count', subkey)

    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'HRZR_PGYFRFFVBA', data=self._UEME_CTLSESSION_VALUE_DATA,
        data_type=dfwinreg_definitions.REG_BINARY)
    subkey.AddValue(registry_value)

    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'HRZR_EHACVQY:%pfvqy2%\\Jvaqbjf Zrffratre.yax',
        data=self._ENTRY_VALUE_DATA, data_type=dfwinreg_definitions.REG_BINARY)
    subkey.AddValue(registry_value)

    registry_file.Open(None)

    registry = dfwinreg_registry.WinRegistry()
    registry.MapFile(key_path_prefix, registry_file)
    return registry

  def testCollect(self):
    """Tests the Collect function."""
    registry = self._CreateTestRegistry()

    test_output_writer = test_lib.TestOutputWriter()
    collector_object = userassist.UserAssistCollector(
        output_writer=test_output_writer)

    result = collector_object.Collect(registry)
    self.assertTrue(result)

    test_output_writer.Close()

    self.assertEqual(len(collector_object.user_assist_entries), 1)

    # TODO: test user assist entry values.

  def testCollectEmpty(self):
    """Tests the Collect function on an empty Registry."""
    registry = dfwinreg_registry.WinRegistry()

    test_output_writer = test_lib.TestOutputWriter()
    collector_object = userassist.UserAssistCollector(
        output_writer=test_output_writer)

    result = collector_object.Collect(registry)
    self.assertFalse(result)

    test_output_writer.Close()

    self.assertEqual(len(collector_object.user_assist_entries), 0)


if __name__ == '__main__':
  unittest.main()
