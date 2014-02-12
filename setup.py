import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    'packages': [
        'email.mime.multipart',
        'email.mime.base',
        'email.mime.text',
        'reportlab.pdfbase._fontdata_enc_winansi',
        'reportlab.pdfbase._fontdata_enc_macroman',
        'reportlab.pdfbase._fontdata_enc_standard',
        'reportlab.pdfbase._fontdata_enc_symbol',
        'reportlab.pdfbase._fontdata_enc_zapfdingbats',
        'reportlab.pdfbase._fontdata_enc_pdfdoc',
        'reportlab.pdfbase._fontdata_enc_macexpert',
        'reportlab.pdfbase._fontdata_widths_courier',
        'reportlab.pdfbase._fontdata_widths_courierbold',
        'reportlab.pdfbase._fontdata_widths_courierboldoblique',
        'reportlab.pdfbase._fontdata_widths_courieroblique',
        'reportlab.pdfbase._fontdata_widths_helvetica',
        'reportlab.pdfbase._fontdata_widths_helveticabold',
        'reportlab.pdfbase._fontdata_widths_helveticaboldoblique',
        'reportlab.pdfbase._fontdata_widths_helveticaoblique',
        'reportlab.pdfbase._fontdata_widths_symbol',
        'reportlab.pdfbase._fontdata_widths_timesroman',
        'reportlab.pdfbase._fontdata_widths_timesbold',
        'reportlab.pdfbase._fontdata_widths_timesbolditalic',
        'reportlab.pdfbase._fontdata_widths_timesitalic',
        'reportlab.pdfbase._fontdata_widths_zapfdingbats',
        ],
    'include_files': ["winxp.cfg","win7.cfg"],
#    'build_exe': {'include_msvcr': "C:\\WINDOWS\system32\\"},
    }

setup ( name = "MChron Reports",
        version = "0.0.7",
        description = "Report generator and emailer for Oruga Amarilla",
        options = {"build_exe": build_exe_options},
        executables = [Executable("mchron.py"),Executable("config.py")] )
