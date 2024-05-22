project('aviator',
  version: '0.6.1',
  meson_version: '>= 0.59',
)

dependency('glib-2.0')
dependency('pygobject-3.0')
dependency('libadwaita-1', version: '>= 1.4.0')

i18n = import('i18n')
gnome = import('gnome')
python = import('python').find_installation('python3')

subdir('data')
subdir('po')
subdir('src')

config_data = configuration_data()
config_data.set_quoted('LOCALEDIR', join_paths(get_option('prefix'), get_option('localedir')))
config_data.set_quoted('GETTEXT_PACKAGE', meson.project_name())
config_file = configure_file(
    input: 'src/aviator.in',
    output: '@BASENAME@',
    configuration: config_data
)

gnome.post_install(
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
