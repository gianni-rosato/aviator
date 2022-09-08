all: clean flatpak run

clean:
	rm -rf build/ .flatpak-builder/

flatpak:
	flatpak-builder build net.natesales.Aviator.yml --force-clean --install --user

run:
	flatpak run net.natesales.Aviator
