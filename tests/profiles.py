#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the user profiles collector."""

from __future__ import unicode_literals

import unittest

from dfwinreg import definitions as dfwinreg_definitions
from dfwinreg import fake as dfwinreg_fake
from dfwinreg import registry as dfwinreg_registry

from winregrc import output_writers
from winregrc import profiles

from tests import test_lib as shared_test_lib


class TestOutputWriter(output_writers.StdoutOutputWriter):
  """Output writer for testing.

  Attributes:
    text (list[str]): text.
  """

  def __init__(self):
    """Initializes an output writer object."""
    super(TestOutputWriter, self).__init__()
    self.text = []

  def WriteText(self, text):
    """Writes text to stdout.

    Args:
      text (str): text to write.
    """
    self.text.append(text)


class UserProfilesCollectorTest(shared_test_lib.BaseTestCase):
  """Tests for the Windows user profiles collector."""

  _SID = 'S-1-5-18'
  _PROFILE_PATH = '%systemroot%\\system32\\config\\systemprofile'

  def _CreateTestRegistry(self):
    """Creates Registry keys and values for testing.

    Returns:
      dfwinreg.WinRegistry: Windows Registry for testing.
    """
    key_path_prefix = 'HKEY_LOCAL_MACHINE\\Software'

    registry_file = dfwinreg_fake.FakeWinRegistryFile(
        key_path_prefix=key_path_prefix)

    registry_key = dfwinreg_fake.FakeWinRegistryKey('ProfileList')
    registry_file.AddKeyByPath(
        '\\Microsoft\\Windows NT\\CurrentVersion', registry_key)

    subkey = dfwinreg_fake.FakeWinRegistryKey(self._SID)
    registry_key.AddSubkey(self._SID, subkey)

    value_data = self._PROFILE_PATH.encode('utf-16-le')
    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'ProfileImagePath', data=value_data,
        data_type=dfwinreg_definitions.REG_SZ)
    subkey.AddValue(registry_value)

    registry_file.Open(None)

    registry = dfwinreg_registry.WinRegistry()
    registry.MapFile(key_path_prefix, registry_file)
    return registry

  def testCollect(self):
    """Tests the Collect function."""
    registry = self._CreateTestRegistry()

    collector_object = profiles.UserProfilesCollector()

    test_output_writer = TestOutputWriter()
    collector_object.Collect(registry, test_output_writer)
    test_output_writer.Close()

    # TODO: return user profile objects.
    self.assertEqual(len(test_output_writer.text), 1)

  def testCollectEmpty(self):
    """Tests the Collect function on an empty Registry."""
    registry = dfwinreg_registry.WinRegistry()

    collector_object = profiles.UserProfilesCollector()

    test_output_writer = TestOutputWriter()
    collector_object.Collect(registry, test_output_writer)
    test_output_writer.Close()

    self.assertEqual(len(test_output_writer.text), 0)


if __name__ == '__main__':
  unittest.main()
