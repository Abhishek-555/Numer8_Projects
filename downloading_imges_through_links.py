import urllib.request
import random



def dl_img(url,file_path , file_name):
    full_path=('E:/images_output/download/'+ file_name + '.jpg')
    urllib.request.urlretrieve(url,full_path)

url=input('Enter the url:')
file_name=input('Enter the file name:')

dl_img(url,'download/',file_name)