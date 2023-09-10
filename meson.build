project('aviator',
  version: '0.4.2',
  meson_version: '>= 0.59',
)

dependency('glib-2.0')
dependency('pygobject-3.0')
dependency('libadwaita-1', version: '>= 1.2.alpha')

i18n = import('i18n')
gnome = import('gnome')
python = import('python').find_installation('python3')

subdir('data')
subdir('po')
subdir('src')

gnome.post_install(
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
