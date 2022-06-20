import requests
import json
from ..common.settings import jobs_url, headers, api_url


class Job:
    def __init__(self, token):
        self.token = token

    def new(self, jobs_dict):
        if type(jobs_dict) is dict:
            self.__dict__ = jobs_dict
        else:
            print(f"The jobs objet takes an argument of a dictionary defining the job details")
            return
        return 

    def __str__(self):
        return f"Volumez Job {self.id}"


class Jobs:
    def __init__(self, headers):
        self.headers = headers
        self.jobs_list = self.get_jobs()

    def get_job(self, job):
        req = requests.get(api_url+jobs_url+f"/{job}", headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to get job properties. Check job ID and try again")
            return
        j = Job()
        j.new(json.loads(req.text))
        return j

    def get_jobs(self):
        req = requests.get(api_url+jobs_url, headers=self.headers)
        if req.status_code != 200:
            print(f"Error getting a list of jobs. {req.reason}")
            return
        res = json.loads(req.text)
        jobs_list = []
        for r in res:
            j = Job(self.headers)
            j.new(r)
            jobs_list.append(j)
        return jobs_list
        
    def delete_job(self, job):
        req = requests.delete(api_url+jobs_url+f"/{job}", headers=self.headers)
        if req.status_code != 200:
            print(f"Failed to delete job with id {job}. {req.reason}")
            return 
        print(f"Deleted job with id {job}.")
        
    def  __str__(self):
        return f"Volumez Job"
