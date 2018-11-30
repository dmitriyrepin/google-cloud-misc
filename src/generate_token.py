import argparse

from service import auth


def get_token(audience):
    key_file_path = "gs://some-backet/drepin-service/service-account.json.encrypted"
    key_ring = ""
    crypto_key = ""
    authToken = auth.AuthToken("service-account", key_file_path, "project-name", key_ring, crypto_key)
    #  API -> Credentials -> OAuth 2.0 client IDs: drepin-service: Client ID
    #  audience = "123456789123-XXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com"
    return authToken.get_auth_token(audience)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Generate Google ID token")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-v", "--vision", action='store_true', help='Use vision-service target audience')
    group.add_argument("-d", "--drepin", action='store_false', help='Use drepin service target audience')
    my_args = parser.parse_args()
    if my_args.drepin:
        token = get_token("123456789123-XXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com")
    else:
        token = get_token("123456789123-YYYYYYYYYYYYYYYYYYYYYY.apps.googleusercontent.com")
    print(token)
