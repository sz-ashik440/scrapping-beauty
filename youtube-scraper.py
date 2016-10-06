import requests, os, sys
from pathlib import Path
from bs4 import BeautifulSoup

def get_all_link(soup):
    """
    Return all of the link atrribute
    
    keyword arguments:
    soup -- soup from where link will extract 
    """
    
    link_str = set()
    
    for link in soup.find_all('a'):
        #link_str+=link.get('href')+'\n'
        link_str.add(link.get('href'))
        
    return '\n'.join(link_str)


def get_soup(url, data_type=''):
    """
    make soup using BeautifulSoup
    
    Keyword arguments:
    url -- url to make soup
    """
    
    
    request_data = requests.get(url)
    #html_text = request_data.text
    return BeautifulSoup(request_data.text, 'lxml')
    

def write_to_file(file_name, data):
    """
    write to a file if file not exist make a file on that directory
    
    keyword arguments:
    file_name -- The absulute file Path
    data      -- Data which will be stored into file
    """
    
    
    if not os.path.isfile(file_path):
        file_Data = open(file_path, 'w')
        file_Data.write('')
        file_Data.close()
    else:
        file_Data = open(file_path, 'w')
        file_Data.write(data)
        file_Data.close()
        

def read_file_and_print(file_name):
    """
    this to read the file
    
    file_name -- The absulute file Path
    """
    read_file = open(file_path, 'r')
    result_str = read_file.read()
    read_file.close()
    print(result_str)


if __name__ == '__main__':
    this_url = "https://www.youtube.com/watch?v=4VbuBcNCgAc"
    if len(sys.argv)>1:
        this_url = sys.argv[1]
    # this is for storing data into file
    file_path = os.getcwd() + '/scrap.txt'
    #write_to_file(file_path, 'Try this os test')
    
    soup = get_soup(this_url)
    
    
    """
    This is for link extraction and save into a file
    
    link = get_all_link(soup)    
    print(link)
    
    #write_to_file(file_path, link)
    #print(soup.prettify()
    """
    
    # get title
    print('Ttile: {0}'.format(soup.find('span', id='eow-title').contents[0].strip()))
    
    # get total view count
    print('Total View: {0}'.format(soup.find('div', class_='watch-view-count').contents[0].strip()))
    
    # get youtube channel name
    print('Channel: {0}'.format(soup.find('div', ['yt-user-info']).a.text))
    
    # get upvote and downvote count
    print('Up Voted: {0}'.format(soup.find('button', ["like-button-renderer-like-button"]).contents[0].text))
    print('Down Voted: {0}'.format(soup.find('button', ["like-button-renderer-dislike-button-unclicked"]).contents[0].text))
    
    #Publish date
    
    print(soup.find('div', id='watch-uploader-info').strong.text)
    #[[FAILD]] get video duration
    #print(soup.find('span', class_='ytp-time-duration'))
    
    