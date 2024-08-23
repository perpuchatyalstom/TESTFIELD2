import pyvisa
import math
import sys

addlib='C:\\ABI\\python\\modules'
if addlib not in sys.path:
	sys.path.append('C:\ABI\python\modules')
import rigol as rg

def rms_mV(rms_val):
    if isinstance(rms_val, str):
        rms_val = float(rms_val)
    return 2 * math.sqrt(2) * rms_val/1000

def main():
    dg2052 = rg.initialize_dg2052()
    inp=159
    freq=15.250
    rg.setup_waveform(dg2052,1, freq*1000, rms_mV(inp), 'SIN')
    print (freq,inp, rms_mV(inp))
    print('First Test ADC0_IEL ; Freq={}kHz level={}mVrms'.format(freq,inp))
    raw_input("Press Enter to continue...")

    rg.outputON(dg2052)
    inp=159
    freq=15.25
    print('Next Test ADC1_SPARE1 ; Freq={}kHz level={}mVrms'.format(freq,inp))
    raw_input("Press Enter to continue...")
    dg2052.write('OUTP OFF')
    rg.setup_waveform(dg2052, 1, freq*1000, rms_mV(inp), 'SIN')
    print ('Freq={}kHz level={}mVrms'.format(freq,inp))
    dg2052.write('OUTP ON')

    inp=335
    freq=30.35
    print('Next Test ADC2_ULAC ; Freq={}kHz level={}mVrms'.format(freq,inp))
    raw_input("Press Enter to continue...")
    dg2052.write('OUTP OFF')
    rg.setup_waveform(dg2052, 1, freq*1000, rms_mV(inp), 'SIN')
    print ('Freq={}kHz level={}mVrms'.format(freq,inp))
    dg2052.write('OUTP ON')
  # Perform any additional operations or setups

    inp=308
    freq=15.25
    print('Next Test ADC3_ULDC; Freq={}kHz level={}mVrms'.format(freq,inp))
    raw_input("Press Enter to continue...")
    dg2052.write('OUTP OFF')
    rg.setup_waveform(dg2052, 1, freq*1000, rms_mV(inp), 'SIN')
    print ('Freq={}kHz level={}mVrms'.format(freq,inp))
    dg2052.write('OUTP ON')

    inp=636
    freq=15.25
    print('Next Test ADC4_UQL; Freq={}kHz level={}mVrms'.format(freq,inp))
    raw_input("Press Enter to continue...")
    dg2052.write('OUTP OFF')
    rg.setup_waveform(dg2052, 1, freq*1000, rms_mV(inp), 'SIN')
    print ('Freq={}kHz level={}mVrms'.format(freq,inp))
    dg2052.write('OUTP ON')

    inp=308
    freq=15.25
    print('Next Test ADC5_UFDCH; Freq={}kHz level={}mVrms'.format(freq,inp))
    raw_input("Press Enter to continue...")
    dg2052.write('OUTP OFF')
    rg.setup_waveform(dg2052, 1, freq*1000, rms_mV(inp), 'SIN')
    print ('Freq={}kHz level={}mVrms'.format(freq,inp))
    dg2052.write('OUTP ON')

    inp=308
    freq=15.25
    print('Next Test ADC6_UBC; Freq={}kHz level={}mVrms'.format(freq,inp))
    raw_input("Press Enter to continue...")
    dg2052.write('OUTP OFF')
    rg.setup_waveform(dg2052, 1, freq*1000, rms_mV(inp), 'SIN')
    print ('Freq={}kHz level={}mVrms'.format(freq,inp))
    dg2052.write('OUTP ON')

    inp=159
    freq=15.25
    print('Next Test ADC7_ILO; Freq={}kHz level={}mVrms'.format(freq,inp))
    raw_input("Press Enter to continue...")
    dg2052.write('OUTP OFF')
    rg.setup_waveform(dg2052, 1, freq*1000, rms_mV(inp), 'SIN')
    print ('Freq={}kHz level={}mVrms'.format(freq,inp))
    dg2052.write('OUTP ON')

    inp=159
    freq=241.74
    print('Next Test ADC8_ILO; Freq={}kHz level={}mVrms'.format(freq,inp))
    raw_input("Press Enter to continue...")
    dg2052.write('OUTP OFF')
    rg.setup_waveform(dg2052, 1, freq*1000, rms_mV(inp), 'SIN')
    print ('Freq={}kHz level={}mVrms'.format(freq,inp))
    dg2052.write('OUTP ON')

    inp=80
    freq=19.641
    print('Connect output generator directly to R1. Right side is GND')
    print('Next Test ADC9_IQLS1; Freq={}kHz level={}mVrms'.format(freq,inp))
    raw_input("Press Enter to continue...")

    dg2052.write('OUTP OFF')
    rg.setup_waveform(dg2052, 1, freq*1000, rms_mV(inp), 'SIN')
    print ('Freq={}kHz level={}mVrms'.format(freq,inp))
    dg2052.write('OUTP ON')
    while True:
        print ('Adjust input level on R1 to 80mVrms?')
        uinp = (raw_input("Enter new input value in mVrms or X to continue: "))
        if uinp.lower() == 'x':
            break
        if uinp != '':
            inp=uinp
        rg.setup_waveform(dg2052, 1, freq*1000, rms_mV(inp), 'SIN')

    inp=51.07
    freq=241.74
    print ('Adjust output level until something happens')
    print('Next Test ADC9_IQLS1: R1 GND=Right; Freq={}kHz level={}mVrms'.format(freq,inp))
    raw_input("Press Enter to continue...")
    dg2052.write('OUTP OFF')
    rg.setup_waveform(dg2052, 1, freq*1000, rms_mV(inp), 'SIN')
    print ('Freq={}kHz level={}mVrms'.format(freq,inp))
    dg2052.write('OUTP ON')
    while True:
        print ('Adjust output level IQLS1 to 51.07mVrms?')
        uinp = (raw_input("Enter new input value in mVrms or X to continue: "))
        if uinp.lower() == 'x':
            break
        if uinp != '':
            inp=uinp
        rg.setup_waveform(dg2052, 1, freq*1000, rms_mV(inp), 'SIN')

    inp=159
    freq=241.74
    print('Next Test ADC10_IQL2; Freq={}kHz level={}mVrms'.format(freq,inp))
    raw_input("Press Enter to continue...")
    dg2052.write('OUTP OFF')
    rg.setup_waveform(dg2052, 1, freq*1000, rms_mV(inp), 'SIN')
    print ('Freq={}kHz level={}mVrms'.format(freq,inp))
    dg2052.write('OUTP ON')

    
    # Close connection
    dg2052.close()


if __name__ == "__main__":

    dg2052 = rg.initialize_dg2052()
#    mso5204 = rg.initialize_mso5204()

#    rg.setup_waveform(dg2052, 1, 1000, rms_mV(707.1), 'SIN')
#    rg.setup_waveform(mso5204,1, 3000, rms_mV(707.1), 'SIN')

#    rg.outputON(dg2052,1)
    #rg.outputOFF(mso5204)

#    dg2052.close()
    
    main()

    sys.exit()

    dg2052 = rg.initialize_dg2052()
    inp=159
    freq=241.641
    print('Connect output generator directly to R1. Right side is GND')
    print('Next Test ADC9_IQLS1; Freq={}kHz level={}mVrms'.format(freq,inp))

    rg.setup_waveform(dg2052, 1, freq*1000, rms_mV(inp), 'SIN')
    print ('Freq={}kHz level={}mVrms'.format(freq,inp))
    dg2052.write('OUTP ON')
    while True:
        inpPrev=inp
        print ('Adjust input level on R1 from {}mVrms?'.format(inp))
        inp = (raw_input("Enter new input value in mVrms or X to continue: "))
        if inp.lower() == 'x':
            break
        if inp == '':
            inp=inpPrev
        rg.setup_waveform(dg2052, 1, freq*1000, rms_mV(inp), 'SIN')
