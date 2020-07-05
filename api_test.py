import urllib.request
import json
"""
Testing the official clash royale API.
"""

def call_api(endpoint: str):
    """
    Calls the API at the base url + an endpoint passed as argument.
    """
    with open("key.txt") as f:
        my_key = f.read().rstrip("\n")
        base_url = "https://api.clashroyale.com/v1"
        request = urllib.request.Request(base_url + endpoint, None, {"Authorization": "Bearer %s" % my_key})
        response = urllib.request.urlopen(request).read().decode("utf-8")
        data = json.loads(response)
        return data


def get_members_in_champion():
    """
    Saves all clan members above 6k in a file.
    """
    store = open("store.txt", "w")

    # %23 is used to escape #. The tag after is the clan tag.
    data = call_api("/clans/%239CC2R9QQ/members")
    for item in data["items"]:
        if(item["trophies"] >= 6000):
            store.write("Name: %s\nTrophies: [%d]\n\n" % (item["name"], item["trophies"]))
    store.close()

def get_members_weekly_donations():
    """
    Saves all clan members and their weekly donations in a file.
    """
    store = open("store.txt", "w")

    # %23 is used to escape #. The tag after is the clan tag.
    data = call_api("/clans/%239CC2R9QQ/members")
    for item in data["items"]:
        store.write("Name: %s\nDonations: [%d]\n\n" % (item["name"], item["donations"]))
    store.close()

def save_members_to_file():
    """
    Saves all clan members in a file. Is used to get total donations from each player.
    """
    store = open("members.txt", "w")

    # %23 is used to escape #. The tag after is the clan tag.
    data = call_api("/clans/%239CC2R9QQ/members")
    for item in data["items"]:
        store.write(item["tag"].replace("#", "%23") + "\n")

def get_members_total_donations():
    """
    Saves all members and their total (lifetime) donations. Takes a long time to execute as it is now.
    """

    # Finds out which player tags we need to look up.
    save_members_to_file()
    playertag = ""
    taglist = []
    store = open("members.txt", "r")
    donation_store = open("member_donations.txt", "w")
    for cnt, line in enumerate(store):
        # Removes all the newlines and reads each tag into a list.
        taglist.append(line.replace("\n", ""))
    # Iterates the tags that we need to look up and changes the endpoint accordingly. A new API call must be made for each player, which is why it takes so long.
    for tag in taglist:
        playertag = tag
        endpoint = "/players/" + playertag
        data = call_api(endpoint)
        donation_store.write("Name: %s\nDonations: [%d]\n\n" % (data["name"], data["totalDonations"]))

get_members_total_donations()
