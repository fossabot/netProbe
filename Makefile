clean:
	@cd net-probe-srv && make -s clean
	@cd py-net-probe && make -s clean
	@rm -f *~ 

test:
	@cd net-probe-srv && make -s test
	@cd py-net-probe && make -s test

git-status: clean
	git status

# git commit
# git push origin master
#
# git rm --cached %
# git add %
#
# git status
