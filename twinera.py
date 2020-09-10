# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 21:21:28 2020

@author: jedraynes

High-level:
The following script will send a pre-defined direct message to the user-defined recipient. It was originally made to automate the daily direct messages sent by @jedraynes to @panerabread to bring back the original chipotle chicken panini.
"""

'''
ITEMS TO ADD~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- ensure the last dm we sent at least yesterday
'''

# import the necessary packages
import tweepy
import sys

# define the api keys
consumer_key = 'h18SDZ7w3KYPCWS60Bwd3VpLB'
consumer_secret = '9h6WMc5bZINDeAORmaqYd7YB6eQgUWKdSVxzyx5AxCWLkkJ3tT'
# bearer_token = 'AAAAAAAAAAAAAAAAAAAAACY8HgEAAAAAodYfttgLZE2mhLw9ajLF7JfUvtk%3D8KibYHFUg09TjalaIo7I0KpC2Ec04zUoONZ3UYO3nAbCADQBnn'
access_token_key = '569519591-zX6JfeuGkmdrZuyyWSIJIIB6jxMBYoteo3V8WFjb'
access_token_secret = 'gBViXTLIwZxTuWuuLY8j55aqBZ34iMMrK0veCQOhAC4T6'

# initiate the api
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
api = tweepy.API(auth)

# define the recipient
def define_recipient():
    try:
        screen_name = str(input('Enter the recipient\'s screen name: '))
        user = api.get_user(screen_name)
        recipient_id = user.id_str
    except:
        print('An exception has occurred. User not found or has been suspended. Exiting...')
        sys.exit()
    return recipient_id

def get_correct_dm(recipient_id):
    list_of_dms = api.list_direct_messages(50)
    for x in range(0,len(list_of_dms)):
        if list_of_dms[x].message_create['target']['recipient_id'] == recipient_id:
            correct_dm = list_of_dms[x]
            break
        else:
            print('Correct DM not found. Trying...')
    try:
        return correct_dm
    except:
        print('An exception has occurred. The correct DM was not found. Exiting...')
        sys.exit()

# get yesterday's counter number
def get_yesterdays_number(recipient_id): 
    correct_dm = get_correct_dm(recipient_id)
    dm_text = correct_dm.message_create['message_data']['text']
    try:
        yesterdays_number = [int(char) for char in dm_text.split() if char.isdigit()][0]
        print('\n' + 'Yesterday\'s number was: {}.'.format(yesterdays_number))
    except:
        print('\n' + 'An exception occurred. The text parsed was not an integer. Exiting...')
        sys.exit()
    return yesterdays_number

# set the counter and nessage
def set_counter_and_message(recipient_id):
    yesterdays_number = get_yesterdays_number(recipient_id)
    counter = yesterdays_number + 1
    # counter = int(input('Enter the day\'s counter: '))
    print('The next number is: {}.'.format(counter))
    message = str(counter) + '\n' + '\n' + 'http://chipotlechickenpanini.com/'
    return message

# send the DM
def send_dm(recipient_id, message):
   api.send_direct_message(recipient_id, message)
   return

# main code
def main():
    recipient_id = define_recipient()
    message = set_counter_and_message(recipient_id)
    recipient_screen_name = api.get_user(recipient_id).screen_name
    print('\n' + 'The recipient\'s screen name is: @{}.'.format(recipient_screen_name))
    print('\n' + 'The message to be sent is:' + '\n' + '\n' + message)
    confirm = input('Confirm? y/n: ')
    if confirm == 'y':
        send_dm(recipient_id, message)
    else:
        print('Script canceled. Exiting...')
        sys.exit()
    return

# run the program
if __name__ == '__main__':
    main()