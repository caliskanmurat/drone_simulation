# DRONE SIMULASYONU UYGULAMASI

<table>
  <tr>
    <td><strong>Hareketli Hedef</strong></td>
    <td><strong>Sabit Hedef</strong></td>
    <td><strong>Hareketli Hedef + Final Durak</strong></td>
   </tr>
  <tr>
    <td><img width="300" src="./gif/hareketli_hedef.gif"></td>
    <td><img width="300" src="./gif/sabit_hedef.gif"></td>    
    <td><img width="300" src="./gif/hareketli_final_durak.gif"></td>
  </tr>
</table>


<hr>

Bu uygulanma kullanılarak belirli hedeflere Drone'lar tarafından ulaşılması simüle edilmektedir. Çalışmada gerekli olan veriler "veriler" klasörü altında bulunmaktadır. Uygulama 3 aşamadan oluşmaktadır. Bunlar; "Güzergah Analizi", "Sonuçların Görselleştirilmesi" ve "Simülasyonun Çalıştırılması". Ayrıca; girdi verilerinin hazırlanmasına yardımcı olabilecek "Rastgele Nokta Oluşturma" imkanı da vardır. Bahsi geçen çalışmalar aşağıda anlatılmıştır.


### 1-) Rastgele Nokta Oluşturma
- `rastgele_nokta_olusturma.py` dosyası kullanılarak gerçekleştirilir,
- "veriler" klasöründeki `data.xlsx` dosyasının `RandomTarget` ve `RandomDrone` sayfasındaki girdiler kullanılarak rastgele drone ve hedef oluşturulur,
- Sonuçlar "sonuclar" klasörüne `random_data.xlsx` ismi ile kaydedilir. (Kayıt yeri ve dosya isminin değiştirilmesi için `rastgele_nokta_olusturma.py` dosyası içerisinden gerekli ayarlamalar yapılabilir.)

### 2-) Çalışma Alanında Rastgele Nokta Oluşturma
- Rastgele Dosya Oluşturma işlemine benzerdir. Oluşacak hedef ve Drone'lara rastgele koordinatlar atamak yerine; "veriler" klasöründe, `sim_boundary.gpkg` dosyasında bulunan ve QGIS yazılımı kullanılarak Beytepe kampüsü sınırları içerisinde daha önce oluşturulan 100 adet hedef baz alınır,
- 100 adet hedef rastgele dağıtılmış olup Drone'ların tek bir noktadan dağıldığı varsayılarak tek bir Drone noktası oluştutulmuştur ve oluşturulan tüm Drone'ların koordinatı bu noktadır,
- İşlem `calisma_alaninda_rastgele_nokta_olusturma.py` dosyası kullanılarak gerçekleştirilir,
- "veriler" klasöründeki `data.xlsx` dosyasının `RandomTarget` ve `RandomDrone` sayfasındaki girdiler kullanılarak oluşturulur,
- `sim_boundary.gpkg` dosyasındaki "Drone" ve "Hedef" koordinatlarını gösteren noktalar değiştirilebilir,
- Sonuçlar "sonuclar" klasörüne `random_data_beytepe.xlsx ismi ile kaydedilir. (Kayıt yeri ve dosya isminin değiştirilmesi için `calisma_alaninda_rastgele_nokta_olusturma.py` dosyası içerisinden gerekli ayarlamalar yapılabilir.)


### 3-) Drone Güzergahı Analizi


### 4-) Güzergaha Ait Çizimler


### 5-) Simulasyon



