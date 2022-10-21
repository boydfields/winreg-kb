# Microsoft Office

**TODO this page currently contains rough notes, fine tune these**

## Microsoft Outlook keys

```
HKEY_CURRENT_USER\Software\Microsoft\Office\%VERSION%\Outlook\
```

Where %VERSION% corresponds to:

Value | Description
--- | ---
8.0 | Outlook 97
8.5 | Outlook 98
9.0 | Outlook 2000
10.0 | Outlook 2002/XP
11.0 | Outlook 2003
12.0 | Outlook 2007
14.0 | Outlook 2010
15.0 | Outlook 2013

Values:

Name | Data type | Description
--- | --- | ---
ForcePSTPath | REG_EXPAND_SZ |

```
HKEY_CURRENT_USER\Software\Microsoft\Office\12.0\Outlook\Catalog
```

```
HKEY_CURRENT_USER\Software\Microsoft\Office\14.0\Outlook\Search
HKEY_CURRENT_USER\Software\Microsoft\Office\14.0\Outlook\Search\Catalog
```

```
HKEY_CURRENT_USER\Software\Microsoft\Office\15.0\Outlook\Search
```

Values:

Name | Data type | Description
--- | --- | ---
%FILENAME% | REG_DWORD |

Where %FILENAME% is the full filename of Outlook file.

```
HKEY_CURRENT_USER\Software\Microsoft\Office\15.0\Outlook\Search\Catalog
```

Values:

Name | Data type | Description
--- | --- | ---
%FILENAME% | REG_BINARY |

Where %FILENAME% is the full filename of Outlook file.

For "file/options/search" allow to search through "deleted items"

```
Key: HKCU\Software\Microsoft\Office\14.0\Outlook\Search
Value: IncludeDeletedItems
```

Where the value data is:

```
1 = Yes
```

Outlook generates log files in %temp%\Outlook logging:

```
Key: HKEY_CURRENT_USER\Software\Microsoft\Office\version number\Outlook\Search
Value: EnableLogging = 0xffff0000
```

Protected View mode

```
Key: HKEY_CURRENT_USER\Software\Microsoft\Office\14.0\Outlook\Security
Key: HKEY_CURRENT_USER\Software\Policies\Microsoft\Office\14.0\Outlook\Security
Value: MarkInternalAsUnsafe
```

Where the value data is:

```
1 = Yes
```

### Offline Address Book (OAB)

```
HKEY_CURRENT_USER\Software\Microsoft\Office\%VERSION%\Outlook\Cached Mode
```

Values:

Name | Data type | Description
--- | --- | ---
DownloadOAB | REG_DWORD |

Setting the value to zero prevents Offline Address Book (OAB) download and 
forces Outlook to use the global address list. If the "Cached Mode" key does 
not exist, create it.

### Secure Temp Folder

```
HKEY_CURRENT_USER\Software\Microsoft\Office\%VERSION%\Outlook\Security
```

Values:

Name | Data type | Description
--- | --- | ---
OutlookSecureTempFolder | REG_SZ |

## Most Recently Used (MRU) keys

### File Name MRU keys

Values:

Name | Data type | Description
--- | --- | ---
Maximum Entries | | Numeric value
Value | | Numeric value

```
HKEY_CURRENT_USER\Software\Microsoft\Office\11.0\Common\Open Find\Microsoft Office Excel\Settings\Open\File Name MRU
HKEY_CURRENT_USER\Software\Microsoft\Office\11.0\Common\Open Find\Microsoft Office Excel\Settings\Save As\File Name MRU
HKEY_CURRENT_USER\Software\Microsoft\Office\12.0\Common\Open Find\Microsoft Office Excel\Settings\Open\File Name MRU
HKEY_CURRENT_USER\Software\Microsoft\Office\12.0\Common\Open Find\Microsoft Office Excel\Settings\Save As\File Name MRU
HKEY_CURRENT_USER\Software\Microsoft\Office\12.0\Common\Open Find\Microsoft Office Word\Settings\Save As\File Name MRU
```

### Item MRU keys

Values:

Name | Data type | Description
--- | --- | ---
%ITEM% | | Where %ITEM% is a string in the form: "Item [0-9]+"

```
HKEY_CURRENT_USER\Software\Microsoft\Office\12.0\Excel\File MRU
HKEY_CURRENT_USER\Software\Microsoft\Office\12.0\Excel\Options\MRUFuncs
HKEY_CURRENT_USER\Software\Microsoft\Office\12.0\PowerPoint\File MRU
HKEY_CURRENT_USER\Software\Microsoft\Office\12.0\PowerPoint\RecentAnimationList\EntranceMRU
HKEY_CURRENT_USER\Software\Microsoft\Office\12.0\PowerPoint\RecentAnimationList\EmphasisMRU
HKEY_CURRENT_USER\Software\Microsoft\Office\12.0\PowerPoint\RecentAnimationList\ExitMRU
HKEY_CURRENT_USER\Software\Microsoft\Office\12.0\PowerPoint\RecentAnimationList\MotionPathMRU
HKEY_CURRENT_USER\Software\Microsoft\Office\12.0\PowerPoint\Slide Libraries\Taskpane MRU
HKEY_CURRENT_USER\Software\Microsoft\Office\12.0\Word\File MRU
```

Every %ITEM% value contains:

in Office 12

```
[F00000000][T%FILETIME%]*\\%FILENAME%
```

in Office 14

```
[F00000000][T%FILETIME%][O00000000]*%FILENAME%
```

Where T%FILETIME% contains a FILETIME timestamp as a hexadecimal string (base-16), in upper case, e.g. T01CD10EC460129A0

### Other MRU keys

Find Contact toolbar button (Outlook 97 – 2003)

```
HKEY_CURRENT_USER\Software\Microsoft\Office\%VERSION%\Outlook\Contact\QuickFindMRU\QuickfindMRU
```

Find Pane’s Look in list

```
HKEY_CURRENT_USER\Software\Microsoft\Office\%VERSION%\Outlook\Contact\StripSearchMRU\StripSearchMRU
```

Appointment Locations

```
HKEY_CURRENT_USER\Software\Microsoft\Office\%VERSION%\Outlook\Preferences\LocationMRU
```

Advanced Find’s Search for Word(s)

```
HKEY_CURRENT_USER\Software\Microsoft\Office\%VERSION%\Outlook\Office Finder\MRU 1
```

Advanced Find’s More Choices, Categories

```
HKEY_CURRENT_USER\Software\Microsoft\Office\%VERSION%\Outlook\Office Finder\MRU 3
```

Choose Form dialog (New Item-> More Items-> Choose Form) (Outlook 2010 – 2013)

```
HKEY_CURRENT_USER\Software\Microsoft\Office\%VERSION%\Outlook\Office 
```

## External links

* [Administering the offline address book in Outlook](https://support.microsoft.com/en-us/topic/administering-the-offline-address-book-in-outlook-51958cc8-684a-83f9-aea5-97d4dddc0af4)

