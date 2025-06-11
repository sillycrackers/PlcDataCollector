import re
import os



def check_valid_ip(ip):

    ipv4_pattern = r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$'

    if re.match(ipv4_pattern, ip):
        return True
    else:
        return False

def check_valid_tag_list(tag_list):

    for tag in tag_list:
        if not check_valid_tag(tag):
            return False

    return True

def check_valid_specific_time(hour, minute):

    if not hour.isdigit():
        return False
    if not minute.isdigit():
        return False

    if int(hour) > 23 or int(hour) < 0:
        return False

    if int(minute) > 59 or int(minute) < 0:
        return False

    return True

def check_valid_interval_start_time(hour, minute):

    if not hour.isdigit():
        return False
    if not minute.isdigit():
        return False

    if int(hour) > 23 or int(hour) < 0:
        return False

    if int(minute) > 59 or int(minute) < 0:
        return False

    return True

def check_valid_tag(tag):

    if len(tag) == 0:
        return False

    if tag[0].isdigit():
        return False

    for i in range(len(tag)):

        if not i == len(tag)-1:

            if tag[i] == '_' and tag[i + 1] == '_':
                return False

            elif not tag[i].isalnum():
                if tag[i] != '_' and tag[i] != '.' and tag[i] != "[" and tag[i] != "]":
                    return False
        else:
            break

    return True

def check_valid_name(name):

    if len(name) == 0:
        return False
    elif len(name) > 30:
        return False
    elif name == "Add New PLC...":
        return False
    else:
        return True

def check_valid_file_name(name):

    valid_file_name_pattern = r"^[\w\-.]+$"

    if re.match(valid_file_name_pattern,name) and len(name) < 100:
        return True
    else:
        return False

def check_valid_file_location(file_dir):

    if os.path.isdir(file_dir):
        return True
    else:
        return False

