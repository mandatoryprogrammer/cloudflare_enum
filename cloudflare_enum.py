#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created using Metafidv2 by Matthew Bryant (mandatory)
# Unauthorized use is stricly prohibited, please contact mandatory@gmail.com with questions/commentself.s.
import requests
import time
import json
import sys
import csv
import os
from bs4 import BeautifulSoup

class cloudflare_enum:
    def __init__( self, username, password ):
        # Show non-essential output
        self.verbose = True

        # Show sexy banner
        self.print_banner()

        # Master list of headers to be used in each connection
        self.global_headers = {
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Host': 'www.cloudflare.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0',
        }

        # Dictionary of parsed values 
        self.parse_dict = {}

        self.username = username
        self.password = password

        self.s = requests.Session()
        self.s.headers.update( self.global_headers )

    def log_in( self ):
        # Log the user in to Cloudflare
        r = self.s.get('https://www.cloudflare.com/login', )
        form_soup = BeautifulSoup( r.text ).findAll( 'form' )
        self.parse_dict[ 'security_token_0' ] = form_soup[0].find( attrs={'name': 'security_token'} )['value'] 
        self.parse_dict[ 'act_0' ] = form_soup[0].find( attrs={'name': 'act'} )['value'] 

        self.statusmsg( "Logging in to Cloudflare..." )

        post_data = {
            'login_email': self.username,
            'login_pass': self.password,
            'security_token': self.parse_dict[ 'security_token_0' ],
            'act': self.parse_dict[ 'act_0' ],
        }
        new_headers = {
            'Referer': 'https://www.cloudflare.com/login',
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.post('https://www.cloudflare.com/login', data=post_data)

        if "You are logged in as " in r.text:
            self.successmsg( "Login was successful!" )
            return True
        else:
            self.errormsg( "Login failed!" )
            return False

    def find_between_r( self, s, first, last ):
        try:
            start = s.rindex( first ) + len( first )
            end = s.rindex( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def find_between( s, first, last ):
        try:
            start = s.index( first ) + len( first )
            end = s.index( last, start )
            return s[start:end]
        except ValueError:
            return ""

    def pprint( self, input_dict ):
        print json.dumps(input_dict, sort_keys=True, indent=4, separators=(',', ': '))

    def print_banner( self ):
        if self.verbose:
            print """
            
                                                     `..--------..`                               
                                                 .-:///::------::///:.`                           
                                              `-//:-.`````````````.-://:.`    `   `               
                                            .://-.```````````````````.-://-`  :  `-   .           
                                          `-//:.........................-://. /. -: `:`  ``       
                                         `://--------:::://////:::--------://-::.::`:- .:.        
                              ``.---..` `///::::::///////////////////:::::::///::::::--:.`.-.     
                            .://::::///::///::///////////////////////////:::///:-----::--:-`  `    
                          `:/:-...--:://////////////////////////////////////////----------.--.`    
                         `:/:..-:://////////////////////////////////////////////-----------.````    
                         .//-::////////////////////////////////////:::::////////-...--------...`    
                         -/////////////////////////////////////////////::::----:. `.-::::::-..``    
                    ``.--:////////////////////////////////////////////////::-..```-///::::///:-`    
                 `.:///::::://////////////////////////////////////:::::::::::::::-----......-:/:.    
               `-//:-----::::://///////////////////////////////:///////////////////:-::::---..-//:`    
              `:/:---://+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//+++//::--//:    
             `//:-/+oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo+++oooo+//://.    
             :///ossssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssosssssso+//:    
            `//+sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss+/-    
            `//+ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo+++++/.    
             ``````````````````````````````````````````````````````````````````````````````````````     
                                                             Cloudflare DNS Enumeration Tool V1.1
                                                                                    By mandatory
        """

    def statusmsg( self, msg ):
        if self.verbose:
            print "[ STATUS ] " + msg

    def errormsg( self, msg ):
        if self.verbose:
            print "[ ERROR ] " + msg

    def successmsg( self, msg ):
        if self.verbose:
            print "[ SUCCESS ] " + msg

    def add_domain( self, domain ):
        self.statusmsg( 'Adding domain to Cloudflare...' )
        new_headers = {
            'Referer': 'https://www.cloudflare.com/login',
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.get('https://www.cloudflare.com/my-websites', )
        self.atok = self.find_between_r( r.text, '"login":true,"atok":"', '","in_www_next_beta"' ) # http://xkcd.com/292/

        get_data = {
            'sort': 'zone_statuself.s.asc',
            'atok': self.atok,
            'o': '0',
        }
        new_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.cloudflare.com/my-websites',
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.get('https://www.cloudflare.com/api/v2/zone/load_multi', params=get_data)

        get_data = {
            'atok': self.atok,
        }
        new_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.cloudflare.com/my-websites',
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.get('https://www.cloudflare.com/api/v2/zone/load_index', params=get_data)

        get_data = {
            'atok': self.atok,
            'z': domain,
        }
        new_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.cloudflare.com/my-websites',
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.get('https://www.cloudflare.com/api/v2/zone/init', params=get_data)
        init_result = json.loads( r.text )
        
        if init_result['result'] == "error":
            self.errormsg( "Cloudflare returned an error with the message: '" + init_result['msg'] + "'" )
            return False
        else:
            return True

    def get_domain_dns( self, domain ):
        self.successmsg( "Querying Cloudflare DNS archives..." )
        new_headers = {
            'Referer': 'https://www.cloudflare.com/login',
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.get('https://www.cloudflare.com/my-websites', )
        self.atok = self.find_between_r( r.text, '"login":true,"atok":"', '","in_www_next_beta"' ) # http://xkcd.com/292/

        get_data = {
            'atok': self.atok,
            'zsn': 'preset',
            'z': domain,
        }
        new_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.cloudflare.com/my-websites',
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.get('https://www.cloudflare.com/api/v2/zstore/get', params=get_data)
        results = json.loads( r.text )

        if results['result'] == 'success':
            pass
        else:
            self.errormsg( "Something went wrong! Ruh roh!" )
            return False

        get_data = {
            'atok': self.atok,
            'z': domain,
            'act': 'zone_resume',
        }
        new_headers = {
            'Referer': 'https://www.cloudflare.com/my-websites',
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.get('https://www.cloudflare.com/my-websites', params=get_data)
        atok = self.find_between_r( r.text, '"login":true,"atok":"', '"};</script>' ) # http://xkcd.com/292/

        new_headers = {
            'Referer': 'https://www.cloudflare.com/my-websites',
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.get('https://www.cloudflare.com/your-websites-step2', )

        get_data = {
            'atok': self.atok,
            'z': domain,
        }
        new_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.cloudflare.com/your-websites-step2',
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.get('https://www.cloudflare.com/api/v2/rec/load_alerts', params=get_data)

        get_data = {
            'atok': self.atok,
            'z': domain,
        }
        new_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.cloudflare.com/your-websites-step2',
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.get('https://www.cloudflare.com/api/v2/rec/load_all', params=get_data)

        try:
            return_dict = json.loads( r.text )['response']['recs']['objs']

            for record in return_dict:
                print record["type"] + ": " + record["name"] + " -> " + record["content"]
        except:
            print "Unexpected error:", sys.exc_info()[0]

        self.statusmsg( 'Deleting domain from account for cleanup...' )

        get_data = {
            'atok': self.atok,
            'z': domain,
        }
        new_headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.cloudflare.com/your-websites-step2',
        }
        self.s.headers.update( dict( new_headers.items() + self.global_headers.items() ) )
        r = self.s.get('https://www.cloudflare.com/api/v2/zone/delete', params=get_data)

        self.statusmsg( "Deleted the domain from Cloudflare account" )

        return return_dict

    def get_spreadsheet( self, domain ):
        dns_data = self.get_domain_dns( domain )
        filename = domain.replace( ".", "_" ) + ".csv"

        with open( filename, 'wb') as csvfile:
            dns_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            dns_writer.writerow( [ "Name", "Type", "Content" ] )
            for record in dns_data:
                dns_writer.writerow( [ record["name"], record["type"], record["content"] ] )
            
        self.statusmsg( "Spreadsheet created at " + os.getcwd() + "/" + filename )

if __name__ == "__main__":
    if len( sys.argv ) < 3:
        print "Usage: " + sys.argv[0] + " username@email.com password domain.com"
    else:
        cloud = cloudflare_enum( sys.argv[1], sys.argv[2] )
        if cloud.log_in():
            if cloud.add_domain( sys.argv[3] ):
                time.sleep( 20 )
                cloud.get_spreadsheet( sys.argv[3] )
