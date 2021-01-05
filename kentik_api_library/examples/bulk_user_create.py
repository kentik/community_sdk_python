import argparse
import os

import yaml
import kentik_api


def load_kentik_users_from_file(filename):
    with open(filename, "r") as users_yaml_file:
        users_from_file = yaml.load(users_yaml_file, yaml.FullLoader)["users"]
        return [kentik_api.User(**user) for user in users_from_file]
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


if __name__ == "__main__":
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

    email = args.email or os.getenv("KTAPI_AUTH_EMAIL")
    token = args.token or os.getenv("KTAPI_AUTH_TOKEN")
    assert isinstance(email, str)
    assert isinstance(token, str)
    api = kentik_api.KentikAPI(email, token)

    print_all_users(api)

    kentik_users = load_kentik_users_from_file(args.filename)
    created_users = create_users_in_kentik_api(api, kentik_users)
    print("Users created:")
    print_users(created_users)

    print_all_users(api)
