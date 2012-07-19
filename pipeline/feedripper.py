import sys,os,os.path,shutil
from util.coroutine import coroutine
from util.colors import	blue,green,warn,fail
from pipeline.maps import VipRM
from pipeline.maps import VipBulkRM
from deploy.database import connection
import logging,csv
from vip.vave.feed_destructor.feed_to_flatfiles import FeedToFlatFiles
from deploy.conf.fieldnames import vip_to_bip_names
from deploy.conf import settings





def fieldname(ename,fieldname):
    new_fieldname = vip_to_bip_names['%s.%s' % (ename,fieldname)]
    return new_fieldname if new_fieldname != None else fieldname

def flip_file(path):
    """
        Modifies csv headers to reflect BIP field names 
    """
    temp_path = path + '.headertransformed'
    fdir,fname = os.path.split(path)
    entity_name = fname.replace('.txt',''	)
    in_file = open(path)
    out_file = open(temp_path,'w')
    old_header= in_file.readline().strip().split(',')
    new_header = [fieldname(entity_name,x) for x in old_header]
    out_file.write(','.join(new_header) + '\n')
    for line in in_file:
        out_file.write(line)
    in_file.close()
    out_file.close()
    os.remove(path)
    shutil.move(temp_path,path)



@coroutine
def do_viacsv():
    """
    Coroutine that takes references to a vip feed file and inserts it into the database. 
    Should be configurable to run under multiple processes.
    """
    try:
        while True:
            rel_path = (yield)
            print "Ripping %s..." % rel_path
            #file operations
            abs_path = os.path.abspath(rel_path)
            local_root,fname = os.path.split(abs_path)
            csv_root = os.path.join(local_root,'%s.flattened' % fname)
            csv_file_paths = [os.path.join(csv_root,fname) for fname in os.listdir(csv_root)]
            if not os.path.isdir(csv_root) or not settings.CACHE_FLATTENING:
                if os.path.isdir(csv_root):
                    shutil.rmtree(csv_root)
                os.mkdir(csv_root)
                ftff = FeedToFlatFiles(csv_root)
                ftff.process_feed(abs_path)
                for fpath in csv_file_paths:
                    flip_file(fpath)
            else:
                print '%s: Skipping flattening' % "Files exist" if os.path.isdir(csv_root) else "Files cached"
            #iterating through all data
            cursor = connection().cursor()
            vrm = VipRM(cursor)
            for fpath in csv_file_paths:
                fdir,fname = os.path.split(fpath)
                entity_name = fname.replace('.txt','')
                insert_func = vrm.get_mapper(entity_name)
                for data in csv.DictReader(open(fpath)):
                    #push record to database
                    logging.info((blue(entity_name),warn(data)))
                    result = insert_func(data)
    except GeneratorExit:
        vrm.flush()
        pass

@coroutine
def do_viabulkcsv():
    """
    Coroutine that takes references to a vip feed file and inserts it into the database. 
    Should be configurable to run under multiple processes.
    """
    try:
        while True:
            rel_path = (yield)
            print "Ripping %s..." % rel_path
            #file operations
            abs_path = os.path.abspath(rel_path)
            local_root,fname = os.path.split(abs_path)
            csv_root = os.path.join(local_root,'%s.flattened' % fname)
            csv_file_paths = [os.path.join(csv_root,fname) for fname in os.listdir(csv_root)]
            if not os.path.isdir(csv_root) or not settings.CACHE_FLATTENING:
                if os.path.isdir(csv_root):
                    shutil.rmtree(csv_root)
                os.mkdir(csv_root)
                ftff = FeedToFlatFiles(csv_root)
                ftff.process_feed(abs_path)
                for fpath in csv_file_paths:
                    flip_file(fpath)
            else:
                print '%s: Skipping flattening' % "Files exist" if os.path.isdir(csv_root) else "Files cached"
            #iterating through all data
            cursor = connection().cursor()
            vrm = VipBulkRM(cursor)
            for fpath in csv_file_paths:
                fdir,fname = os.path.split(fpath)
                entity_name = fname.replace('.txt','')
                vrm.get_mapper(entity_name)(fpath,entity_name)
    except GeneratorExit:
        pass


def main():
    """
        Module must be run from manage.py. 
    """
    fnames = (os.path.abspath(x) for x in sys.argv[1:])
    ripper = do_expat()
    for fname in fnames:
        ripper.send(fname)
    


