# Most recently used (MRU)

The Windows Registry contains various keys with information about Most Recently
files Used (MRU). Windows Explorer (or Windows shell), extensively uses such
keys. Several different variants of MRU keys are known to be used, such as:

* Keys with a MRUList value
* Keys with a MRUListEx value
* BagMRU key

## Keys with a MRUList value

Values:

Value | Data type | Description
--- | --- | ---
MRUList | | Contains a list of the most recently used (MRU) items. <br/> Consists of an array of UTF-16 little-endian formatted character value. <br/> The first value represents the most recently used item, the second the second recently used item and so forth. The last value indicates the end of the list and should be 0 (0x0000).
%ALPHA% | | Where %ALPHA% is a string in the form: "[a-z]" <br/> The value name corresponds to a string value in the MRUList value. E.g. a MRUList value of "a" (0x0061) corresponds to the value "a".

### String MRUList values

The following keys with a MRUList value contain %ALPHA% values that consists of
an UTF-16 little-endian formatted string with an end-of-string character.

Sub keys of: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\`

Registry key | Windows version | Description
--- | --- | ---
ComDlg32\LastVisitedMRU | 2000, XP |
ComDlg32\OpenSaveMRU\%EXTENSION% | 2000, XP | <br/> Where %EXTENSION% is a file extension like "exe" or "\*"
Doc Find Spec MRU | | Most recently used "Find Files" commands
FileExts\%EXTENSION%\OpenWithList | 2000, XP, Vista | Most recently used "Open With" commands <br/> Where %EXTENSION% is a file extension like ".exe"
FindComputerMRU | | Most recently used "Find Computer" commands
Map Network Drive MRU | XP | Most recently used mapped network drives
PrnPortsMRU | | Most recently used printer ports
RecentDocs | 2000, XP |
RecentDocs\%EXTENSION% | 2000, XP | <br/> Where %EXTENSION% is a file extension like ".exe" or "Folder"
RunMRU | NT4, 2000, XP, Vista | Most recently used "Run" commands
WordWheelQuery | |

### Shell Item List MRUList values

The following keys with a MRUList value contain %ALPHA% values that consists of
a Shell Item List.

Sub keys of: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\`

Registry key | Windows version | Description
--- | --- | ---
DesktopStreamMRU | NT4 | How icons are arranged on the desktop. <br/> Although the key is present on later versions of Windows it does not seem to be used anymore.

## Keys with a MRUListEx value

Values:

Value | Data type | Description
--- | --- | ---
MRUListEx | | Contains a list of the most recently used (MRU) items. <br/> Consists of an array of 4-byte little-endian values. <br/> The first value represents the most recently used item, the second the second recently used item and so forth. The last value indicates the end of the list and should be -1 (0xffffffff).
%NUMERIC% | | Where %NUMERIC% is a string in the form: "[0-9]+" <br/> The value name corresponds to a 4-byte numeric value in the MRUListEx value. E.g. a MRUListEx value of 0x00000001 corresponds to the value named "1".

The value data of the numeric value depends on the sub key.

### String MRUListEx values

The following keys with a MRUListEx value contain %NUMERIC% values that
consists of an UTF-16 little-endian formatted string with an end-of-string
character.

### Shell Item List MRUListEx values

The following keys with a MRUListEx value contain %NUMERIC% values that
consists of a Shell Item List.

Sub keys of: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\`

Registry key | Windows version | Description
--- | --- | ---
ComDlg32\OpenSavePidlMRU\%EXTENSION% | Vista | <br/> Where %EXTENSION% is a file extension like "exe" or "\*"
StreamMRU | 2000, XP |

### String and Shell Item MRUListEx values

The following keys with a MRUListEx value contain %NUMERIC% values that
consists of a String and Shell Item. The String and Shell Item is variable of
size and consists of:

Offset | Size | Value | Description
--- | --- | --- | ---
0 | ... | | The filename stored as an UTF-16 little-endian formatted string with end-of-string character
... | ... | | The filename stored as a Shell Item. <br/> The Shell Item is empty if not set.

Sub keys of: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\`

Registry key | Windows version | Description
--- | --- | ---
RecentDocs | Vista |
RecentDocs\%EXTENSION% | Vista | Where %EXTENSION% is a file extension like .exe or Folder

### String and Shell Item List MRUListEx values

The following keys with a MRUListEx value contain %NUMERIC% values that
consists of a String and Shell Item List. The String and Shell Item List is
variable of size and consists of:

Offset | Size | Value | Description
--- | --- | --- | ---
0 | ... | | The filename stored as an UTF-16 little-endian formatted string with end-of-string character
... | ... | | The path stored as a Shell Item List. <br/> The first Shell Item is empty if not set.

Sub keys of: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\`

Registry key | Windows version | Description
--- | --- | ---
ComDlg32\LastVisitedPidlMRU | Vista, 7 |

## BagMRU key

The values in the BagMRU and sub keys are also referred to as "shellbags".

BagMRU keys as of XP (stored in NTUSER.DAT)

```
HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\BagMRU
HKEY_CURRENT_USER\Software\Microsoft\Windows\ShellNoRoam\BagMRU
```

Additional BagMRU keys as of Vista (stored in USRCLASS.DAT)

```
HKEY_CURRENT_USER\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU
HKEY_CURRENT_USER\Software\Classes\Local Settings\Software\Microsoft\Windows\ShellNoRoam\BagMRU
HKEY_CURRENT_USER\Software\Classes\Wow6432Node\Local Settings\Software\Microsoft\Windows\Shell\BagMRU
HKEY_CURRENT_USER\Software\Classes\Wow6432Node\Local Settings\Software\Microsoft\Windows\ShellNoRoam\BagMRU
```

Seen in Windows 7:

```
HKEY_CURRENT_USER\Local Settings\Software\Microsoft\Windows\Shell\BagMRU
```

The BagMRU sub keys form a hierarchy similar to a folder structure.

Values:

Value | Data type | Description
--- | --- | ---
NodeSlot | REG_DWORD | Contains the node slot index number (also referred to as bag number) <br/> This number corresponds to the sub key name the corresponding Bags sub key. <br/> E.g. bag number 1 in HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\BagMRU relates to the Bags sub key HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\Bags\1
NodeSlots | | Only present in the root BagMRU key.
MRUListEx | REG_BINARY | Contains a list of the most recently used (MRU) items. <br/> Consists of an array of 4-byte little-endian values. <br/> The first value represents the most recently used item, the second the second recently used item and so forth. The last value indicates the end of the list and should be -1 (0xffffffff).
%NUMERIC% | REG_BINARY | Where %NUMERIC% is a string in the form: "[0-9]+" <br/> The value name corresponds to a 4-byte numeric value in the MRUListEx value. E.g. a MRUListEx value of 0x00000001 corresponds to the value named "1". <br/> Contains a shell item

### Bag number shell sub key

The numbered sub keys of the Bags key have a Shell sub key e.g.

```
HKEY_CURRENT_USER\Software\Microsoft\Windows\Shell\Bags\1\Shell
```

This key contains various values:

Value | Data type | Description
--- | --- | ---
Address | |
Buttons | |
Col | |
ColInfo | |
FolderType | |
FFlags | |
HotKey | |
Links | |
MinPos%GEOMETRY%(1).bottom | | Where %GEOMETRY% is the screen geometry in the form 1100x705
MinPos%GEOMETRY%(1).left | | Where %GEOMETRY% is the screen geometry in the form 1100x705
MinPos%GEOMETRY%(1).right | | Where %GEOMETRY% is the screen geometry in the form 1100x705
MinPos%GEOMETRY%(1).top | | Where %GEOMETRY% is the screen geometry in the form 1100x705
MinPos%GEOMETRY%(1).x | | Where %GEOMETRY% is the screen geometry in the form 1100x705
MinPos%GEOMETRY%(1).y | | Where %GEOMETRY% is the screen geometry in the form 1100x705
Mode | |
Rev | |
ScrollPos%GEOMETRY%(1).x | | Where %GEOMETRY% is the screen geometry in the form 1100x705
ScrollPos%GEOMETRY%(1).y | | Where %GEOMETRY% is the screen geometry in the form 1100x705
ShowCmd | |
Sort | |
SortDir | |
Vid | |
WFlags | |

## Notes

This section contains some notes on explorer MRU keys that need to be completed.

### Wallpaper MRU key MRUListEx value

Sub keys of: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\`

Registry key | Windows version | Description
--- | --- | ---
Wallpaper\MRU | XP, 2003 | Most recently used wallpapers

```
00000000  43 00 3a 00 5c 00 57 00  49 00 4e 00 44 00 4f 00  |C.:.\.W.I.N.D.O.|
00000010  57 00 53 00 5c 00 42 00  6c 00 75 00 65 00 20 00  |W.S.\.B.l.u.e. .|
00000020  4c 00 61 00 63 00 65 00  20 00 31 00 36 00 2e 00  |L.a.c.e. .1.6...|
00000030  62 00 6d 00 70 00 00 00  70 00 00 00 00 00 00 00  |b.m.p...p.......|
00000040  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000050  00 00 00 00 78 01 08 00  00 00 00 00 00 00 00 00  |....x...........|
00000060  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000070  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000080  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000090  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
000000a0  00 00 00 00 28 f6 0b 00  00 00 00 00 70 4b 0c 00  |....(.......pK..|
000000b0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
000000c0  00 00 00 00 00 00 00 00  28 f6 0b 00 00 00 00 00  |........(.......|
000000d0  78 5b 0c 00 00 00 00 00  20 f6 0b 00 00 00 00 00  |x[...... .......|
000000e0  78 01 08 00 00 00 00 00  00 00 00 00 00 00 00 00  |x...............|
000000f0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000100  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000110  00 00 00 00 00 00 00 00  78 01 08 00 92 02 00 00  |........x.......|
00000120  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000130  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000140  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000150  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000160  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000170  00 00 00 00 00 00 00 00  28 f6 0b 00 00 00 00 00  |........(.......|
00000180  01 02 00 00 00 00 00 00  68 4b 0c 00 08 10 00 00  |........hK......|
00000190  68 4b 0c 00 00 00 00 00  70 4b 0c 00 78 01 08 00  |hK......pK..x...|
000001a0  08 10 00 00 2f 2d f4 77  51 8e e4 77 f8 00 00 00  |..../-.wQ..w....|
000001b0  00 00 00 00 00 00 00 00  00 00 00 00 50 f4 a2 00  |............P...|
000001c0  70 4b 0c 00 00 10 00 00  03 00 00 00 28 8d e4 77  |pK..........(..w|
000001d0  f4 dc 0b 00 36 8e e4 77  04 01 00 00 ab 3d 29 77  |....6..w.....=)w|
000001e0  40 fd a2 00 00 00 00 00  d6 0f 00 00 a8 4e 0c 00  |@............N..|
000001f0  00 d0 fd 7f 00 00 00 00  be 20 08 00 01 00 00 00  |......... ......|
00000200  e0 dc 0b 00 08 00 00 00  30 00 00 00 30 00 00 00  |........0...0...|
00000210  00 60 a9 0f c6 f2 c2 01                           |.`......|
```

### Explorer MRUList

```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\MRU
```

### CIDSizeMRU MRUListEx

Seen on Windows Vista

```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\CIDSizeMRU
```

```
00000000  66 00 69 00 72 00 65 00  66 00 6f 00 78 00 2e 00  |f.i.r.e.f.o.x...|
00000010  65 00 78 00 65 00 00 00  00 00 00 00 00 00 00 00  |e.x.e...........|
00000020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
...
00000200  00 00 00 00 00 00 00 00  12 00 00 00 0b 00 00 00  |................|
00000210  22 04 00 00 15 03 00 00  00 00 00 00 00 00 00 00  |"...............|
00000220  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000230  00 00 00 00 00 00 00 00  1a 00 00 00 27 00 00 00  |............'...|
00000240  7c 02 00 00 d6 00 00 00  00 00 00 00 00 00 00 00  |...............|
```

MRUListEx

```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\FirstFolder
```

Contains an UTF-16 little-endian formatted string.

## External Links

* [Windows Shell Item format specification](https://github.com/libyal/libfwsi/blob/main/documentation/Windows%20Shell%20Item%20format.asciidoc)

