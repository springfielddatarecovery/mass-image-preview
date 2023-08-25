import math
import os

from PIL import Image
from multiprocessing import Pool
import argparse
from typing import Dict,List,Set,Union,Any
source_dir='/home/baby/Pictures/'
dest_dir='/home/baby/thumbtests/'
thumbnail_width=200
thumbnail_height=200
contact_sheet_width=400
contact_sheet_height=600
padding_between_images=10
ALLOWED_EXTS=['.jpg','.bmp','.jpeg','.png'] # Extensions we try to thumbnail. Note they must be lowercase.
def is_allowed_ext(filename:str):
    for ext in ALLOWED_EXTS:
        if filename.lower().endswith(ext):
            return True
    return False
def make_image_list(search_dir:str)->List[str]:
    return_list=[]
    for root,dirs,files in os.walk(search_dir):
        for file in files:
            if is_allowed_ext(file):
                abs_path=os.path.join(root,file)
                return_list.append(abs_path)
    return return_list
def image_to_thumbnail(abspath:str,width:int,height:int)->Image:
    try:
        image=Image.open(abspath)
        image=image.resize((width,height))
    except Exception as e:
        print('Error loading image {}: {}'.format(abspath,e))
        image=Image.new('RGB',(width,height))
    return image
def make_page(page_dest:str,image_list:List[str]):
    page=Image.new('RGB',(contact_sheet_width,contact_sheet_height),'GRAY')
    x_offset=0
    y_offset=0
    for image in image_list:
        thumbnail=image_to_thumbnail(image,thumbnail_width,thumbnail_height)
        page.paste(thumbnail,(x_offset,y_offset))
        x_offset+=thumbnail_width
        if x_offset+thumbnail_width>contact_sheet_width:
            x_offset=0
            y_offset+=thumbnail_height
        if y_offset>contact_sheet_height:
            print('Error y offset > height this should not happen!. OFF is {} height is {}'.format(y_offset,contact_sheet_height))
    page.save(page_dest)
if __name__ == '__main__':
    # Sanity checks
    if contact_sheet_width<thumbnail_width:
        print('Contact sheet width cannot be < thumbnail width!')
        quit()
    if contact_sheet_height<thumbnail_height:
        print('Contact sheet height cannot be < thumbnail height!')
        quit()
    # Find images
    image_list=make_image_list(source_dir)
    rows_per_page=int(contact_sheet_height/thumbnail_height)
    images_per_row=int(contact_sheet_width/thumbnail_width)
    images_per_column=int(contact_sheet_height/thumbnail_height)
    columns_per_page = int(contact_sheet_width / thumbnail_width)
    images_per_page=rows_per_page*columns_per_page
    print('There will be {} images per page. Each thumb is {}x{} the page is {}x{}'.format(images_per_page,thumbnail_width,thumbnail_height,contact_sheet_width,contact_sheet_height))
    print('That is {} rows per page and {} columns'.format(rows_per_page,columns_per_page))
    print('Each row has {} images, each column has {}'.format(images_per_row,images_per_column))
    total_pages=math.ceil(len(image_list)/images_per_page)

    # Generate thumbnails
    for index in range(0,total_pages):
        start_image=index*images_per_page
        print('Start image is {}'.format(start_image))
        end_image=(index*images_per_page)+images_per_page
        print('End image is {}'.format(end_image))
        page_images=image_list[start_image:end_image]
        page_dest=os.path.join(dest_dir,'{}.jpg'.format(index))
        make_page(page_dest,page_images)


    # Put thumbnails into contact sheets



