jobs_url = "/jobs"
policy_url = "/policies"
snap_url = "/snapshots"
api_url = "https://api.volumez.com"
nodes_url = "/nodes"
auth_url = "/signin"
volumes_url = "/volumes"
attachments_url = "/attachments"
media_url = "/media"
headers = {"Content-type": "application/json", "Accept":"text/plain"}


def get_headers(token):
    return {"Content-type": "application/json", "Accept":"text/plain", "authorization": token}