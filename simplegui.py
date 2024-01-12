# hello_psg.py

import PySimpleGUI as sg
import sys
import glob
import serial

names = []
bauds = [9600,250000]


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    print(result)
    return result


layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]

# Create the window
lst = sg.Combo(names,default_value="Please choose a COM Port", font=('Arial Bold', 14),  expand_x=True, enable_events=True,  readonly=False, key='-COMBO-')
lst2 = sg.Combo(bauds,default_value=bauds[0],font=('Arial Bold', 14),  expand_x=True, enable_events=True,  readonly=False, key='-baud_COMBO-')
layout = [[
    lst,
    lst2,
    #sg.Button('Add', ),
    sg.Button('Update'),
    sg.Button('Open')],
    [sg.Text("", key='-MSG-',
        font=('Arial Bold', 14),
        justification='center')]
]
window = sg.Window('Choose COM Port', layout, size=(715, 200))
while True:
    ch = ''
    event, values = window.read()
    names.append(serial_ports)
    print(event, values)

    if event == 'Update':
        del names
        new_ports = serial_ports
        if new_ports == []:
            names[0] = 'No COM Ports found'
        else:
            names = new_ports
            window['-COMBO-'].update(values=names, value=values['-COMBO-'])
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Open':
        #names.append(values['-COMBO-'])
        print(names)
        window['-COMBO-'].update(values=names, value=values['-COMBO-'])
        msg = "A new item added : {}".format(values['-COMBO-'])
        window['-MSG-'].update(msg)
    if event == '-COMBO-':
        ch = sg.popup_yes_no("Do you want to Continue?", title="YesNo")
    if ch == 'Yes':
        val = values['-COMBO-']
        names.remove(val)
    window['-COMBO-'].update(values=names, value=' ')
    #msg = "A new item removed : {}".format(val)
    #window['-MSG-'].update(msg)
    
print(serial_ports)