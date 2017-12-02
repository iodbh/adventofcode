import requests

def get_input(year, day):
    filename =  f'{year}_day_{day}_input'
    with open(filename) as f:
        return f.readlines()
