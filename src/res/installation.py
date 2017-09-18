print "\nPlease enter your BITS Mail"
email = raw_input()
print "Please enter your Nalanda Password"
pwd = raw_input()
print "Please enter the complete path to the location where the lecture slides must be stored"
path = raw_input()
f = open('credentials.txt','w')
f.write(email+'\n')
f.write(pwd+'\n')
f.write(path)