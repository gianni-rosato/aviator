desktop_file = i18n.merge_file(
        input: 'net.natesales.Aviator.desktop.in',
       output: 'net.natesales.Aviator.desktop',
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'applications'
)

install_data('net.natesales.Aviator.metainfo.xml',
  install_dir: get_option('datadir') / 'metainfo',
desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

)

subdir('icons')
