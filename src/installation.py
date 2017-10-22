import os
print "\nEnter your BITS ID [Eg: f2016015]"
email = raw_input()
if ('@' not in email):
    email = email + '@pilani.bits-pilani.ac.in'
print "Enter your Nalanda Password"
pwd = raw_input()
print "Enter the path to store the lecture slides [Refer to readme]"
path = raw_input()
config_path = os.path.join(
    os.path.expanduser('~'),
     '.termi-nalanda/config.txt')
path = os.path.join(os.path.expanduser('~'),path)
f = open(config_path, 'w')
config = email + '\n' + pwd + '\n' + path
f.write(config)
f.close()
