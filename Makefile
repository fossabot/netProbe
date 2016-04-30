clean:
	cd net-probe-srv && make clean
	cd py-net-probe && make clean
	rm -f *~ 

test:
	cd net-probe-srv && make test
	cd py-net-probe && make test

git-status: clean
	git status

# git commit
# git push origin master
#
# git rm --cached %
# git add %
#
# git status
