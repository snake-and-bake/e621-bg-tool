#!/bin/sh

read -p 'Ender the full path to the folder where you would like to save the photos' pathname

cd $pathname

docker run -it --rm --name e621bg e621bg
