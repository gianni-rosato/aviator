all: flatpak run

update-ffmpeg-python:
	if ! [ -f flatpak-pip-generator ]; then wget https://raw.githubusercontent.com/flatpak/flatpak-builder-tools/master/pip/flatpak-pip-generator; fi
	python3 flatpak-pip-generator --requirements-file=requirements.txt
	# cat python3-ffmpeg-python.json | python3 -c 'import sys, yaml, json; print(yaml.dump(json.loads(sys.stdin.read())["sources"]))'
	# rm -f flatpak-pip-generator ffmpeg-python.json

clean:
	rm -rf build/ .flatpak-builder/

flatpak:
	flatpak-builder build net.natesales.Aviator.yml --force-clean --install --user

run:
	flatpak run net.natesales.Aviator
