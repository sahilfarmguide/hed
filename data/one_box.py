from boto.s3.connection import S3Connection;
from boto.s3.key import Key;
import os;
import shutil

key_id = 'AKIAIDJDXTYTWWLZY5EA';
secret = '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';
scraper_bkt = 'usscrapperimages1';
box = "92ee8b64-c75d-11e6-b349-02adcd2575fd";

if os.path.exists(box):
    shutil.rmtree(box)
os.makedirs(box+'/original/');
shutil.copyfile('detect_edges.py', box+'/detect_edges.py')
shutil.copyfile('index_images.py', box+'/index_images.py')

bconn = S3Connection(key_id, secret);
bucket = bconn.get_bucket(scraper_bkt);
img_list = bucket.list(box+"/", "");
for img in img_list:
    img_contents = img.name.split('/')
    dir_name = img_contents[0]
    file_name = img_contents[1]
    file_path = dir_name+'/original/'+file_name
    img.get_contents_to_filename(file_path)
