docker run --name mi-mysql-db -e MYSQL_ROOT_PASSWORD=nolasabrasnunca1970 -e MYSQL_DATABASE=secretaria-el-cano -p 3306:3306 -v mysql-data:/var/lib/mysql -d mysql:latest
