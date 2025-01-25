юот для распознавани лиц

для установки докер контейнера необходимо установка Докер на компе https://www.docker.com/products/docker-desktop/
для устновки не сервер необходимо ставить докер на сервер:
               Для установки Docker на Ubuntu вы можете выполнить следующие шаги. Откройте терминал и выполните следующие команды по порядку:

            1. Обновите индекс пакетов:
               
               sudo apt update
               

            2. Установите необходимые пакеты для добавления нового репозитория через HTTPS:
               
               sudo apt install apt-transport-https ca-certificates curl software-properties-common
               

            3. Добавьте GPG-ключ Docker:
               
               curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
               

            4. Добавьте репозиторий Docker в список источников:
               
               sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
               

            5. Снова обновите индекс пакетов:
               
               sudo apt update
               

            6. Установите Docker:
               
               sudo apt install docker-ce
               

            7. Проверьте, что Docker установлен и работает:
               
               sudo systemctl status docker
               

            Если вы хотите запускать Docker без sudo, добавьте своего пользователя в группу docker:
            sudo usermod -aG docker $USER

создаю образ :
   docker build -t face_check1 . 

проверка докера 
   docker images

запуск контейнера 
   docker run -d face_check1 // название образа (image) после d

   проверка запущенных контейнеров
      docker ps // если добавтьб "-a" то покажет остановленные контейнеры



################################деплоим образ##############################################


docker images

Эта команда выведет список всех доступных образов, включая их имена, теги и идентификаторы.

Пример:
PS C:\microblog\bots\face_checker> docker images
REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
fix1         latest    de719e5e3feb   3 minutes ago   11.3GB

Тегирование образа: Выполни следующую команду для тегирования образа:



docker tag fix1 levsha11/fix1:latest

Загрузка образа на Docker Hub: После этого загрузи образ с помощью команды:



    docker push levsha11/fix1:latest

Убедись, что ты вошел в свою учетную запись Docker Hub, выполнив команду:



docker login

Если все прошло успешно, твой образ должен загрузиться на Docker Hub. 


################################# Заливаем все на сервер ######################################


docker pull levsha11/fix1:latest



#####################################  вносим изменения в docker-compose.yml присваивая ему имя docker-compose1.yml #######################

version: '3.8'

services:
  checker_bot:
    image: levsha11/fix1:latest  # Обновлено имя образа
    container_name: checker_bot
    volumes:
      - /var/www/face_checker_bot/facechecker_data:/app/resources
      - /var/www/face_checker_bot/token.txt:/app/token.txt  # Монтируем файл токенов внутрь контейнера
    restart: unless-stopped

  admin_bot:
    image: levsha11/fix1:latest  # Обновлено имя образа
    container_name: admin_bot
    volumes:
      - /var/www/face_checker_bot/facechecker_data:/app/resources
      - /var/www/face_checker_bot/token.txt:/app/token.txt
    restart: unless-stopped


проходим в идекторию где у нас все лежит 
cd /var/www/face_checker_bot
останавливаем старый докер
sudo docker compose -f docker-compose.yml down

запускаем новый
sudo docker compose -f docker-compose1.yml up -d

