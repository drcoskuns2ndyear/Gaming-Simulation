# Gaming-Simulation
#readme
# Simple Turn-Based Rogue Combat Simulation — Stage_1 Architecture Design:

Bu proje, konsol tabanlı küçük bir turn-based rogue-like dövüş oyununun temel mimarisini oluşturmak için hazırlanmıştır. Stage_1’in amacı; oyunun temelini oluşturan sınıfları belirlemek, bu sınıflar arasındaki ilişkileri tasarlamak ve geliştirilebilir bir OOP yapısı kurmaktır. Bu aşamada yalnızca mimari oluşturulur; henüz çalışabilir bir oyun döngüsü, çarpışma veya yapay zekâ sistemi yoktur.

## 1. Amacım:

Stage 1, oyunda yer alacak ana nesneleri ve bu nesnelerin temel davranışlarını tanımlamaya odaklanır. Bu aşamada hedef:

- Ortak davranışların bir üst sınıf ile tanımlanması
- Her nesnenin kendi hareket ve saldırı davranışını uygulayabilmesi
- Encapsulation kullanarak sağlık, konum ve benzeri değişkenlerin kontrollü şekilde saklanması
- Karakterlere ek özellikler kazandırmak için composition yapılarının kullanılması
- İleride oluşturulacak oyun döngüsü, çarpışma sistemi ve AI için sağlam bir temel kurmak

Bu aşama, daha gelişmiş mekaniklerin ekleneceği Stage 2 ve Stage 3 için altyapı görevi görür.

---

## 2. Temel Sınıflar ve Tasarım:

### **GameObject**
GameObject, oyundaki tüm nesnelerin türediği bir üst sınıftır. Her nesne ortak olarak bir `name` ve `position` bilgisine sahiptir (itemlerin move hariç positionları da boş bulunabilir). Bunun yanında tüm alt sınıfların mutlaka tanımlaması gereken iki davranış içerir:

- `move(direction)`
- `attack(target)`
(örneğin itemlerde de vardır fakat boş bulunur)
Bu soyut yapı, Player, Enemy ve Item sınıflarının aynı arayüz üzerinden çalışmasını sağlar.

### **Player**

Oyuncu karakteri için tasarlanmış sınıftır. Player sınıfı:

- `health` değişkeni ile yaşam puanını saklar
- `inventory` bileşenine sahiptir (composition)
- `weapon` bileşeni taşır (composition)
- Kendi hareket ve saldırı davranışlarını uygular

Player’ın davranışı ilerleyen aşamalarda daha karmaşık stratejiler, yetenekler ve envanter yönetimiyle genişletilebilir.

### **Enemy**

Enemy sınıfı, düşman karakterlerini temsil eder. Player ile benzer şekilde:

- `health` değeri içerir
- Bir `weapon` taşıyabilir
- Kendi hareket ve saldırı mantığını uygular

Ayrıca Enemy sınıfında **alternative constructor** kullanımı tasarlanmıştır.  
Bu sayede:

- `Enemy.from_preset("goblin")`
- `Enemy.from_preset("orc")`

gibi hazır düşman tipleri üretilebilir. Bu yöntem, oyun dünyasının çeşitliliğini artırır ve düşmanların tek bir noktadan yönetilmesini sağlar.

### **Item**
Item sınıfı; harita üzerinde duran, oyuncu tarafından toplanabilen veya kullanılan pasif nesneleri temsil eder. Bir eşya:

- `effect` adında bir özelliğe sahiptir
- move() ve attack() gibi davranışlara ihtiyaç duymaz fakat GameObject arayüzü gereği temel metotları boş olarak barındırır

Bu yapı, Item’ların oyundaki karakter sınıflarıyla aynı hiyerarşiyi paylaşmasını sağlar, bu da sistemi daha tutarlı hale getirir.

## 3. Composition Yapıları:

### **Weapon**
Weapon, karakterlerin saldırı gücünü belirleyen basit bir bileşendir. Player ve Enemy tarafından kullanılabilir. Weapon:

- `name`
- `damage`

özelliklerini taşır ve saldırı hesaplamalarında kullanılır.

### **Inventory**
Inventory, Player’ın birden fazla eşya taşıması için kullanılan kompozisyon bileşenidir.  
Bu bileşen:

- Item nesnelerini listede saklar
- `add(item)` gibi temel yönetim işlevlerine sahiptir

Inventory sınıfı, ilerleyen aşamalarda eşyaların aktif/pasif etkileri, kapasite sınırı ve kullanma mekaniği ile genişletilebilir.

## 4. Tasarımın Öne Çıkan Noktaları:

- **Soyutlama:** GameObject, oyundaki tüm nesnelerin ortak davranışlarını belirleyen merkez yapıdır.
- **Polymorphism:** Player, Enemy ve Item aynı metod imzasını paylaşır fakat farklı davranışlar sergiler.
- **Composition:** Inventory ve Weapon gibi sınıflar karakterlere ek özellikler kazandırır ve kod tekrarını azaltır.
- **Genişletilebilirlik:** Yeni düşman türleri, yeni item tipleri veya yeni karakter sınıfları kolayca eklenebilir.
- **Modülerlik:** Kod yapısı, oyun döngüsü ve AI gibi sistemlerin Stage 2’de sorunsuzca eklenebileceği şekilde planlanmıştır.

## 5. Stage 1’in Sonraki Aşamalara Hazırladığı Altyapı

Stage 2’de eklenecek:

- Turn-based oyun döngüsü  
- Karakter hareket sistemi  
- Çarpışma tespiti  
- Savaş sistemi (health reduction, damage)  
- Konsol çıktıları ve basit UI  

Stage 3’te eklenecek:

- Factory Pattern ile nesne üretimi  
- Strategy Pattern ile saldırı ve hareket algoritmaları  
- Pathfinding  
- AI karar mekanizması  
- Leaderboard ve skor sistemi  

Bu nedenle Stage 1’de kurulan mimari, sonraki aşamalara entegre olacak şekilde esnek ve düzenli olarak tasarlanmıştır.
#The End...
