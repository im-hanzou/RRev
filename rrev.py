import os
import re
import threading
import requests
from fake_useragent import UserAgent
from colorama import Fore, Style, init

init(autoreset=True)

def print_banner():
    banner = f"""
{Fore.CYAN}
      _____  _____            
     |  __ \|  __ \           
     | |__) | |__) |_____   __
     |  _  /|  _  // _ \ \ / /
     | | \ \| | \ \  __/\ V / 
     |_|  \_\_|  \_\___| \_/  
                          
        {Fore.RED}RapidDNS ReverseIP
        Github: IM-Hanzou
{Style.RESET_ALL}
"""
    print(banner)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def process_reversing(ips):
    try:
        for ip in ips:
            ip = ip.strip()
            if ip.startswith(('http://', 'https://')):
                ip = re.sub(r'^https?://', '', ip)
            response = session.get(f'https://rapiddns.io/s/{ip}?full=1#result', headers=header, verify=True).content.decode('utf-8')
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
        
        thread_size = 50
        coks = [lines[i:i + thread_size] for i in range(0, len(lines), thread_size)]
        threads = []
        for cok in coks:
            thread = threading.Thread(target=process_reversing, args=(cok,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        print(f"{Fore.LIGHTYELLOW_EX}\nReverse IP Lookup completed.{Style.RESET_ALL}\n{Fore.YELLOW}Results saved to {Fore.LIGHTCYAN_EX}results.txt{Style.RESET_ALL}")
    except Exception as e:
        print(f'{Fore.RED}Error: {e}{Style.RESET_ALL}')

if __name__ == '__main__':
    session = requests.Session()
    user_agent = UserAgent()
    header = {'User-Agent': user_agent.random}
    domain_list = []
    start_reverse_lookup()
