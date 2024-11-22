import pdfkit

path_to_wkhtmltopdf = r'G:\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

url = 'https://di.hkex.com.hk/di/NSForm2.aspx?fn=CS20230209E00204&sa2=cs&sid=11636&corpn=Industrial+and+Commercial+Bank+of+China+Ltd.++-+H+Shares&sd=01%2f07%2f2023&ed=31%2f12%2f2023&cid=2&sa1=cl&scsd=01%2f07%2f2023&sced=31%2f12%2f2023&sc=1398&src=MAIN&lang=EN&g_lang=en&'
output = 'pagetest.pdf'

pdfkit.from_url(url, output, configuration=config)
    