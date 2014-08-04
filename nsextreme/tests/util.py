import os
import sys
import hashlib
import shutil
from functools import wraps
from nose.tools import make_decorator
from nsextreme import tests
from nsextreme.video import effects

snapshot_dir = os.path.join(os.path.dirname(tests.__file__), 'snapshots')
json_data_path = os.path.join(os.path.dirname(__file__), 'testdata_new.json')


def movie_path(scenario):
    return os.path.join(os.path.dirname(tests.__file__),
                        'videos/%s.mov' % scenario)


# from: http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()


def prompt_compare(snapshot_mov_filename, snapshot_md5_filename, filename):
    # if not open the video using the player
    # TODO: make platform agnostic
    os.system("open %s" % filename)
    os.system("open %s" % snapshot_mov_filename)
    # warn if it's rotated
    try:
        rotation = effects.get_rotation(filename)
        print "snapshot: rotation is", rotation
    except:
        pass
    # and ask if it looks OK?
    ok = query_yes_no("snapshot: New/changed snapshot. Is the video ok?")
    if ok:
        # if so save the filesize, and md5 of the file
        md5 = md5sum(filename)
        print "snapshot: Using md5sum: %s" % md5
        with open(snapshot_md5_filename, 'w') as snapshot_md5_file:
            snapshot_md5_file.write(md5)
        shutil.copyfile(filename, snapshot_mov_filename)
    else:
        raise Exception("snapshot: not accepted")


def snapshot(f):
    "Takes an MD5 snapshot of video for test acceptance"
    @wraps(f)
    def wrapper(*args, **kwargs):
        filename = f(*args, **kwargs)
        snapshot_name = f.func_name
        print "snapshot:", snapshot_name
        snapshot_filename = os.path.join(snapshot_dir, snapshot_name)
        snapshot_md5_filename = snapshot_filename + '.md5'
        snapshot_mov_filename = snapshot_filename + '.mov'
        # Do we have an existing snapshot in snapshots directory?
        if not os.path.exists(snapshot_md5_filename):
            prompt_compare(snapshot_mov_filename, snapshot_md5_filename,
                           filename)
        else:
            # otherwise we have a snapshot
            sample_md5 = md5sum(filename)
            snapshot_md5 = file(snapshot_md5_filename).read()
            if sample_md5 == snapshot_md5:
                print "snapshot: success, they are the same!"
            else:
                prompt_compare(snapshot_mov_filename,
                               snapshot_md5_filename, filename)
        if os.path.exists(filename):
            print "snapshot: removing", filename
            os.remove(filename)
    wrapper = make_decorator(f)(wrapper)
    return wrapper
