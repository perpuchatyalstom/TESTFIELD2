import visa

# Create a resource manager
rm = visa.ResourceManager()

# List available instruments (change 'USB' to your desired interface)
instruments = rm.list_resources()

# Find and open the Rigol function generator (replace 'YOUR_DEVICE_ID' with the actual ID)
function_gen = rm.open_resource('USB0::0x1AB1::0x0515::MS5A250801032::INSTR')

# Query the RMS voltage of Channel 1
response = int(function_gen.query('MEAS:freq? chan2'))*1000
print (response)

# Close the connection
function_gen.close()
