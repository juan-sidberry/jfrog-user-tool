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
    print(" creating it now...\n")
    payload = {'name': data['username'], 'email': data['email'], 'password': data['password'], 'groups': data['groups']}
    results = requests.put(url + "/api/security/users/" + data['username'], auth=(config.login_name, config.apitoken), json=payload)
    stat_code = results.status_code

    if stat_code == 200 or stat_code == 201:
        print(f"{data['username']} as been added to jFrog...\n")
    else:
        print(f"something went wrong...\n")
        action_status = "error"
        return action_status


def delete_user(deleted_user):
    results = requests.delete(url + "/api/security/users/" + deleted_user, auth=(config.login_name, config.apitoken))
    stat_code = results.status_code
    if stat_code == 200 or stat_code == 201:
        print(f"\n{deleted_user} as been deleted from jFrog...\n")
    else:
        print(f"something went wrong...\n")


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
    print(f"\nUsage:\n\t-u, --user, --username\tusername\n\t-e, --email first.last@domain.com\n\t-d, --delete username")
    print(f"Examples: \n\tadd: python jfrog.py -u batman -e bruce.wayne@domain.com")
    print(f"\tdel: python jfrog.py -d batman")
    print()
    print(f"\nDefault password is:\n\tAbc_1234\n")


def main():
    configuration_item = {}
    user_name, user_email = get_username_and_email()
    action_status = ''

    if user_email != 'Deleted Email':
        usernames = get_usernames()

        if user_name not in usernames:
            print(f"\n'{user_name}' is not in Artifactory...\n")
            configuration_item['username'] = user_name
            configuration_item['email']    = user_email
            configuration_item['password'] = 'Abc_1234'
            configuration_item['groups']   = ["readers", "npm"]
            action_status = add_user(configuration_item)
            # if action_status == "error":
            #     pass
        else:
            print(f"'{user_name}' already exist...\n")


if __name__ == '__main__':
    main()
    
