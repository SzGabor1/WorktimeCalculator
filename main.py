import PySimpleGUI as sg
import time
import json
import os
from datetime import datetime
def main():
    # Define the layout of the GUI
    
    sg.theme_background_color('white')
    layout = [[sg.Text('Worktime calculator', text_color='#000000', background_color='white', font=('Helvetica', 20))],
            [sg.Text('Press Start to begin timing', key='instruction' ,text_color='#000000', background_color='white', font=('Helvetica', 20))],
            [
            sg.Button('Start', button_color=('#000000', '#306998'), pad=((10, 0), (20, 0)), size=(10, 2)),
            sg.Button('Stop', button_color=('#000000', '#FFD43B'), pad=((10, 0), (20, 0)), size=(10, 2)),
            sg.Button('Reset', button_color=('#000000', '#4B8BBE'), pad=((10, 0), (20, 0)), size=(10, 2)),
            ],
            [sg.Text('Customer name', text_color='#000000', background_color='white', font=('Helvetica', 16), pad=((0, 0), (20, 0)))],
            [sg.InputText('', size=(30, 1), key='name', font=('Helvetica', 16))],
            [sg.Text('Completed tasks', text_color='#000000', background_color='white', font=('Helvetica', 16), pad=((0, 0), (20, 0)))],
            [sg.InputText('', size=(30, 1), key='tasks', font=('Helvetica', 16))],
            [sg.Button('Save', button_color=('#000000', '#FFD43B'), size=(10, 2))],
            [sg.Text('00:00:00', font=('Helvetica', 20), key='timer', text_color='#000000', background_color='white')],
              
            [sg.Text('Select the period:', background_color='white')],
            [sg.CalendarButton('Start date', format='%Y-%m-%d', key='-START-', border_width=1, button_color=('#000000', '#306998'))],
            [sg.CalendarButton('End date', format='%Y-%m-%d', key='-END-', border_width=1, button_color=('#000000', '#306998'))],
[
    [sg.Text('Start_time:', font=('Helvetica', 20), text_color='#000000', background_color='white', pad=((0, 0), (20, 0))),
     sg.Text('00:00:00', font=('Helvetica', 20), key='start_time', text_color='#000000', background_color='white')],
    [sg.Text('End_time:', font=('Helvetica', 20), text_color='#000000', background_color='white', pad=((0, 0), (20, 0))),
     sg.Text('00:00:00', font=('Helvetica', 20), key='end_time', text_color='#000000', background_color='white')]
],




            [sg.Text('Worked Hours:', font=('Helvetica', 20), text_color='#000000', background_color='white', pad=((0, 0), (20, 0)))],
              
            [sg.Text('00:00:00', font=('Helvetica', 20), key='worked_hours', text_color='#000000', background_color='white')]
            ]

    # Create the window
    window = sg.Window('Bence\'s Stopwatch', layout, element_justification='c', size=(500, 800), margins=(50, 50))

    # Initialize variables
    start_time, end_time, elapsed_time = None, None, 0
    
    start_time_date, end_time_date = None, None
    
    running = False
    
    last_save_time = 0
    
    last_dates = read_settings()


    # Event loop
    while True:
        event, values = window.read(timeout=100) 

        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Start' and not running:
            start_time = time.time()
            start_time_date = datetime.now().strftime('%H:%M:%S')
            running = True
            window['instruction'].update('Press Stop to stop timing')
            window['timer'].update(text_color='#228B22')
        elif event == 'Stop' and running:
            end_time = time.time()
            elapsed_time += end_time - start_time
            running = False
            window['timer'].update(text_color='#FF0000')
            window['instruction'].update('Press Reset to reset the timer')
            end_time_date = datetime.now().strftime('%H:%M:%S')
        elif event == 'Reset':
            start_time, end_time, elapsed_time = None, None, 0
            running = False
            window['timer'].update(text_color='#000000')
            window['instruction'].update('Press Start to begin timing')
            
        elif event == 'Save':
            # Check if the cooldown period has passed since the last save
            current_time = time.time()
            if current_time - last_save_time < 1:
                sg.popup('Please wait before saving again.', background_color='white', text_color='#000000')
            else:
                result = save_worktime(values['name'], values['tasks'], elapsed_time, start_time_date, end_time_date)
                if result == True:
                    sg.popup('Saved successfully!', background_color='white', text_color='#000000')
                    # Update the last save time
                    last_save_time = current_time
                elif result == False:
                    sg.popup('Error while saving!', background_color='white', text_color='#000000')
                else:
                    sg.popup('Worktime entry with name already exists or 404!', background_color='white', text_color='#000000')
            
        if values['-START-'] and values['-END-']:
            window['worked_hours'].update(time.strftime('%H:%M:%S', time.gmtime(calculate_working_hours(values['-START-'], values['-END-']))))
            if values['-START-'] != last_dates[0]['start_date'] or values['-END-'] != last_dates[0]['end_date']:
                    last_dates[0]['start_date'] = values['-START-']
                    last_dates[0]['end_date'] = values['-END-']
                    with open('settings.json', 'w') as f:
                        json.dump(last_dates, f, indent=4)
        
        elif last_dates:
            window['worked_hours'].update(time.strftime('%H:%M:%S', time.gmtime(calculate_working_hours(last_dates[0]['start_date'], last_dates[0]['end_date']))))


        
                    
                    
        
        # Update the timer display
        if running:
            current_time = time.time()
            elapsed_time += current_time - start_time
            start_time = current_time
        
        window['timer'].update(time.strftime('%H:%M:%S', time.gmtime(elapsed_time)))
        if start_time_date:
            window['start_time'].update(start_time_date)

        if end_time_date:
            window['end_time'].update(end_time_date)
        
    # Close the window
    window.close()

def read_settings():
    try:
        with open('settings.json', 'r') as f:
            data = json.load(f)
            #print(data)
        return data
    except (json.JSONDecodeError, IOError) as e:
        # Handle potential errors
        print(f"Error: {e}")
        return False  # Return False to indicate failure

def calculate_working_hours(start_date, end_date):
    with open('worktime.json', 'r') as f:
        data = json.load(f)
    total_time = 0
    for entry in data:
        if entry['date'] >= start_date and entry['date'] <= end_date:
            total_time += entry['time']
    return total_time
    
def save_worktime(name,tasks, elapsed_time, start_time_date, end_time_date):
    try:
        # Create a dictionary with the name, elapsed time, and current date
        worktime = {
            'name': name,
            'tasks': tasks,
            'time': elapsed_time,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'start-time': start_time_date,
            'end-time': end_time_date
        }

        # Check if the file exists
        if os.path.exists('worktime.json'):
            with open('worktime.json', 'r') as f:
                data = json.load(f)
        else:
            data = []

        # Check if the name already exists in the data
        if any(entry['name'] == name for entry in data):
            print(f"Worktime entry with name '{name}' already exists. No duplicate entry added.")
            return "Same name"  # Return False to indicate failure

        data.append(worktime)

        # Write the data back to the JSON file
        with open('worktime.json', 'w') as f:
            json.dump(data, f, indent=4)

        return True  # Return True if the operation was successful

    except (json.JSONDecodeError, IOError) as e:
        # Handle potential errors
        print(f"Error: {e}")
        return False  # Return False to indicate failure

if __name__ == '__main__':
    main()
