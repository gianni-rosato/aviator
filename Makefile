all: requirements flatpak run

requirements:
	rm -f python3-requirements.json
	python3 ~/apps/flatpak-pip-generator --requirements-file requirements.txt

flatpak:
	flatpak-builder build net.natesales.Aviator.yml --force-clean --install --user

run:
	flatpak run net.natesales.Aviator
