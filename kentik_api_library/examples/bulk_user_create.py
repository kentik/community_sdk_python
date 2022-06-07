import argparse
import logging

import yaml

from kentik_api import KentikAPI, User
from kentik_api.utils import get_credentials

logging.basicConfig(level=logging.INFO)


def load_kentik_users_from_file(filename):
    with open(filename, "r") as users_yaml_file:
        users_from_file = yaml.load(users_yaml_file, yaml.FullLoader)["users"]
        return [User(**user) for user in users_from_file]
        # Calls kentik_api.User(full_name=user["full_name"], email=user["email"], role=user["role"],
        #                       email_service=user["email_service"], email_product=user["email_product"])
        # for each entry in the file


def create_users_in_kentik_api(api_client, users):
    result = []
    for user in users:
        result.append(api_client.users.create(user))
    return result


def delete_users_from_kentik_api(api_client, users):
    for user in users:
        api_client.users.delete(user.id)


def print_users(users):
    for user in users:
        print(user.full_name, user.created_date)


def print_all_users(api_client):
    print("All users:")
    users = api_client.users.get_all()
    print_users(users)


def get_users_filename() -> str:
    parser = argparse.ArgumentParser(description="Load users from file and create them in Kentik API.")
    parser.add_argument(
        "--filename",
        dest="filename",
        default="users.yaml",
        help="path to a YAML file containing Kentik Users",
    )
    parser.add_argument("--email", dest="email", help="email to be used to authenticate with Kentik API")
    parser.add_argument(
        "--token",
        dest="token",
        help="API token to be used to authenticate with Kentik API",
    )
    args = parser.parse_args()
    return args.filename


if __name__ == "__main__":
    email, token = get_credentials()
    client = KentikAPI(email, token)

    print_all_users(client)
    print()

    kentik_users = load_kentik_users_from_file(get_users_filename())
    created_users = create_users_in_kentik_api(client, kentik_users)
    print("Users created:")
    print_users(created_users)
    print()

    print("Delete created users...")
    delete_users_from_kentik_api(client, created_users)
    print("Done")
