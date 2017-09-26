print "\nPlease enter your BITS ID [Eg: f2016015]"
email = raw_input()
if ('@' not in email):
    email = email + '@pilani.bits-pilani.ac.in'
print "Please enter your Nalanda Password"
pwd = raw_input()
print "Please enter the 'complete' path to where the slides must be stored"
path = raw_input()
f = open('credentials.txt','w')
f.write(email+'\n')
f.write(pwd+'\n')
f.write(path)