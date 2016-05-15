#
# Time-stamp: <2016-05-15 11:10:17 alex>
#

all:
	@echo make git-status
	@echo make clean
	@echo make test

clean:
	@cd net-probe-srv && make -s clean
	@cd py-net-probe && make -s clean
	@rm -f *~ 
	@rm -f ansible/files/*~ ansible/playbooks/*~ ansible/playbooks/*retry

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
