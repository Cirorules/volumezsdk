import requests
import json
from .settings import jobs_url, headers, api_url


class Job:
    def new(self, jobs_dict):
        if type(jobs_dict) is dict:
            self.__dict__ = jobs_dict
        else:
            print(f"The jobs objet takes an argument of a dictionary defining the job details")
            return
        return 

    def get_job(self, token):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.get(api_url+jobs_url+"/"+str(self.id), headers=heads)
        if req.status_code != 200:
            print(f"Failed to get job properties. Check job ID and try again")
            return
        self.__dict__ = json.loads(req.text)
        print("Job state updated")
        return

    def delete_job(self, token):
        heads = headers
        heads["authorization"] = token.id_token
        req = requests.delete(api_url+jobs_url+"/"+str(self.id), headers=heads)
        if req.status_code != 200:
            print(f"Failed to delete job with id {self.id}. {req.reason}")
            return 
        print(f"Deleted job with id {self.id}.")

    def  __str__(self):
        return f"Volumez Job {self.id}"


class Jobs:
    def __init__(self, token):
        self.token = token
        self.headers = headers
        self.headers["authorization"] = self.token.id_token

    def get_jobs(self):
        req = requests.get(api_url+jobs_url, headers=self.headers)
        if req.status_code != 200:
            print(f"Error getting a list of jobs. {req.reason}")
            return
        res = json.loads(req.text)
        self.jobs = []
        for r in res:
            j = Job()
            j.new(r)
            self.jobs.append(j)
