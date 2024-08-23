import binascii
import csv

patfile='C:\\ABI\\XE-FQC1\\media\\6.7.4a-readstatus.pat'
patout='C:\\ABI\\XE-FQC1\\media\\6.7.3b-readstatus.pat'
patcsv='C:\\ABI\\XE-FQC1\\media\\6.7.3b-readstatus.csv'

with open(patfile,'rb') as f:
    bindata=f.read()

hex_data = binascii.hexlify(bindata)

hex_elements = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]
with open(patcsv,'wb') as f:
    for item in hex_elements:
        #print item
        f.write(item+'\n')

print hex_elements[4403]
hex_elements[4845]='01'

hex_string = ''.join(hex_elements)
bindata = binascii.unhexlify(hex_string)

#print bindata

with open(patout,'wb') as f:
    f.write(bindata)