# main.py


try:
    with open('mission_computer_main.log', 'r') as log_file:
        log_data = log_file.readlines()

        print('All Log List (Reversed Order) >>>>>')
        for line in log_data:
            print(line.strip(), '\n')


except FileNotFoundError:
    print('File not found.')
except Exception as e:
    print(f"except: {e}")
