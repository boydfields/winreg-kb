# -*- coding: utf-8 -*-
"""Task Cache collector."""

import logging

from dfdatetime import filetime as dfdatetime_filetime
from dfdatetime import semantic_time as dfdatetime_semantic_time

from dtfabric import errors as dtfabric_errors

from winregrc import data_format
from winregrc import errors
from winregrc import interface


class CachedTask(object):
  """Cached task.

  Attributes:
    identifier (str): identifier.
    last_registered_time (dfdatetime.DateTimeValues): last registered
        date and time.
    launch_time (dfdatetime.DateTimeValues): launch date and time.
    name (str): name.
  """

  def __init__(self):
    """Initializes a cached task."""
    super(CachedTask, self).__init__()
    self.identifier = None
    self.last_registered_time = None
    self.launch_time = None
    self.name = None


class TaskCacheDataParser(data_format.BinaryDataFormat):
  """Task Cache data parser."""

  _DEFINITION_FILE = 'task_cache.yaml'

  def __init__(self, debug=False, output_writer=None):
    """Initializes a Task Cache data parser.

    Args:
      debug (Optional[bool]): True if debug information should be printed.
      output_writer (Optional[OutputWriter]): output writer.
    """
    super(TaskCacheDataParser, self).__init__()
    self._debug = debug
    self._output_writer = output_writer

  def _ParseFiletime(self, filetime):
    """Parses a FILETIME timestamp value.

    Args:
      filetime (int): a FILETIME timestamp value.

    Returns:
      dfdatetime.DateTimeValues: date and time values.
    """
    if filetime == 0:
      return dfdatetime_semantic_time.SemanticTime(string='Not set')

    if filetime == 0x7fffffffffffffff:
      return dfdatetime_semantic_time.SemanticTime(string='Never')

    return dfdatetime_filetime.Filetime(timestamp=filetime)

  def ParseDynamicInfo(self, value_data, cached_task):
    """Parses the DynamicInfo value data.

    Args:
      value_data (bytes): DynamicInfo value data.
      cached_task (CachedTask): cached task.

    Raises:
      ParseError: if the value data could not be parsed.
    """
    if self._debug:
      self._output_writer.WriteDebugData('DynamicInfo value data:', value_data)

    value_data_size = len(value_data)

    if value_data_size == 28:
      data_type_map = self._GetDataTypeMap('dynamic_info_record')
    elif value_data_size == 36:
      data_type_map = self._GetDataTypeMap('dynamic_info2_record')

    if not data_type_map:
      raise errors.ParseError(
          f'Unsupported value data size: {value_data_size:d}.')

    try:
      dynamic_info = data_type_map.MapByteStream(value_data)
    except (
        dtfabric_errors.ByteStreamTooSmallError,
        dtfabric_errors.MappingError) as exception:
      raise errors.ParseError(exception)

    cached_task.last_registered_time = self._ParseFiletime(
        dynamic_info.last_registered_time)
    cached_task.launch_time = self._ParseFiletime(
        dynamic_info.launch_time)

    if self._debug:
      self._output_writer.WriteValue(
          'Unknown1', f'0x{dynamic_info.unknown1:08x}')

      # Note this is likely either the last registered time or
      # the update time.
      self._DebugPrintFiletimeValue(
          'Last registered time', dynamic_info.last_registered_time)

      # Note this is likely the launch time.
      self._DebugPrintFiletimeValue('Launch time', dynamic_info.launch_time)

      self._output_writer.WriteValue(
          'Unknown2', f'0x{dynamic_info.unknown2:08x}')

      self._output_writer.WriteValue(
          'Unknown3', f'0x{dynamic_info.unknown3:08x}')

      if dynamic_info.unknown_time is not None:
        self._DebugPrintFiletimeValue('Unknown time', dynamic_info.unknown_time)

      self._output_writer.WriteText('')


class TaskCacheCollector(interface.WindowsRegistryKeyCollector):
  """Task Cache collector.

  Attributes:
    cached_tasks (list[CachedTask]): cached tasks.
  """

  _TASK_CACHE_KEY_PATH = (
      'HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows NT\\CurrentVersion\\'
      'Schedule\\TaskCache')

  def __init__(self, debug=False, output_writer=None):
    """Initializes a Task Cache collector.

    Args:
      debug (Optional[bool]): True if debug information should be printed.
      output_writer (Optional[OutputWriter]): output writer.
    """
    super(TaskCacheCollector, self).__init__(debug=debug)
    self._parser = TaskCacheDataParser(debug=debug, output_writer=output_writer)
    self._output_writer = output_writer
    self.cached_tasks = []

  def _GetIdValue(self, registry_key):
    """Retrieves the Id value from Task Cache Tree key.

    Args:
      registry_key (dfwinreg.WinRegistryKey): Windows Registry key.

    Yields:
      tuple[dfwinreg.WinRegistryKey, dfwinreg.WinRegistryValue]: Windows
          Registry key and value.
    """
    id_value = registry_key.GetValueByName('Id')
    if id_value:
      yield registry_key, id_value

    for subkey in registry_key.GetSubkeys():
      for value_key, id_value in self._GetIdValue(subkey):
        yield value_key, id_value

  def Collect(self, registry):  # pylint: disable=arguments-differ
    """Collects the Task Cache.

    Args:
      registry (dfwinreg.WinRegistry): Windows Registry.

    Returns:
      bool: True if the Task Cache key was found, False if not.
    """
    dynamic_info_size_error_reported = False

    task_cache_key = registry.GetKeyByPath(self._TASK_CACHE_KEY_PATH)
    if not task_cache_key:
      return False

    tasks_key = task_cache_key.GetSubkeyByName('Tasks')
    tree_key = task_cache_key.GetSubkeyByName('Tree')

    if not tasks_key or not tree_key:
      return False

    task_guids = {}
    for subkey in tree_key.GetSubkeys():
      for value_key, id_value in self._GetIdValue(subkey):
        # TODO: improve this check to a regex.
        # The GUID is in the form {%GUID%} and stored an UTF-16 little-endian
        # string and should be 78 bytes in size.

        id_value_data_size = len(id_value.data)
        if id_value_data_size != 78:
          logging.error('Unsupported Id value data size: {0:s}.')
          continue

        guid_string = id_value.GetDataAsObject()
        task_guids[guid_string] = value_key.name

    for subkey in tasks_key.GetSubkeys():
      dynamic_info_value = subkey.GetValueByName('DynamicInfo')
      if not dynamic_info_value:
        continue

      cached_task = CachedTask()
      cached_task.identifier = subkey.name
      cached_task.name = task_guids.get(subkey.name, subkey.name)

      if self._debug:
        if (task_cache_key.last_written_time and
            task_cache_key.last_written_time.timestamp):
          self._output_writer.WriteFiletimeValue(
              'Last written time', task_cache_key.last_written_time.timestamp)

        self._output_writer.WriteValue('Task', cached_task.name)
        self._output_writer.WriteValue('Identifier', cached_task.identifier)
        self._output_writer.WriteText('')

      try:
        self._parser.ParseDynamicInfo(dynamic_info_value.data, cached_task)
      except errors.ParseError as exception:
        if not dynamic_info_size_error_reported:
          logging.error(exception)
          dynamic_info_size_error_reported = True
        continue

      self.cached_tasks.append(cached_task)

    return True
