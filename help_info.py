ctf_help = '''
`!ctf create CTF_NAME`
create a category and role for a ctf (must have permissions to manage channels)*
`!ctf end`
archives the ctf.
`!ctf join CTF_NAME`
give the user the ctf_role **use this command in the ctfhall channel**
`!ctf leave CTF_NAME`
remove the ctf_role from user **use this command in the ctfhall channel**
`!ctf setcreds [username] [password]`
pin the message of ctf credentials, can be fetched by the users later with `!ctf show creds` command.
`!ctf event CTFTIME_URL (--pin)(--countdown)[optional]`
shows the info of the event. use the --pin option to pin the info and create a start and end live timer --countdown option to create a static start timer. if using the --pin option Recommended to use it in the ctf channel.
`!ctf attempt CHALLENGE_NAME`
create a channel and a role with the challenge_name. other players attempting the same challenge will have access to the channel. **use this command in the ctf main room channel**
`!ctf note MSG`
pins the msg in the channel which can later be viewed by other players with `!ctf show note` command. **use this inside the challenge channel assigned**
`!ctf solved (--freeze)[optional](channel_name)[Default=current_channel]`
marks the challenge as solved. If --freeze option is specified then the send_message access will be reboked. [Default] Delete the channel (Recommended). **use this command inside the challenge channel assigned.**
`!ctf show creds`
gets the credentials from the pinned message.
`!ctf show note`
gets the notes pinned in the channel.
`!ctf show [info/event]`
gets the info of the event.
'''

pwn_help = '''
`!pwn syscall <arch> <syscall name / syscall number>`
shows the syscall info for the args specified [Eg : !pwn syscall x86 execve]
`!pwn magic [md5 hash of libc.so file]`
shows magic output of libc [Eg : !pwn magic e63efc14f34504f4ac4cf7d63ed229ca]
'''

ctfd_help = '''
`!ctfd start <ctf_link_homepage>`
live scoreboard countdown of ctfd
'''

help_page = '''
`!ping`
proves that bot is not actually dead
`!tic`
play a tic tac toe game
`!help ctf`
info for all ctf commands
`!help pwn`
info for all pwn commands
`!ping`
try it out and thank me later :))
`!ask (question) (--all)[optional]`
gets you the answer of the question from *_stackoverflow_* with --all option you get a detailed answer
'''