import os
import re
import pycurl
import io
from multiprocessing import Pool, Manager
from fake_useragent import UserAgent
from colorama import Fore, Style, init

init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.CYAN}
      _____  _____            
     |  __ \\|  __ \\           
     | |__) | |__) |_____   __
     |  _  /|  _  // _ \\ \\ / /
     | | \\ \\| | \\ \\  __/\\ V / 
     |_|  \\_\\_|  \\_\\___| \\_/  
                          
        {Fore.RED}RapidDNS ReverseIP
        Github: IM-Hanzou
{Style.RESET_ALL}
"""
    print(banner)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_content(url, header):
    buffer = io.BytesIO()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, url)
    curl.setopt(curl.HTTPHEADER, header)
    curl.setopt(curl.WRITEDATA, buffer)
    try:
        curl.perform()
        curl.close()
        return buffer.getvalue().decode('utf-8')
    except pycurl.error as e:
        curl.close()
        return str(e)

def process_reversing(ip, domain_list, header):
    try:
        ip = ip.strip()
        if ip.startswith(('http://', 'https://')):
            ip = re.sub(r'^https?://', '', ip)
        
        url = f'https://rapiddns.io/s/{ip}?full=1#result'
        response = fetch_content(url, header)
        results = re.findall(r'</th>\n<td>(.*?)</td>', response)
        num_results = len(results)
        status = 'Failed' if num_results == 0 else num_results
        color = Fore.GREEN if num_results > 0 else Fore.RED
        print(f'{color}[#] Reversed {Fore.MAGENTA}{ip}{Style.RESET_ALL} {color}=>{Style.RESET_ALL} {Fore.YELLOW}{status}{Style.RESET_ALL} {color}domains [#]{Style.RESET_ALL}')
        
        for result in results:
            result = result.strip()
            if result.startswith('www.'):
                result = result[4:]
            if result not in domain_list:
                domain_list.append(result)
                with open('results.txt', 'a+') as file:
                    file.write(result + '\n')
    except Exception as e:
        print(f'{Fore.RED}Error: {e}{Style.RESET_ALL}')

def start_reverse_lookup():
    try:
        clear_screen()
        print_banner()
        ip_list_file = input(f'{Fore.LIGHTYELLOW_EX}IPs list filename: ')
        with open(ip_list_file, 'r') as file:
            lines = file.read().splitlines()
        
        thread_size = 20
        header = [f'User-Agent: {UserAgent().random}']
        
        with Manager() as manager:
            domain_list = manager.list()
            with Pool(thread_size) as pool:
                pool.starmap(process_reversing, [(ip, domain_list, header) for ip in lines])

        print(f"{Fore.LIGHTYELLOW_EX}\nReverse IP Lookup completed.{Style.RESET_ALL}\n{Fore.YELLOW}Results saved to {Fore.LIGHTCYAN_EX}results.txt{Style.RESET_ALL}")
    except Exception as e:
        print(f'{Fore.RED}Error: {e}{Style.RESET_ALL}')

if __name__ == '__main__':
    start_reverse_lookup()
