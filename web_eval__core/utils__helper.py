import os
from settings import *

def get_ip_from_request (request):
    return request.META['REMOTE_ADDR']
    
    
def save_file (dest, file):
    destination = open(dest, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
    

def pygments_standardize (value):
    if value == 'pike':
        return 'cpp'
    if value == 'cs':
        return 'c#'
    if value == 'ml':
        return 'ocaml'
    return value

def copy_initial_avatar (username):
    sample = os.path.join(AVATARS_DIR, "sample.png")
    prefix = os.path.join(AVATARS_DIR, "%s_" % username.username)
    os.system("convert %s %s" % (sample, prefix + "normal.jpeg"))
    os.system("convert %s -resize 150^ -gravity Center -crop 150x150+0+0 +repage %s" % (prefix + "normal.jpeg", prefix + "medium.jpeg"))
    os.system("convert %s -resize 50^ -gravity Center -crop 50x50+0+0 +repage %s" % (prefix + "normal.jpeg", prefix + "small.jpeg"))
    os.system("convert %s -resize 16x16^ -gravity Center -crop 16x16+0+0 +repage %s" % (prefix + "normal.jpeg", prefix + "tiny.jpeg"))
    os.system("convert %s -resize 100 %s" % (prefix + "normal.jpeg", prefix + "100px.jpeg"))
