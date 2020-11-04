from kentik_fluent_api.kentik_api_client import get_kentik_com_client
import json

client = get_kentik_com_client("<AUTH E-MAIL>", "<AUTH API TOKEN>")


def example1():
    try:
        response = client.v5.devices.get()
    except Exception as e:
        print("{} at {}".format(e, client.host))
        exit(1)

    print_response(response)


def example2():
    try:
        response = client.v5._("deviceLabels").get()
    except Exception as e:
        print("{} at {}".format(e, client.host))
        exit(1)

    print_response(response)


def print_response(response):
    print(response.status_code)
    print(response.headers)
    print(json.loads(response.body))


def print_spacing():
    print("\n" * 4)


if __name__ == "__main__":
    example1()
    print_spacing()
    example2()
