from PyPDF2 import PdfMerger

merger = PdfMerger()
merger.append('production/1_create_frontpage.pdf')
merger.append('production/submission.pdf')
merger.write('production/production_output.pdf')       
merger.close()