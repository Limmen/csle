docker network create --subnet=15.15.15.0/24 my_custom_network

docker run -d --name test_container1 --network my_custom_network --ip 15.15.15.15 alpine sh -c "while true; do sleep 3600; done"

docker run -d --name test_container2 --network my_custom_network --ip 15.15.15.14 alpine sh -c "while true; do sleep 3600; done"

docker exec test_container2 ping -c 3 15.15.15.15

docker stop test_container1
docker stop test_container2
docker rm test_container1
docker rm test_container2

