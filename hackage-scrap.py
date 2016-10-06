import requests, re
from bs4 import BeautifulSoup

class HaskPackage:
    def __init__(self, pk_name=''):
        self.pk_name = pk_name
        self.pk_url = ''
        self.pk_maintainer_name = []
        self.pk_maintainer_email = []
        self.pk_github_url = ''
        self.pk_github_star = 0
        
    def set_pk_url(self, url):
        self.pk_url = url
        
def get_soup(url):
    """
    make soup using BeautifulSoup
    
    Keyword arguments:
    url -- url to make soup
    """
    
    try:
        request_data = requests.get(url)
        #print('url: '+url)
        #print(request_data.status_code)
        #html_text = request_data.text
        return BeautifulSoup(request_data.text, 'lxml')
        
    except Exception:
        return 'You have massed with URL'

if __name__ == '__main__':
    base_url = 'https://hackage.haskell.org'
    
    soup = get_soup(base_url+'/packages/top')
    
    table_content = soup.find('table').contents
    
    table_content = table_content[1:]
    
    # a list of HaskPackage object 
    package_info = []
    
    for row in table_content:
        data_obj = HaskPackage()
        data = row.find_all('td')
        if int(data[1].text.strip()) > 100:
            #print(data[0].find('a').get('href')+' '+ data[1].text)
            data_obj.pk_url = base_url+data[0].find('a').get('href')
            package_info.append(data_obj)
            
    for i in package_info:
        soup = get_soup(i.pk_url)
        i.pk_name = soup.h1.text.split(' ')[1]
        print('Package Name: '+ i.pk_name)
        #print('Maintainer: {0}\n'.format(soup.find(text='Maintainer').parent.parent.find('td').text))
        #maintainer_list = soup.find(text='Maintainer').parent.parent.find('td').text
        # maintainer_dic = {}
        # for item in maintainer_list:
        #     single_maintainer = item.split(',')
        
        maintainer_list = soup.find(text='Maintainer').parent.parent.find('td').text.strip().split(',')

        anguler_brac_re = re.compile(r'[<\(].*[>\)]')
        email_re = re.compile(r'[a-zA-Z0-9._%+-]+@[a-z]+(\.[a-zA-Z]{2,4})')
        #print(anguler_brac_re.sub(r'', row_list[0]).strip())
        #print(email_re.search(row_list[0]).group())
        for row in maintainer_list:
            if not anguler_brac_re.search(row):
                if email_re.search(row):
                    i.pk_maintainer_name.append('N/A')
                    i.pk_maintainer_email.append(email_re.search(row).group().strip())
                    # email.append(email_re.search(row).group().strip())
                    # name.append('N/A')
                else:
                    i.pk_maintainer_name.append(str(row).strip())
                    i.pk_maintainer_email.append('N/A')
                    # name.append(str(row).strip())
                    # email.append('N/A')
            else:
                if len(anguler_brac_re.sub(r'', row).strip())==0:
                    #name.append('N/A')
                    i.pk_maintainer_name.append('N/A')
                else:
                    #name.append(anguler_brac_re.sub(r'', row).strip())
                    i.pk_maintainer_name.append(anguler_brac_re.sub(r'', row).strip())
                #email.append(anguler_brac_re.search(row).group().strip()[1:-1].strip())
                i.pk_maintainer_email.append(anguler_brac_re.search(row).group().strip()[1:-1].strip())
        try:        
            raw_git_link = ''
            if soup.find(text='Source repository'):
                raw_git_link = soup.find(text='Source repository').parent.parent.find('a').get('href')
            else:
                raw_git_link = soup.find(text='Home page').parent.parent.find('a').get('href')
            
            git_link_fix_re = re.compile(r'^(git://)[a-zA-Z0-9-@:%._\+~#=/]*')
            if git_link_fix_re.search(raw_git_link):
                raw_git_link = raw_git_link.replace('git://', 'https://')
            # remove_trailinggit_re = re.compile(r'.*(.git)$') 
            # if remove_trailinggit_re.search(raw_git_link.strip()):
            #     raw_git_link.replace('.git', '')
            #     print('boom')
            print(raw_git_link)
            # raw_git_link = raw_git_link.replace('.git', ' ')
            # git_repo_re = re.compile(r'(?:https|git)://[a-zA-Z0-9-@:%._\+~#=]{2,256}.com/.*')
            
            # print(git_repo_re.findall(raw_git_link)[0].split(' '))
            
            print(i.pk_maintainer_name)
            print(i.pk_maintainer_email)
            #print('\n')
            
            git_soup = get_soup(raw_git_link.strip())
        
            git_star = git_soup.find_all('a', ['social-count', 'js-social-count'])[1].text.strip()
            print('Git-hub star: {0}\n'.format(git_star))
        except Exception:
            print('Git repo not found.\n')
            
#li = []
# for i in range(1,10):
#     obj = HaskPackage(chr(65+i))
#     name = 'sz ashik, mitul islam'
#     obj.pk_maintainer_name.extend([s.strip() for s in name.split(',')])
#     li.append(obj)
    
# li[1].pk_name = 'something new'
# for i in li:
#     print(i.pk_maintainer_name)

# name = []
# email = []

# str_test_1 = 'sz ashik <szashik@gmail.com>, mitul islam <mitul.islam@gmail.com>'
# str_test_2 = '<szashik@gmail.com>, <mitul@gmail.com > '
# str_test_3 = 'sz ashik, mitul islam'

# row_list = str_test_2.strip().split(',')

# anguler_brac_re = re.compile(r'<.*?>')
# email_re = re.compile(r'[a-zA-Z0-9._%+-]+@[a-z]+(\.[a-zA-Z]{2,4})')
# #print(anguler_brac_re.sub(r'', row_list[0]).strip())
# #print(email_re.search(row_list[0]).group())
# for row in row_list:
#     if not anguler_brac_re.search(row):
#         if email_re.search(row):
#             email.append(email_re.search(row).group().strip())
#             name.append('N/A')
#         else:
#             name.append(str(row).strip())
#             email.append('N/A')
#     else:
#         if len(anguler_brac_re.sub(r'', row).strip())==0:
#             name.append('N/A')
#         else:
#             name.append(anguler_brac_re.sub(r'', row).strip())
#         email.append(anguler_brac_re.search(row).group().strip()[1:-1].strip())
    
# print(name)
# print(email)
    
    