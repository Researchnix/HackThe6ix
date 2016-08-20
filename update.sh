#!/bin/bash

clear
echo "stagig ..."
git add --all

echo "checking the status:"
git status

echo "Do you want to proceed pushing the changes?"
read answer

echo "commit ..."
git commit -m \"update\"
echo "pushing to master"
git push origin master
echo "successfully updated the repository!"
