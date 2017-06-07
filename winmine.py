from ctypes import *
from ctypes.wintypes import *
import struct

def getpid(process_name):
    import os
    return [item.split()[1] for item in os.popen('tasklist').read().splitlines()[4:] if process_name in item.split()]


showField = ''
i=0 #for print


OpenProcess = windll.kernel32.OpenProcess
ReadProcessMemory = windll.kernel32.ReadProcessMemory
CloseHandle = windll.kernel32.CloseHandle

PROCESS_ALL_ACCESS = 0x1F0FFF
pid = int(getpid('winmine.exe')[0])


FieldAddress = 0x01005340
BombAddress = 0x010056a4
AddAddress = 0x00000000

buffer = c_char_p(b"aa")


processHandle = OpenProcess(PROCESS_ALL_ACCESS, False, pid)


if ReadProcessMemory(processHandle, BombAddress, buffer, 2, 0):
	bombcount = ord(buffer.value)
	bombMax = bombcount
	
	while 1:
		if ReadProcessMemory(processHandle, FieldAddress+AddAddress, buffer, 2, 0):
			edit = buffer.value
			edit = edit.replace('\x0f', '0 ')
			edit = edit.replace('\x10', '-')
			edit = edit.replace('\x8f', '* ')
			showField += edit
			if edit == '0 * ' or edit == '* 0 ' or edit == '-* ' or edit == '* -':
				bombcount -= 1
			if edit == '* * ':
				bombcount -= 2
			if bombcount == 0 and edit == '--':
				break
			AddAddress += 0x00000002

	if bombMax == 10 or bombMax == 40:
		showField = showField.replace('--','').split('-')
	elif bombMax == 99:
		showField = showField.replace('---','').split('-')

	if bombMax==40 or bombMax==99:
		print ''

	if bombMax==10 or bombMax==99:
		a = 0
	else:
		a = 1

	for show in showField:
		if i%2 == a:
			print show
		i+=1
	
else:
    print("Failed.")
CloseHandle(processHandle)
