FROM python:3.6
RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak
COPY docker/sources.list /etc/apt/sources.list
RUN apt-get update
WORKDIR /PromptGenius
ADD . .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' > /etc/timezone

EXPOSE 8080

#CMD ["tail", "-f", "/dev/null"]
CMD ["waitress-serve", "--port=8080", "--call", "app:create_app"]