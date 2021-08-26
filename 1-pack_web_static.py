#!/usr/bin/python3
""" generates a .gtz archive from the contents of the web_static folder of
    AirBnB repo """

from fabric.operations import local
from datetime import datetime


def do_pack():
    """ This function compresses files """
    local("mkdir -p versions")
    tar_result = local("tar -cvzf versions/web_static_{}.tgz web_static".format
                       (datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")),
                       capture=True)

    if tar_result.failed:
        return None
    return tar_result
