git stash
echo -e "This file contains bug\nIt has to be somewhere.\nI feel like I can smell it.\nHow this program could work with such bug?" > bug.txt
git add bug.txt
git commit -m "bugfixes"
git stash pop
echo -e "Finally, finished it!" >> bug.txt
git add .
git commit -m "program"
git push