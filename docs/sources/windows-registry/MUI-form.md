# Multilingual User Interface (MUI) form

The Multilingual User Interface (MUI) form is used to store strings in multiple
languages. This is also known as Registry string redirection.

The actual strings are stored in the resource sections of PE/COFF files (also
referred to as resource file) e.g .exe, .dll.

In the Registry the MUI strings are referenced using the following form:

```
@path,-stringID[;comment]
```

Where:

* path; is the full path or filename of the resource file that contains the
string
* stringID; the identifier of the string within the string resource of the
resource file
* comment; a comment

For example the MUI form string:

```
@%SystemRoot%\system32\SHELL32.dll,-9227
```

This MUI form string refers to the string with identifier 9227, stored in the
string resource of SHELL32.dll. Which, for an English version of SHELL32.dll,
corresponds to: "My Documents".

An example of a MUI form with comment:

```
@wfplwfs.inf,%WfpLwfs_Name%;WFP LightWeight Filters
```

## Notes

What about the form (seen in the Shell Folder value LocalizedString):

```
@%SystemRoot%\System32\fvecpl.dll,-1#immutable1
```

What does # represent here?

```
@wd.inf,%WdServiceDisplayName%;Microsoft Watchdog Timer Driver
```

Yet another variation seen in Windows 2000.

```
@C:\WINNT\system32\shell32.dll,-9227@1033,My Documents
```

## External Links

* [MSDN: Multilingual User Interface](http://msdn.microsoft.com/en-us/library/windows/desktop/dd319073(v=vs.85).aspx
* [MSDN: Using Registry String Redirection](http://msdn.microsoft.com/library/dd374120(VS.85).aspx)

