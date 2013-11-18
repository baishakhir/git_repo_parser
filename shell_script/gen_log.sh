cd $1
echo "sha | committer | commit date | author | author date | subject | body" >  no_merge_log.txt
git log --no-merges --shortstat --pretty="%H | %cn | %cd | %an | %ad | %s | %b" >> no_merge_log.txt
cd ..
