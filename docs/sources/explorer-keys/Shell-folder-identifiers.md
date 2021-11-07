# Shell folder identifier keys

Shell folder identifiers are class identifiers (CLSID) with ShellFolder sub
key of some [COM Class Identifier (CLSID) keys](https://github.com/libyal/winreg-kb/blob/main/documentation/Component%20Object%20Model%20keys.asciidoc).

```
HKEY_CLASSES_ROOT\CLSID\{%GUID%}\ShellFolder
```

## Shell Folder class identifier (CLSID) sub key

Sub keys specific to shell folder identifiers:

Name | Description
--- | ---
shell |
shellex |
ShellFolder |

Values:

Value | Data type | Description
--- | --- | ---
(default value) | |
InfoTip | |
LocalizedString | |
SortOrderIndex | |

### Shell Folder sub key

Values:

Value | Data type | Description
--- | --- | ---
Attributes | REG_DWORD |
CallForAttributes | |
HideOnDesktopPerUser | |

### Attributes values

Value | Identifier | Description
--- | --- | ---
0x00000010 | SFGAO_CANRENAME | The extension's root folder can be renamed by the user. The folder's shortcut menu will have a Rename item.
0x00000020 | SFGAO_CANDELETE | The extension's root folder can be deleted by the user. The folder's shortcut menu will have a Delete item.
0x00000040 | SFGAO_HASPROPSHEET | The extension's root folder has a Properties property sheet. The folder's shortcut menu will have a Properties item.
| |
0x20000000 | SFGAO_FOLDER | The extension's root folder contains one or more items.
0x80000000 | SFGAO_HASSUBFOLDER | The extension's root folder contains one or more subfolders. Windows Explorer will place a plus sign ( `+` ) next to the folder icon.

### Localized String value data

The Localize String value contains a localized version of the folder name, e.g.
on Windows XP the folder identifier key:

```
HKEY_CLASSES_ROOT\CLSID\{450d8fba-ad25-11d0-98a8-0800361b1103}
```

Has a LocalizedString value with the following data:

```
@%SystemRoot%\system32\SHELL32.dll,-9227
```

Which is the [MUI Form](https://winreg-kb.readthedocs.io/en/latest/sources/windows-registry/MUI-form.html)
for "My Documents".

## Notes

TODO: add information about

```
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders
```

```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders
```

## External Links

* [libfwsi: Shell Folder identifiers](https://github.com/libyal/libfwsi/wiki/Shell-Folder-identifiers)
