# gunicorn config file

pidfile = '/home/vagrant/nsextremeweb/gunicorn.pid'
debug = True
#proc_name = 'nsextremeweb' # requires setproctitle module to be installed
workers = 2
bind = '0.0.0.0:8001'
logfile = '/home/vagrant/nsextremeweb/gunicorn.log'
loglevel = 'debug'
