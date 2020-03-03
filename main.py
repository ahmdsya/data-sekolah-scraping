import requests
from bs4 import BeautifulSoup
import pandas as pd

# PASTIKAN ANDA TELAH TERKONEKSI DENGAN INTERNET SEBELUM MENJALANKAN FILE INI

# ubah kode_kab_kota
# jalankan file kode_kab_kota.py untuk melihat list kode_kab_kota
kode_kab_kota = '060300'

# ubah jenjang sekolah
# SD, SMP, SMA, SMK
jenjang_sekolah = 'SMA'

# mencari mst_kode_wilayah berdasarkan kode_kab_kota
r = requests.get('http://jendela.data.kemdikbud.go.id/api/index.php/cwilayah/wilayahKabGet')
areas = r.json()['data']
for x in areas:
    if x['kode_wilayah'] == '{}  '.format(kode_kab_kota):
        mst_kode_wilayah = x['mst_kode_wilayah'].replace('  ', '')
        nama = x['nama']

# mengambil data sekolah
r = requests.get('http://jendela.data.kemdikbud.go.id/api/index.php/Csekolah/detailSekolahGET?mst_kode_wilayah={}&bentuk={}'.format(mst_kode_wilayah,jenjang_sekolah))
if r.status_code != 200:
    raise Exception('Gagal mengumpulkan data sekolah ({})'.format(r.status_code))

data   = r.json()['data']
output = [x for x in data if(x['kode_kab_kota'] == '{}  '.format(kode_kab_kota))]
schoolNPSN = [npsn['npsn'].strip() for npsn in output]

sekolah = []
NPSN = []
alamat = []
kode_pos = []
kel = []
kec = []
kab = []
prov = []
status = []
jenjang = []

no_pendirian = []
tgl_pendirian = []
akreditasi = []
no_akreditasi = []
tgl_akreditasi = []

fax = []
email = []
website = []

print('Sedang scraping data sekolah ({}) {}, Silahkan tunggu sampai proses selesai...'.format(jenjang_sekolah, nama))

for npsn in schoolNPSN:
    page = requests.get('https://referensi.data.kemdikbud.go.id/tabs.php?npsn={}'.format(npsn))
    soup = BeautifulSoup(page.content, 'html.parser')

    # Data profil (tab 1)
    tabs1 = soup.find(id='tabs-1')
    data1 = tabs1.find('td', valign='top')
    td1 = data1.find_all('td')
    if len(td1) > 1:
        sekolah.append(td1[3].text)
        NPSN.append(td1[7].text)
        alamat.append(td1[11].text)
        kode_pos.append(td1[15].text)
        kel.append(td1[20].text)
        kec.append(td1[24].text)
        kab.append(td1[28].text)
        prov.append(td1[32].text)
        status.append(td1[36].text)
        jenjang.append(td1[46].text)

    # Data perijinan (tab 2)
    tabs2 = soup.find(id='tabs-2')
    td2 = tabs2.find_all('td')
    if len(td2) > 1:
        no_pendirian.append(td2[8].text)
        tgl_pendirian.append(td2[12].text)
        akreditasi.append(td2[30].text)
        no_akreditasi.append(td2[35].text)
        tgl_akreditasi.append(td2[39].text)

    # Data kontak (tab 3)
    tabs6 = soup.find(id='tabs-6')
    td6 = tabs6.find_all('td')
    if len(td6) > 1:
        test = td6[12].text
        fax.append(td6[3].text)
        email.append(td6[8].text)
        website.append(td6[12].text)


# import data ke file excel (.xlsx)
data = {
    'provinsi': prov,
    'kabupaten': kab,
    'kecamatan': kec,
    'kelurahan': kel,
    'alamat': alamat,
    'kode_pos': kode_pos,
    'npsn': NPSN,
    'sekolah': sekolah,
    'status': status,
    'jenjang': jenjang,
    'akreditasi': akreditasi,
    'no_akreditasi': no_akreditasi,
    'tgl_akreditasi': tgl_akreditasi,
    'no_pendirian': no_pendirian,
    'tgl_pendirian': tgl_pendirian,
    'fax': fax,
    'email': email,
    'website': website
}

df = pd.DataFrame(data)
filename = '{} {}.xlsx'.format(jenjang_sekolah,nama)
writer = pd.ExcelWriter(filename, engine='xlsxwriter')
df.to_excel(writer)
writer.save()

print('SELESAI.. {} data berhasil di simpan.'.format(len(output)))