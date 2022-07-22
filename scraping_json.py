from bs4 import BeautifulSoup
import requests
import json

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def get_soup(url):
    req = requests.get(url)
    return BeautifulSoup(req.text, "html.parser")

def get_vendor_device(url):
    print('\n========== fetching from URL',url,'==========\n')
    soup = get_soup(url)
    table = soup.find('tbody')
    trs = table.find_all('tr')
    l = len(trs)

    vendors = {}
    devices = {}
    for i,tr in enumerate(trs):
        printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete')
        tds = tr.find_all('td')
        vendors[tds[0].text.strip()] = tds[1].text

        exdend_url = tds[0].find('a')['href']
        redirect_url = base_url + exdend_url
        redirect_soup = get_soup(redirect_url)
        device_table = redirect_soup.find("div", {"class": "search-results"}).find('table')
        if device_table is not None:
            tb_trs = device_table.find('tbody').find_all('tr')
            for tb_tr in tb_trs:
                tb_tds = tb_tr.find_all('td')
                devices[tb_tds[3].text.strip()] = tb_tds[4].text.strip()

    return vendors,devices

if __name__=='__main__':

    base_url = "https://devicehunt.com"
    url_usb = base_url+"/all-usb-vendors"
    url_pci = base_url+"/all-pci-vendors"

    usb_vendors, usb_devices =  get_vendor_device(url_usb)
    pci_vendors, pci_devices =  get_vendor_device(url_pci)

    with open("usb_vendor_data.json", "w") as outfile:
        json.dump(usb_vendors, outfile)
    with open("pci_vendor_data.json", "w") as outfile:
        json.dump(pci_vendors, outfile)
    with open("usb_device_data.json", "w") as outfile:
        json.dump(usb_devices, outfile) 
    with open("pci_device_data.json", "w") as outfile:
        json.dump(pci_devices, outfile)

    

