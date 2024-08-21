"""
dns propagation 是域的名称服务器更新所需的时间
或者是世界各地的ISP使用域的新dns信息更新其缓存所需的时间。
DNS传播通常需要24-48小时, 但如果域位于地理位置较远的区域,  则DNS传播也可能高达72小时。

First # python3 -m venv /Users/wangdejia/Desktop/smartproxy-dns-checker/venv
source /Users/wangdejia/Desktop/smartproxy-dns-checker/venv/bin/activate
pip install requests && pip install dnspython

"""

import requests
import socket
import dns.resolver
import json
import time
from datetime import datetime

########################################################################################## Proxy Detail Print

def get_proxy_details(proxy):
    proxy_url = f"http://{proxy}"
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    
    try:
        # Get the proxy IP address
        ip_response = requests.get('https://api.ipify.org?format=json', proxies=proxies)
        ip_response.raise_for_status()
        ip = ip_response.json().get('ip')
        
        if ip:
            # Get detailed information about the IP
            details_url = f"https://ipinfo.io/{ip}/json"
            details_response = requests.get(details_url, proxies=proxies)
            details_response.raise_for_status()
            details = details_response.json()
            
            return details
        
        return None
    
    except requests.RequestException as e:
        print(f"# Error retrieving proxy details with proxy {proxy}: {e}")
        return None

########################################################################################## Proxy Setup Function

# Proxy settings
PROXY_USERNAME = "user-sp69q79ipz-sessionduration-1"
PROXY_PASSWORD = "3k5xvzZu6G7uiHfhW_"
PROXY_HOST = "ph.smartproxy.com"
# Proxy DNS range
PROXY_PORT_START = 41001
PROXY_PORT_END = 41201

def generate_proxy_list():
    return [f"{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{port}" for port in range(PROXY_PORT_START, PROXY_PORT_END + 1)]

def query_dns_via_resolver(domain, resolver_ip):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [resolver_ip]
    try:
        answers = resolver.resolve(domain, 'A')
        return [answer.address for answer in answers]
    except dns.exception.DNSException as e:
        print(f"# Error querying DNS via resolver {resolver_ip}: {e}")
        return None

########################################################################################## Frontend Load Speed Test Function

def measure_load_speed(proxy, domain):
    url = f"https://{domain}"
    proxy_url = f"http://{proxy}"
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
    try:
        start_time = time.time()
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()  # Check for HTTP errors
        load_time = time.time() - start_time
        return load_time
    except requests.RequestException as e:
        print(f"# Error measuring load speed with proxy {proxy_url}: {e}")
        return None

########################################################################################## Main Function

def main():
    domain = "hawkgaming.com"
    proxy_list = generate_proxy_list()
    anchor_ips = []  # List to store the first three matching IP sets
    
    for proxy in proxy_list:
        executed_time = datetime.now().strftime("%Y-%m-%d:%H:%M")
        execution_status = "Success"
        dns_result = None
        
        print(f"# Querying DNS for {domain} using proxy {proxy}...")

        # Print proxy details
        details = get_proxy_details(proxy)
        if details:
            print(f"# Proxy IP: {details.get('ip')}, Region: {details.get('region')}, ISP: {details.get('org')}")
        else:
            print(f"# Failed to retrieve details from proxy {proxy}")

        # Query DNS using a resolver close to the proxy's network (you can set up a DNS server in the proxy's region)
        if details and 'ip' in details:
            resolver_ip = details['ip']  # You may need a DNS resolver IP near the proxy
            current_ips = query_dns_via_resolver(domain, resolver_ip)
            if current_ips:
                # Store the IPs from the DNS answer
                if len(anchor_ips) < 3:
                    anchor_ips.append(set(current_ips))
                else:
                    # Check if the current IPs match with any of the anchor IPs
                    if not any(set(current_ips) == anchor_set for anchor_set in anchor_ips):
                        execution_status = "Fail_DNS_Poison_Possible"
            else:
                execution_status = "Fail_No_Answer"
                print(f"# Failed to retrieve DNS results from proxy {proxy}")

        # Measure frontend load speed and store the results
        load_time = measure_load_speed(proxy, domain)
        if load_time is not None:
            print(f"# Frontend load time for {domain}: {load_time:.2f} seconds")
        else:
            execution_status = "Fail_Load_Error"
            print(f"# Failed to measure load speed with proxy {proxy}")

        # Construct the execution detail
        execution_detail = {
            "execution_detail": {
                "target_domain": f"https://{domain}",
                "executed_time": executed_time,
                "proxy_url": proxy,
                "smart_proxy_ip": details.get('ip') if details else None,
                "region": details.get('region') if details else None,
                "ISP": details.get('org') if details else None,
                "content_load_time": load_time,
                "status": execution_status
            },
            "dns_query_result": current_ips
        }

        print("\nExecution Result:")
        print(json.dumps(execution_detail, indent=2))
        print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
