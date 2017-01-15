#
# Time-stamp: <2017-01-14 16:34:30 alex>
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

test: clean
	@cd net-probe-srv && make -s test
	@cd py-net-probe && make -s test

git-status: clean
	git status
