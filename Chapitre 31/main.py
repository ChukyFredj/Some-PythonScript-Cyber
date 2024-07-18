import sqlite3
import os

def get_firefox_profile_path():
    if os.name == 'nt':
        base_path = os.path.expandvars(r'%APPDATA%\Mozilla\Firefox\Profiles')
    elif os.name == 'posix':
        base_path = os.path.expanduser('~/.mozilla/firefox')
    else:
        raise Exception("Unsupported OS")

    profiles = [os.path.join(base_path, profile) for profile in os.listdir(base_path) if profile.endswith('.default-release')]
    if not profiles:
        raise Exception("No Firefox profiles found")
    return profiles[0]

def get_cookies():
    profile_path = get_firefox_profile_path()
    cookies_db_path = os.path.join(profile_path, 'cookies.sqlite')

    connection = sqlite3.connect(cookies_db_path)
    cursor = connection.cursor()

    query = """
    SELECT host, name, value
    FROM moz_cookies
    LIMIT 10
    """

    cursor.execute(query)
    rows = cursor.fetchall()
    connection.close()

    return rows

if __name__ == "__main__":
    cookies = get_cookies()
    print("Cookies :")
    for cookie in cookies:
        print(f"Host: {cookie[0]}, Name: {cookie[1]}, Value: {cookie[2]}")
