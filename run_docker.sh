JUPYTER_TOKEN=test24
docker run --rm -it -p 5901:5901 -p 9999:9999 -e JUPYTER_TOKEN=${JUPYTER_TOKEN} lukassnoek/niedu
