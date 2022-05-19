# Compiler_Design


# Derleyici(Compiler) Tasarımı

>## Project

![image](https://user-images.githubusercontent.com/61595808/169250874-5458fa8f-5a85-47f7-b25e-8fc6f5369c9a.png)

![image](https://user-images.githubusercontent.com/61595808/169315015-96e1c001-fb7f-455e-b7ad-85c5f7ccc27d.png)

![image](https://user-images.githubusercontent.com/61595808/169346485-bbd73630-d7c9-4468-b457-d21ec8155c3e.png)



> ## 08-03-2022

- ### Derleyici ve Yorumlayıcı arasındaki fark nedir?

Programın derleme işlemini gerçekleştiren programa Derleyici (Compiler), yorumlama işlemini gerçekleştiren programa ise Yorumlayıcı (Interpreter) adı verilir.

Derleyiciler, yorumlayıcılara göre daha hızlıdır. Çünkü yorumlayıcılar ilk kod satırından son kod satırına kadar her satırını teker teker yorumlar ve kodun karşılığındaki işlemi gerçekleştirir. Derleyiciler ise kodların tamamını bilgisayar diline çevirir. Eğer hata varsa, tüm hataları programcıya bildirir.


- ### Token nedir?

Token'lar, bir platform veya uygulama şeklinde oluşturulmuş ve platformun tüm yönlerinden faydalanmanıza olanak sağlayan transfer edilebilen dijital mülkler olarak tanımlanır.

- ### Yüksek Seviyeli,Orta Seviyeli, Alt Seviyeli dil nedir?

Alt seviye programlama dilleri: Makine koduna oldukca yakın programlama dilleridir.Makina hakimiyeti oldukca gelişmiştir.Bu programlama dillerini bilen kişilerin mikro işlemciler hakkında bilgi sahibi olması gereklidir.(Assembly programlama dili gibi)

Orta seviye programlama dilleri: Oldukça esnek olan bu diller hem üst hem alt seviye programlama yapabilirler. Alt seviye dillere oranla biraz daha anlaşılırdır. (C programlama dili gibi.)

Üst seviye programlama dilleri: Olay tabanlı programlama dilleri olarak da adlandırılırlar yalnız bu programlama dilleri sadece belirli fonksiyonlar etrafında çalışırlar ve programlama hakimiyetini azaltırlar. En hızlı ve en etkili programlama dilleri bu kategoridedir. (visual basic ve pic basic pro gibi) Diğer programlama dillerine kıyasla daha kolay öğrenildiği ve uygulandığı için yeni başlayanlara en uygun diller üst seviye programlama dilleridir.

- ### bin ve exe dosyası ne demek?

BIN, dosya uzantısı yaygın olarak sıkıştırılmış arşiv dosyları olarak programlar tarafından farklı amaçlar için kullanılır. Açılımıyla “Binary” olarak adlandırılan bu dosya türlerini genellikle CD, veya DVD, dosyalarının Backup, yansıması alındığında veya virüs, yazılımlarının içerisinde görebiliriz.

.exe uzantılı EXE dosyaları, bilgisayarınıza yeni bir uygulama yüklemek istediğiniz zaman kullanmak zorunda olduğunuz yükleme dosyalarının formatıdır.
Executable, (Türkçesi çalıştırılabilir) uygulanabilir bir dosya, bilgisayar bilimininde, içeriği bir bilgisayar ile bir program arasında yorumlanmak için ifade edilen bir dosyadır. Sözlük anlamı çalıştırılabilir olmakla beraber bağımsız çalışabilen Windows Application dosya uzantısı (.exe) uzatılmış halidir.

- ### Static Dil ile Dynamic Dil arasındaki fark nedir?

Statik programlama dili, her değişken tipinin önceden belirtiliyor olmasıdır. Yani string bir değer tanımlıyorken başına string, sayi tanımlıyorken int, double, float gibi tipleri yazıyoruz. Bu nedenle değişken tipleri program henüz çalışmıyorken bile bu tiplerin neler olduğunu biliyor. Bu da program henüz çalışmıyorken bile bir hata yapmışsanız sizi uyarır ve hatayı düzeltmenizi bekler.
C, C++, C#, Java, Scala, Haskel gibi diller statik programlama dilleridir.
Statik programlama dillerinin amacı donanımı optimize etmek olduğu için bu şekilde çalışmak zorundadırlar.


Dinamik programlama dilleri ise statiğin aksine değişken tiplerinin programın çalışma anında belirlendiği dillerdir. Yani ne string, ne int, ne double ne de bir array için herhangi bir değişken tipi belirtmenize gerek yoktur. Bazıları bunun geliştirme hızını artırdığını çünkü geliştiricinin hangi tiple olduğunu düşünmeden direk yazdığını savunsa da (haklılık payları yok değil) programın çalışma anına kadar herhangi bir hata var mı yok mu göremezler.
Lisp, Perl, Ruby, Python, JavaScript gibi filler dinamik programlama dilleridir.
Dinamik programmala dillerinin amacı geliştiricinin dili en etkili şekilde kullanabilmesi için tasarlanmışlardır, bu nedenle bu tipler çalışma anında belirlenir.

- ### Linker ne demek?

Bir derleyici tarafından üretilmiş olan kodları bağlayarak işletim sisteminin çalıştırabileceği tek bir kod üreten programdır.
Kodun birden fazla parçaya bölünmesi ve her parçanın ayrı ayrı üretilmesi durumunda bu parçaların birleştirilmesi ve tek bir program halinde üretilmesinden sorumlu olan programlara bağlayıcı (linker) adı verilmektedir

- ### dll,lib,exe,obj nedir?


- ### setup dosyası nedir?


- ### XML nedir?

_Derleme (compilation) ,Yorumlama (interpretation)_

> ## 15-03-2022

- ### Lexical Analysis nedir?

- ### Joker karakter nedir?


> ## 22-03-2022

- Lexical Analizde tokenler çıkarılıyor.

- Scanner ->harf harf okunuyor

- Lexical : -Parser ve -Scanner
- 
- Lexical analizde en başta

      *boşluklar çıkar
      
      *tablolar çıkar
      
      *harf harf okunur
      
      *tokenler tespit edilir.

- Her bir satıra sayı vermelisin ki nerede hata olduğunu görebilirsin.

- Boşluk bir token değildir.

- Num(10) -> token

- +boş küme olamaz

- elapsed Time -> bu iş için ne kadar zaman harcadın.

- text=\"%s\" ,programlama dilinde karar veremiyordu,iç içe aynı karakterleri bütün olarak görsün diye \\ kulanılıyordu c'de.

























