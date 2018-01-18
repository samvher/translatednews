Setup on EC2 Amazon Linux instance
==================================

```bash
sudo yum update -y
sudo yum install -y docker git
sudo service docker start
sudo usermod -a -G docker ec2-user
```

Log out of your ssh session and back in for the new docker rights.

```bash
git clone https://github.com/samvher/translatednews
chmod a+rw ~/translatednews/data
cd translatednews/docker
docker build -t tn .

docker run -d -p 80:80 -p 443:443 \
  --name nginx-proxy \
  -v /home/ec2-user/translatednews/nginx/certs:/etc/nginx/certs:ro \
  -v /home/ec2-user/translatednews/nginx/vhost.d:/etc/nginx/vhost.d \
  -v /home/ec2-user/translatednews/nginx/html:/usr/share/nginx/html \
  -v /var/run/docker.sock:/tmp/docker.sock:ro \
  --label com.github.jrcs.letsencrypt_nginx_proxy_companion.nginx_proxy \
  jwilder/nginx-proxy:alpine

docker run -d \
  -v /home/ec2-user/translatednews/nginx/certs:/etc/nginx/certs:rw \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  --volumes-from nginx-proxy \
  jrcs/letsencrypt-nginx-proxy-companion

docker run -d --restart=always \
  --name tn \
  -e VIRTUAL_HOST=translatethe.news,www.translatethe.news \
  -e LETSENCRYPT_HOST=translatethe.news,www.translatethe.news \
  -e LETSENCRYPT_EMAIL=samvherwaarden@gmail.com \
  -v /home/ec2-user/translatednews/app:/app \
  -v /home/ec2-user/translatednews/data:/data \
  tn
```
