FROM hub.meiqia.com/devops/python:2.7.13

COPY . /data/apps/harbor/

RUN pip install -r /data/apps/harbor/requirement.txt -i https://pypi.douban.com/simple

ENTRYPOINT ["python","/data/apps/harbor/main.py"]
CMD ["-h"]
