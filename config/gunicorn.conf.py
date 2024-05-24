import os

if not os.path.exists('.log'):
    os.makedirs('.log')

accesslog = '.log/access.log'
errorlog = '.log/error.log'
loglevel = 'info'
