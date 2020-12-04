from kentik_api.client import get_kentik_com_client
import json
import os


def example1(client):
    try:
        response = client.v5.devices.get()
    except Exception as e:
        print("{} at {}".format(e, client.host))
        exit(1)

    print_response(response)


def example2(client):
    try:
        response = client.v5._("deviceLabels").get()
    except Exception as e:
        print("{} at {}".format(e, client.host))
        exit(1)

    print_response(response)


def get_client():
    email = token = ''
    try:
        email = os.environ['KTAPI_AUTH_EMAIL']
        token = os.environ['KTAPI_AUTH_TOKEN']
    except KeyError:
        print('You have to specify KTAPI_AUTH_EMAIL and '
              'KTAPI_AUTH_TOKEN first')
        exit(1)

    return get_kentik_com_client(email, token)


def print_response(response):
    print(response.status_code)
    print(response.headers)
    print(json.loads(response.body))


def print_spacing():
    print("\n" * 4)


if __name__ == "__main__":
    com_client = get_client()
    example1(com_client)
    print_spacing()
    example2(com_client)
