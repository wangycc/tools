#/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'WangYiChen'

from harborclient import logger,HarborClient

import arrow
import argparse
import logging
import json

logger.setLevel(logging.INFO)

class HarborHandler(HarborClient):
    def get_repositories_name(project=None):
	projects = [ project['project_id'] for project in self.get_projects() ] 
	repositories_name = []
	if not project:
	   for project in projects:
		 for repositories in self.get_repositories(project):
		     repositories_name.append(repositories['name'])
	   return repositories_name
	for repositories in self.get_repositories(project):
	    repositories_name.append(repositories['name'])
	return repositories_name

    def get_repository_tag(self,repo_name,datetime_day=None):
	result = super(HarborHandler,self).get_repository_tags(repo_name)
	# 处理时间戳
	for tag_info in result:
	    tag_info["timestamp"] = arrow.get(tag_info["created"]).timestamp
	if datetime_day:
	    current_timestamp = arrow.get().timestamp
	    delta_timestamp = datetime_day * 86400
	    last_timestamp = current_timestamp - delta_timestamp
	    last_result = []
	    for tag_info in result:
		if tag_info["timestamp"] <= last_timestamp:
		    last_result.append(tag_info)
	    return last_result
	return result

def arg_parse():
    parser = argparse.ArgumentParser(description="cleanup Harbor registry")
    parser.add_argument("-d","--day",
			dest="day",
			type=int,
			help="Only delete tags created before given date.")
    parser.add_argument("--last",
			dest="last",
			type=int,
			help="Keep last N tags(default: 20)",
			default=20)
    parser.add_argument("-g","--group",
			dest="group",
			nargs='+',
			help="Delete only the repositories of the specified project group")
    parser.add_argument("-l","--list",
			dest="list",
			action='store_true',
			help="list all project group")
    parser.add_argument("-u","--user",
			dest="user",
			help="harbor user")
    parser.add_argument("-p","--password",
			dest="password",
			help="harbor password")
    parser.add_argument("--host",
			dest="host",
			help="harbor host")
    return parser.parse_args()

def main():
    args = arg_parse()
    client = HarborHandler(host=args.host,
			   user=args.user,
			   password=args.password,
			   protocol="https")
    client.login()
    if args.list:
	projects = [] 
	for project in client.get_projects():
	    projects.append({
		"project_name": project['name'],
	        "project_id": project['project_id']
		})
	print(json.dumps(projects,indent=4))
	return 
    #repositories = []
    for project in args.group:
	# get all repositories in the project group
	for repository in  client.get_repositories(project):
            ## get all expired tags for repository	
	    repository = repository["name"]
	    if len(client.get_repository_tag(repository)) > args.last:
		expired_tags = []
                for repostory_tag in client.get_repository_tag(repository,args.day):
		    repostory_tag['repostory_name']=repository
		    expired_tags.append(repostory_tag["name"])
		    # 判断删除过期的tag之后剩余tag数是否满足保留要求，如果不满足就跳过。
		    if len(client.get_repository_tag(repository)) - len(expired_tags) < args.last:
			break
		    client.delete_tag_of_repository(repository,repostory_tag["name"])
if __name__ == "__main__":
    main()
