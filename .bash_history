sudo hostnamectlo set-hostname Martinez
sudo hostnamectl set-hostname Martinez
exec bash
curl http://localhost:5000/
curl -X POST -H "Content-Type: application/json" -d '{"usuario":"marcos", "password":"clave123"}' http://localhost:5000/login
curl -X POST -H "Content-Type: application/json" -d '{"usuario":"martinez", "password":"secreta456"}' http://localhost:5000/login
curl -X POST -H "Content-Type: application/json" -d '{"usuario":"marcos", "password":"clave_mala"}' http://localhost:5000/login
ifconfig
