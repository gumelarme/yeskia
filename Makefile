run:
	python3 main.py

emu:
	pypy3 emulator.py

watch:
	watchmedo shell-command --patterns="*.py" --recursive --command="python3 main.py"

raspi_ip = 192.168.1.104
sync:
	rsync -r -t -v --progress -l -s -e ssh --filter=":- .gitignore" /home/gumendol/dev/repo/yeskia pi@$(raspi_ip):/home/pi/repo

compare:
	rsync -avnc -e ssh --filter=":- .gitignore" /home/gumendol/dev/repo/yeskia pi@$(raspi_ip):/home/pi/repo

