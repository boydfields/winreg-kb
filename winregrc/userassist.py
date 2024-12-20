# -*- coding: utf-8 -*-
"""Windows UserAssist information collector."""

import codecs
import logging

from winregrc import data_format
from winregrc import errors
from winregrc import interface


class UserAssistEntry(object):
  """UserAssist entry.

  Attributes:
    guid (str): GUID.
    name (str): name.
    value_name (str): name of the Windows Registry value.
  """

  def __init__(self, guid=None, name=None, value_name=None):
    """Initializes an UserAssist entry.

    Args:
      guid (Optional[str]): GUID.
      name (Optional[str]): name.
      value_name (Optional[str]): name of the Windows Registry value.
    """
    super(UserAssistEntry, self).__init__()
    self.guid = guid
    self.name = name
    self.value_name = value_name


class UserAssistDataParser(data_format.BinaryDataFormat):
  """UserAssist data parser."""

  _DEFINITION_FILE = 'userassist.yaml'

  # pylint: disable=missing-type-doc
  def _DebugPrintEntry(self, format_version, user_assist_entry):
    """Prints UserAssist entry value debug information.

    Args:
      format_version (int): format version.
      user_assist_entry (user_assist_entry_v3|user_assist_entry_v5):
          UserAssist entry.
    """
    self._DebugPrintValue('Unknown1', f'0x{user_assist_entry.unknown1:08x}')

    self._DebugPrintDecimalValue(
        'Number of executions', user_assist_entry.number_of_executions)

    if format_version == 5:
      self._DebugPrintDecimalValue(
          'Application focus count',
          user_assist_entry.application_focus_count)

      self._DebugPrintDecimalValue(
          'Application focus duration',
          user_assist_entry.application_focus_duration)

      self._DebugPrintValue('Unknown2', f'{user_assist_entry.unknown2:.2f}')
      self._DebugPrintValue('Unknown3', f'{user_assist_entry.unknown3:.2f}')
      self._DebugPrintValue('Unknown4', f'{user_assist_entry.unknown4:.2f}')
      self._DebugPrintValue('Unknown5', f'{user_assist_entry.unknown5:.2f}')
      self._DebugPrintValue('Unknown6', f'{user_assist_entry.unknown6:.2f}')
      self._DebugPrintValue('Unknown7', f'{user_assist_entry.unknown7:.2f}')
      self._DebugPrintValue('Unknown8', f'{user_assist_entry.unknown8:.2f}')
      self._DebugPrintValue('Unknown9', f'{user_assist_entry.unknown9:.2f}')
      self._DebugPrintValue('Unknown10', f'{user_assist_entry.unknown10:.2f}')
      self._DebugPrintValue('Unknown11', f'{user_assist_entry.unknown11:.2f}')
      self._DebugPrintValue('Unknown12', f'0x{user_assist_entry.unknown12:08x}')

    self._DebugPrintFiletimeValue(
        'Last execution time', user_assist_entry.last_execution_time)

    if format_version == 5:
      self._DebugPrintValue('Unknown13', '0x{user_assist_entry.unknown13:08x}')

    self._DebugPrintText('\n')

  # pylint: disable=missing-return-type-doc
  def ParseEntry(self, format_version, entry_data):
    """Parses an UserAssist entry.

    Args:
      format_version (int): format version.
      entry_data (bytes): entry data.

    Returns:
      user_assist_entry_v3|user_assist_entry_v5: UserAssist entry.

    Raises:
      ParseError: if the value data could not be parsed.
    """
    if format_version == 3:
      data_type_map = self._GetDataTypeMap('user_assist_entry_v3')
      expected_entry_data_size = 16
    elif format_version == 5:
      data_type_map = self._GetDataTypeMap('user_assist_entry_v5')
      expected_entry_data_size = 72
    else:
      data_type_map = None
      expected_entry_data_size = 0

    if expected_entry_data_size != len(entry_data):
      entry_data_size = len(entry_data)
      raise errors.ParseError((
          f'Version: {format_version:d} size mismatch (calculated: '
          f'{expected_entry_data_size:d}, stored: {entry_data_size:d}).'))

    try:
      user_assist_entry = self._ReadStructureFromByteStream(
          entry_data, 0, data_type_map, 'UserAssist entry')
    except (ValueError, errors.ParseError) as exception:
      raise errors.ParseError(
          f'Unable to parse UserAssist entry value with error: {exception!s}')

    if self._debug:
      self._DebugPrintEntry(format_version, user_assist_entry)

    return user_assist_entry


class UserAssistCollector(interface.WindowsRegistryKeyCollector):
  """Windows UserAssist information collector.

  Returns:
    user_assist_entries (list[UserAssistEntry]): UserAssist entries.
  """

  _USER_ASSIST_KEY = (
      'HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\'
      'Explorer\\UserAssist')

  def __init__(self, debug=False, output_writer=None):
    """Initializes a Windows UserAssist information collector.

    Args:
      debug (Optional[bool]): True if debug information should be printed.
      output_writer (Optional[OutputWriter]): output writer.
    """
    super(UserAssistCollector, self).__init__(debug=debug)
    self._output_writer = output_writer
    self._parser = UserAssistDataParser(
        debug=debug, output_writer=output_writer)
    self.user_assist_entries = []

  def _CollectUserAssistFromKey(self, guid_subkey):
    """Collects the UserAssist information from a GUID sub key.

    Args:
      guid_subkey (dfwinreg.WinRegistryKey): UserAssist GUID Registry key.
    """
    version_value = guid_subkey.GetValueByName('Version')
    if not version_value:
      logging.warning(f'Missing Version value in sub key: {guid_subkey.name:s}')
      return

    format_version = version_value.GetDataAsObject()

    if self._debug:
      self._output_writer.WriteValue('GUID', guid_subkey.name)
      self._output_writer.WriteIntegerValueAsDecimal(
          'Format version', format_version)

      self._output_writer.WriteText('\n')

    count_subkey = guid_subkey.GetSubkeyByName('Count')
    for value in count_subkey.GetValues():
      if self._debug:
        self._output_writer.WriteValue('Original name', value.name)

      try:
        # Note that Python 2 codecs.decode() does not support keyword arguments
        # such as encodings='rot-13'.
        value_name = codecs.decode(value.name, 'rot-13')
      except UnicodeEncodeError:
        characters = []
        for character in value.name:
          if ord(character) < 128:
            try:
              character = codecs.decode(character, 'rot-13')
              characters.append(character)
            except UnicodeEncodeError:
              characters.append(character)
          else:
            characters.append(character)

        value_name = ''.join(characters)

      if self._debug:
        self._output_writer.WriteValue('Converted name', value_name)
        self._output_writer.WriteDebugData('Value data:', value.data)

      if value_name != 'UEME_CTLSESSION':
        user_assist_entry = self._parser.ParseEntry(format_version, value.data)

        user_assist_entry = UserAssistEntry(
            guid=guid_subkey.name, name=value_name, value_name=value.name)
        self.user_assist_entries.append(user_assist_entry)

  def Collect(self, registry):  # pylint: disable=arguments-differ
    """Collects the UserAssist information.

    Args:
      registry (dfwinreg.WinRegistry): Windows Registry.

    Returns:
      bool: True if the UserAssist key was found, False if not.
    """
    user_assist_key = registry.GetKeyByPath(self._USER_ASSIST_KEY)
    if not user_assist_key:
      return False

    for guid_subkey in user_assist_key.GetSubkeys():
      self._CollectUserAssistFromKey(guid_subkey)

    return True
