## General Instructions for Keylogger
This is logkeys, you can find more about it in this link:<br>
* [logkeys](https://github.com/kernc/logkeys)<br>

**Usage** 

```
$python3 preprocess_youtube.py <URL list> <path>
```
In order to achieve the correct encoding for stdin you need to use the following file:<br>
```
$sudo logkeys -m en_us_ubuntu_1204.map --start -o [log file name.extension]
$sudo logkeys logkeys --kill
```
