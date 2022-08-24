# from artifactory import ArtifactoryPath
import requests
import pprint as pp
import config
import sys, getopt


url      = "https://cloudigart.jfrog.io/artifactory"

# clears out unwanted noise
poplist =[
    'disableUIAccess',
    'internalPasswordDisabled',
    'lastLoggedIn',
    'lastLoggedInMillis',
    'mfaStatus',
    'offlineMode',
    'policyManager',
    'profileUpdatable',
    'reportsManager',
    'watchManager'
]

def get_usernames():
    usernames = []
    results = requests.get(url + "/api/security/users", auth=(config.login_name, config.apitoken))
    user_data = results.json()
    for data in user_data:
        usernames.append(data['name'])
    return usernames


def add_user(data):
    payload = {'name': data['username'], 'email': data['email'], 'password': data['password'], 'groups': data['groups']}
    results = requests.put(url + "/api/security/users/" + data['username'], auth=(config.login_name, config.apitoken), json=payload)
    stat_code = results.status_code

    if stat_code == 200 or stat_code == 201:
        print(f"{data['username']} as been added to jFrog...")
    else:
        print(f"something went wrong...")


def delete_user(deleted_user):
    results = requests.delete(url + "/api/security/users/" + deleted_user, auth=(config.login_name, config.apitoken))
    stat_code = results.status_code
    if stat_code == 200 or stat_code == 201:
        print(f"\n{deleted_user} as been deleted from jFrog...\n")
    else:
        print(f"something went wrong...")


def get_username_and_email():
    uname = None
    email = None

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "u:e:d:", ["username=", "email=", "delete="])
    except getopt.GetoptError as err:
        print(err)
        opts = []

    for opt, arg in opts:
        if opt in ['-u', '--username', '--user']:
            uname = arg
        elif opt in ['-e', '--email']:
            email = arg
        elif opt in ['-d', '--delete']:
            uname = arg
            email = 'Deleted Email'
            delete_user(uname)

    if uname == None or email == None:
        usage()

    return uname, email


def usage():
    print(f"\nPlease enter --username and the --email parameters.\n")
    print(f"Usage:\n\t-u, --user, --username\tusername\n\t-e, --email\t\temail-address\n\t-d, --delete")
    print(f"Example: \n\tjfrog.py -u jsidberry -e juan.sidberry@insightglobal.com\n")
    print(f"\nDefault password is:\n\tAbc_1234\n")


def main():
    configuration_item = {}
    user_name, user_email = get_username_and_email()

    if user_email != 'Deleted Email':
        usernames = get_usernames()

        if user_name not in usernames:
            print(f"\n'{user_name}' is not in Artifactory. creating it now...\n")
            configuration_item['username'] = user_name
            configuration_item['email']    = user_email
            configuration_item['password'] = 'Abc_1234'
            configuration_item['groups']   = ["readers", "npm"]
            add_user(configuration_item)
            print(f'added user {user_name}\n')
        else:
            print(f"'{user_name}' already exist...\n")


if __name__ == '__main__':
    main()
    
