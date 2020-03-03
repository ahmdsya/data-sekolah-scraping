import requests

# PASTIKAN ANDA TELAH TERKONEKSI DENGAN INTERNET SEBELUM MENJALANKAN FILE INI

# mencari kode_kab_kota
r = requests.get('http://jendela.data.kemdikbud.go.id/api/index.php/cwilayah/wilayahKabGet')
areas = r.json()['data']

# membuat table
print('kode_kab_kota  |  nama')
for x in areas:
    print(x['kode_wilayah'].strip()+'         |  '+x['nama'])

