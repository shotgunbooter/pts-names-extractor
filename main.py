import requests

session = requests.Session()

def get_max_pages():
    r = session.get("https://habbo-ca.com/all/personnel")
    r.raise_for_status()
    data = r.json()
    return data['last_page']

def get_personnel(page):
    r = session.get(f"https://habbo-ca.com/all/personnel?page={page}")
    r.raise_for_status()
    data = r.json()
    return data['personnel']

def main():
    max_pages = get_max_pages()
    personnel = []
    
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page} of {max_pages}...")
        personnel.extend(get_personnel(page))
    
    print(f"Total personnel fetched: {len(personnel)}")
    print(f"Writing usernames to personnel.txt...")
    with open("personnel.txt", "w") as f:
        seen = set()
        for person in personnel:
            username = person.get('username')

            status = person.get('status')
            if status == 'active' or status == "reserves":
                if username and username not in seen:
                    print(f"Writing username for person: {username}")
                    f.write(f"{username}\n")
                    seen.add(username)
                elif not username:
                    print("Missing 'username':", person)

main()
