import PySimpleGUI as sg
import time

def main():
    # Define the layout of the GUI
    
    sg.theme_background_color('white')
    layout = [[sg.Text('Worktime calculator', text_color='#000000', background_color='white', font=('Helvetica', 20))],
              [sg.Text('Press Start to begin timing' ,text_color='#000000', background_color='white', font=('Helvetica', 20))],
              [sg.Button('Start', button_color ='#306998'),
               sg.Button('Stop', button_color ='#FFD43B'),
               sg.Button('Reset', button_color ='#4B8BBE'),],
              [sg.Text('00:00:00', font=('Helvetica', 20), key='timer', text_color='#228B22', background_color='white')]]

    # Create the window
    window = sg.Window('Bence\'s Stopwatch', layout, element_justification='c')

    # Initialize variables
    start_time, end_time, elapsed_time = None, None, 0
    running = False

    # Event loop
    while True:
        event, values = window.read(timeout=100)  # Időzítő beállítása 100 millimásodperces frissítéssel

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Start' and not running:
            start_time = time.time()
            running = True
        elif event == 'Stop' and running:
            end_time = time.time()
            elapsed_time += end_time - start_time
            running = False
        elif event == 'Reset':
            start_time, end_time, elapsed_time = None, None, 0
            running = False

        # Update the timer display
        if running:
            current_time = time.time()
            elapsed_time += current_time - start_time
            start_time = current_time
        window['timer'].update(time.strftime('%H:%M:%S', time.gmtime(elapsed_time)))

    # Close the window
    window.close()

if __name__ == '__main__':
    main()
