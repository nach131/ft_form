# Django

https://github.com/django/django

# python-app-api

para saber los error de syntax en el codido

 docker compose run --rm app sh -c "flake8"
 

 Para testear Django

 docker compose run --rm app sh -c "python manage.py test"

lanzar docker para crear el proyeto, docker se para y se borra

crea el proyecto
docker compose run --rm app sh -c "django-admin startproject app ."

crea una app "core"
docker compose run --rm app sh -c "django-admin startapp core"

=====================


docker compose run --rm app sh -c "python manage.py makemigrations"

docker compose run --rm app sh -c "python manage.py migrate"

====================

# AWS

sudo yum install git -y

$-> sudo yum install docker -y
$-> sudo service docker start

sudo usermod -a -G docker ec2-user

sudo usermod -aG docker $USER

# make docker  autostart
$-> sudo chkconfig docker on
# I strongly recommend install also: git (sudo yum install -y git)

$-> sudo reboot # only if for you it is neccesary


# docker-compose (latest version)
$-> sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
# Fix permissions after download
$-> sudo chmod +x /usr/local/bin/docker-compose
# Verify success
$-> docker-compose version

# run server
docker-compose -f docker-compose-deploy.yml up -d



1. **Super Fácil**
2. **Muy Fácil**
3. **Fácil**
4. **Normal**
5. **Difícil**
6. **Muy Difícil**
7. **Extremo**
8. **Imposible**
9. **Infernal**
10. **Dios**

### En Inglés:
1. **Super Easy**
2. **Very Easy**
3. **Easy**
4. **Normal**
5. **Hard**
6. **Very Hard**
7. **Extreme**
8. **Impossible**
9. **Infernal**
10. **God**

Estas listas te permiten definir una progresión de dificultad de manera clara y efectiva para los jugadores.


https://obfuscator.io/

# PIXIjs
https://github.com/pixijs/pixijs/releases