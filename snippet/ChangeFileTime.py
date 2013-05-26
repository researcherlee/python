'''
Change mtime and atime for all files in current directory to "2011-01-01 13:00"
'''
import time, os

# get 2011-01-01 13:00
newtime = time.mktime((2011, 1, 1, 13, 0, 0, 0, 0, 0))


for f in os.listdir('.'):
    
    # modify atime and mtime
    f.utime(f, (newtime, newtime))
    
    # show result
    print os.stat(f)
    # exepcted result like that
    # nt.stat_result(st_mode=16895, st_ino=0L, st_dev=0, st_nlink=0, st_uid=0, st_gid=0, st_size=4096L
    #                st_atime=1360672233L, st_mtime.., st_ctime...)







