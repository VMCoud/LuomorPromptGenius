```shell
sudo docker run -it --privileged --volume="$(pwd)":/PromptGenius --rm python:3.6 bash
cd PromptGenius/
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
waitress-serve --port=8080 --call app:create_app

sudo docker build -t yiluxiangbei/prompt-genius:v1 -f docker/Dockerfile .
sudo docker run --name prompt-genius -itd -p 8080:8080 yiluxiangbei/prompt-genius:v1

sudo docker run --name prompt-genius -it --rm -p 8080:8080 --volume="$(pwd)":/PromptGenius yiluxiangbei/prompt-genius:v1

cd git/PromptGenius
sudo docker run --name prompt-genius -itd -p 8080:8080 --volume="$(pwd)":/PromptGenius yiluxiangbei/prompt-genius:v1

sudo docker ps -a|grep prompt-genius
sudo docker exec -it prompt-genius bash

sudo docker logs -f prompt-genius
sudo docker stop prompt-genius
sudo docker start prompt-genius
sudo docker rm prompt-genius

http://82.157.54.206:8080/
https://prompt-genius.luomor.com

docker 清理 log
ls -alh /var/lib/docker/containers/9b16ad6d4ab227987a46659075497ba3394c37d0c7f5c61e4850da6a4cb34710/

sudo docker push yiluxiangbei/prompt-genius:v1

docker rmi `docker images | grep none | awk '{print $3}'`
```