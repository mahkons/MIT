echo -e "*.exe \n*.o \n*.jar \nlibraries/" > .gitignore
git add *
git add .gitignore
git commit -m "Add and ignore"
git push