#!/usr/bin/python3
# A Fabric script that generates a .tgz archive from the contents of the
# web_static folder of your AirBnB Clone repo, using the function do_pack

from fabric.api import local
from datetime import datetime
from os.path import getsize


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder"""

    t_now = datetime.now()
    time = t_now.strftime('%Y%m%d%H%M%S')
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static".format(time))

        f_path = 'versions/web_static_{}.tgz'.format(time)
        f_size = getsize('versions/web_static_{}.tgz'.format(time))
        print("web_static packed: versions/web_static_{}.tgz -> {}Bytes"
                .format(time, f_size))
        return f_size

    except Exception as e:
        return None
