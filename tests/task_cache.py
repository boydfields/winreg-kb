#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the Task Cache information collector."""

import unittest

from dfwinreg import definitions as dfwinreg_definitions
from dfwinreg import fake as dfwinreg_fake
from dfwinreg import registry as dfwinreg_registry

from winregrc import task_cache

from tests import test_lib


_DYNAMIC_INFO_DATA = bytes(bytearray([
    0x03, 0x00, 0x00, 0x00, 0x0c, 0x1c, 0x7d, 0x12, 0x3f, 0x04, 0xca, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00]))

_DYNAMIC_INFO2_DATA = bytes(bytearray([
    0x03, 0x00, 0x00, 0x00, 0x0c, 0x1c, 0x7d, 0x12, 0x3f, 0x04, 0xca, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x0c, 0x1c, 0x7d, 0x12, 0x3f, 0x04, 0xca, 0x01]))


class TaskCacheDataParserTest(test_lib.BaseTestCase):
  """Tests for the Task Cache data parser."""

  def testParseDynamicInfo(self):
    """Tests the ParseDynamicInfo function."""
    data_parser = task_cache.TaskCacheDataParser()

    cached_task = task_cache.CachedTask()
    data_parser.ParseDynamicInfo(_DYNAMIC_INFO_DATA, cached_task)

    # TODO: compare date time value.
    self.assertIsNotNone(cached_task.last_registered_time)
    # TODO: compare date time value.
    self.assertIsNotNone(cached_task.launch_time)

    cached_task = task_cache.CachedTask()
    data_parser.ParseDynamicInfo(_DYNAMIC_INFO2_DATA, cached_task)

    # TODO: compare date time value.
    self.assertIsNotNone(cached_task.last_registered_time)
    # TODO: compare date time value.
    self.assertIsNotNone(cached_task.launch_time)


class TaskCacheCollectorTest(test_lib.BaseTestCase):
  """Tests for the Task Cache information collector."""

  _GUID1 = '{8905ECD8-016F-4DC2-90E6-A5F1FA6A841A}'
  _GUID2 = '{F93C7104-998A-4A38-B935-775A3138B3C3}'
  _GUID3 = '{FE7B674F-2430-40A1-9162-AFC3727E3DC3}'

  _NAME1 = 'AD RMS Rights Policy Template Management (Automated)'
  _NAME2 = 'Notifications'
  _NAME3 = 'AutoWake'

  _PATH = (
      '\\Microsoft\\Windows\\Active Directory Rights Management Services '
      'Client\\AD RMS Rights Policy Template Management (Automated)')

  def _CreateTestRegistry(self):
    """Creates Registry keys and values for testing.

    Returns:
      dfwinreg.WinRegistry: Windows Registry for testing.
    """
    key_path_prefix = 'HKEY_LOCAL_MACHINE\\Software'

    registry_file = dfwinreg_fake.FakeWinRegistryFile(
        key_path_prefix=key_path_prefix)

    registry_key = dfwinreg_fake.FakeWinRegistryKey(self._GUID1)
    registry_file.AddKeyByPath(
        '\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\TaskCache\\Tasks',
        registry_key)

    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'DynamicInfo', data=_DYNAMIC_INFO_DATA,
        data_type=dfwinreg_definitions.REG_BINARY)
    registry_key.AddValue(registry_value)

    value_data = self._PATH.encode('utf-16-le')
    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'Path', data=value_data, data_type=dfwinreg_definitions.REG_SZ)
    registry_key.AddValue(registry_value)

    registry_key = dfwinreg_fake.FakeWinRegistryKey(self._NAME1)
    registry_file.AddKeyByPath((
        '\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\TaskCache\\Tree\\'
        'Microsoft\\Windows\\Active Directory Rights Management Services '
        'Client'), registry_key)

    value_data = '{8905ECD8-016F-4DC2-90E6-A5F1FA6A841A}\x00'.encode(
        'utf-16-le')
    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'Id', data=value_data, data_type=dfwinreg_definitions.REG_SZ)
    registry_key.AddValue(registry_value)

    registry_key = dfwinreg_fake.FakeWinRegistryKey(self._GUID2)
    registry_file.AddKeyByPath(
        '\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\TaskCache\\Tasks',
        registry_key)

    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'DynamicInfo', data=_DYNAMIC_INFO2_DATA,
        data_type=dfwinreg_definitions.REG_BINARY)
    registry_key.AddValue(registry_value)

    registry_key = dfwinreg_fake.FakeWinRegistryKey(self._NAME2)
    registry_file.AddKeyByPath((
        '\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\TaskCache\\Tree\\'
        'Microsoft\\Windows\\Location'), registry_key)

    value_data = '{F93C7104-998A-4A38-B935-775A3138B3C3}\x00'.encode(
        'utf-16-le')
    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'Id', data=value_data, data_type=dfwinreg_definitions.REG_SZ)
    registry_key.AddValue(registry_value)

    registry_key = dfwinreg_fake.FakeWinRegistryKey(self._GUID3)
    registry_file.AddKeyByPath(
        '\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\TaskCache\\Tasks',
        registry_key)

    registry_key = dfwinreg_fake.FakeWinRegistryKey(self._NAME3)
    registry_file.AddKeyByPath((
        '\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\TaskCache\\Tree\\'
        'Microsoft\\Windows\\SideShow'), registry_key)

    value_data = '{FE7B674F-2430-40A1-9162-AFC3727E3DC3}\x00'.encode(
        'utf-16-le')
    registry_value = dfwinreg_fake.FakeWinRegistryValue(
        'Id', data=value_data, data_type=dfwinreg_definitions.REG_SZ)
    registry_key.AddValue(registry_value)

    registry_file.Open(None)

    registry = dfwinreg_registry.WinRegistry()
    registry.MapFile(key_path_prefix, registry_file)
    return registry

  def _CreateTestRegistryEmpty(self):
    """Creates Registry keys and values for testing.

    Returns:
      dfwinreg.WinRegistry: Windows Registry for testing.
    """
    key_path_prefix = 'HKEY_LOCAL_MACHINE\\Software'

    registry_file = dfwinreg_fake.FakeWinRegistryFile(
        key_path_prefix=key_path_prefix)

    registry_key = dfwinreg_fake.FakeWinRegistryKey('Tasks')
    registry_file.AddKeyByPath(
        '\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\TaskCache',
        registry_key)

    registry_file.Open(None)

    registry = dfwinreg_registry.WinRegistry()
    registry.MapFile(key_path_prefix, registry_file)
    return registry

  def testCollect(self):
    """Tests the Collect function."""
    registry = self._CreateTestRegistry()

    test_output_writer = test_lib.TestOutputWriter()
    collector_object = task_cache.TaskCacheCollector(
        output_writer=test_output_writer)

    result = collector_object.Collect(registry)
    self.assertTrue(result)

    test_output_writer.Close()

    self.assertEqual(len(collector_object.cached_tasks), 2)

    cached_tasks = sorted(
        collector_object.cached_tasks, key=lambda task: task.identifier)

    cached_task = cached_tasks[0]

    self.assertIsNotNone(cached_task)
    self.assertEqual(cached_task.identifier, self._GUID1)
    # TODO: fix test
    # self.assertEqual(cached_task.name, self._NAME1)

    cached_task = cached_tasks[1]

    self.assertIsNotNone(cached_task)
    self.assertEqual(cached_task.identifier, self._GUID2)
    # TODO: fix test
    # self.assertEqual(cached_task.name, self._NAME2)

  def testCollectEmpty(self):
    """Tests the Collect function on an empty Registry."""
    registry = dfwinreg_registry.WinRegistry()

    test_output_writer = test_lib.TestOutputWriter()
    collector_object = task_cache.TaskCacheCollector(
        output_writer=test_output_writer)

    result = collector_object.Collect(registry)
    self.assertFalse(result)

    test_output_writer.Close()

    self.assertEqual(len(collector_object.cached_tasks), 0)


if __name__ == '__main__':
  unittest.main()
