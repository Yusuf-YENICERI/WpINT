from email import header
from json import JSONDecodeError
import requests




class fcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[37m'




headers = {
    "api-key": "<enter-your-leakix-api-key-here>",
    "Accept": "application/json"
}


print(f"""{fcolors.OKGREEN}
             @@@@@@@@@@@@                                                       
          @@             @@                                                   
        @@    #######      @@      @@  @@  @@         @@  @@@@@@ ######             
        @@   ##      ##    @@      @&  @@  &@         @@  @@  @@   &@               
         @@   ##      ##   @@      @&  @@  &@  @#@@@  @@  @@  @@   &@               
          @@   ##     ##  @@       @&  @@  &@  @# @@  @@  @@  @@   &@               
           @@     #####  @@        @&@@@@@@&@  @%@@@  @@  @@  @@   &@               
             @@        #                       @#                                
               @@@@@@@@ #                      @#                                 
""")

username = str(input(f"{fcolors.HEADER}Please enter username-surname to search the internet to find wordpress website: {fcolors.WHITE}"))

print()

try:
    results = requests.get(f'https://leakix.net/search?q=plugin%3A"WpUserEnumHttp"+%2B+"{username}"&scope=leak', headers=headers).json()
    page = 2
    while True:
        for result in results:
            if result['event_source'] == 'WpUserEnumHttp':
                ip, host, port, summary, country_name, organization_name = result['ip'], result['host'], result['port'], result['summary'], result['geoip']['country_name'], result['network']['organization_name']
                print(f"{fcolors.OKBLUE}{fcolors.BOLD}{country_name}   {organization_name}   {host if host else (ip if ip else '')}:{port}\n")
                print(f"{fcolors.OKGREEN}{summary}\n\n\n")
        if len(results) == 20:
            try:
                results = requests.get(f'https://leakix.net/search?page={page}&q=plugin%3A"WpUserEnumHttp"+%2B+"{username}"&scope=leak', headers=headers).json()
                page += 1
            except:
                break
        else:
            break
except ValueError:
    print(f'{fcolors.WARNING}user can\'t be found, now program will search by words starting from the last one\n')

    generated_names = [i for i in username.split(' ') if len(i) != 0]
    generated_names.reverse()
    for name in generated_names:
        try:
            results = requests.get(f'https://leakix.net/search?page=1&q=plugin%3A"WpUserEnumHttp"+%2B+"{name}"&scope=leak', headers=headers).json()
            page = 2
            while True:
                for result in results:
                    if result['event_source'] == 'WpUserEnumHttp':
                        ip, host, port, summary, country_name, organization_name = result['ip'], result['host'], result['port'], result['summary'], result['geoip']['country_name'], result['network']['organization_name']
                        print(f"{fcolors.OKBLUE}{fcolors.BOLD}{country_name}   {organization_name}   {host if host else (ip if ip else '')}:{port}\n")
                        print(f"{fcolors.OKGREEN}{summary}\n\n\n")
                if len(results) == 20:
                    try:
                        results = requests.get(f'https://leakix.net/search?page={page}&q=plugin%3A"WpUserEnumHttp"+%2B+"{name}"&scope=leak', headers=headers).json()
                        page += 1
                    except:
                        break
                else:
                    break
        except Exception as ex:
            print(ex)
            print(f"{fcolors.FAIL}no user found for {name}!")
    