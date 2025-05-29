* Eğer cihazda RDP Level 1 (0xBB) aktifken .hex dosyası yüklenirse, STM32CubeProgrammer flash'a yazmayı başarsa bile, yazma sonrasında yaptığı doğrulama sırasında okuma koruması nedeniyle hata mesajı oluşabilir, bu bir hata değildir. Yükleme işlemi başarıyla tamamlanmış olabilir, sadece doğrulama yapılması RDP koruması nedeniyle engellenmiştir. Bu durum, RDP=0xAA komutu yüklemeden sonra çalıştırıldığında otomatik olarak düzelir.

Kullanım:
* JSON ve py dosyaları projede .hex'in olduğu klasöre atılır. (örnek hex yolu -> D:/workspace/stm/rdp_project/CM7/Debug)
* JSON içindeki path'ler ve istenen RDP değeri uygun şekilde değiştirilir.
* Script çalıştırılır.
* RDP durumu "D:\STMPROG\bin\STM32_Programmer_CLI.exe -c port=SWD -ob displ" komutu ile kontrol edilebilir.
