networking_commands = {
'file_prompt': ['configure terminal',
    'file prompt quiet',
    'exit'],
'tracelong_commands': [
    "request platform software trace rotate all",
    "request platform software trace slot rp active archive target bootflash:",
    "request platform software trace slot rp standby archive target stby-bootflash:"
    ],
'tracelogs_archieve': [
    "archive tar /create tftp://135.21.42.90/AXAYSCRIPT_Tracelog.tar bootflash:/tracelogs"
    ],
'username': 'cisco15',
'file_un_prompt': ['configure terminal',
        'no file prompt quiet',
        'exit'],
'router_ip': ['135.25.14.91', '135.25.14.92', '135.25.14.93', '135.25.14.94', '135.25.14.95', '135.25.14.96',
              '135.25.14.97', '135.25.14.98', '135.25.14.99', '135.25.14.100', '135.25.14.101', '135.25.14.102',
              '135.25.14.103', '135.25.14.104', '135.25.14.105',
              '135.25.14.106', '135.25.14.107', '135.25.14.154', '135.25.14.155', '135.25.14.156']
}


def get_commands(command_set):
    return networking_commands.get(command_set, [])
