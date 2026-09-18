# 8-Puzzle AI Search

8-Puzzle problemini farklı yapay zekâ arama algoritmaları kullanarak çözmek amacıyla geliştirilmiş bir Python projesidir.

Projede uninformed search yöntemlerinden Breadth-First Search (BFS) ve Depth-First Search (DFS) ile informed search yöntemi olan A* algoritması uygulanmıştır.

A* algoritması için Manhattan Distance ve Euclidean Distance olmak üzere iki farklı sezgisel (heuristic) fonksiyon kullanılabilmektedir.

## Özellikler

- 8-Puzzle probleminin çözülmesi
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- A* Search
- Manhattan Distance sezgisel fonksiyonu
- Euclidean Distance sezgisel fonksiyonu
- Geçerli puzzle hareketlerinin otomatik oluşturulması
- Çözüm yolunun adım adım gösterilmesi
- Yapılan hareket yönlerinin gösterilmesi
- Toplam çözüm maliyetinin hesaplanması
- Genişletilen düğüm sayısının hesaplanması
- Çözüm derinliğinin gösterilmesi
- Algoritmaların çalışma süresinin ölçülmesi

## Kullanılan Algoritmalar

### Breadth-First Search (BFS)

BFS, başlangıç durumundan itibaren düğümleri seviye seviye genişleterek hedef durumu arar.

Projede oluşturulan yeni puzzle durumları kuyruk mantığıyla işlenerek hedef duruma ulaşılmaya çalışılmaktadır.

### Depth-First Search (DFS)

DFS, bir çözüm yolunda mümkün olduğunca derine ilerleyerek arama gerçekleştirir.

Bir yol tamamlandığında veya ilerleme mümkün olmadığında diğer olası durumlar incelenir.

### A* Search

A* algoritması, gerçek yol maliyeti ile sezgisel maliyeti birlikte kullanarak hedef duruma ulaşmaya çalışır.

Algoritmada toplam maliyet:

f(n) = g(n) + h(n)

şeklinde hesaplanmaktadır.

Burada:

- g(n): Başlangıç durumundan mevcut duruma kadar yapılan hamle sayısını ifade eder.
- h(n): Mevcut durum ile hedef durum arasındaki tahmini maliyeti ifade eder.

## Sezgisel Fonksiyonlar

### Manhattan Distance

Her taşın mevcut konumu ile hedef konumu arasındaki yatay ve dikey uzaklıkların toplamı hesaplanır.

### Euclidean Distance

Her taşın mevcut konumu ile hedef konumu arasındaki doğrusal uzaklık hesaplanır.

Kullanıcı A* algoritmasını seçtiğinde kullanılacak sezgisel fonksiyonu belirleyebilir.

## Hedef Durum

Projede kullanılan hedef puzzle durumu:

1 2 3  
8 0 4  
7 6 5  

0 değeri puzzle içerisindeki boş alanı temsil etmektedir.

## Program Çıktıları

Program çözüm işlemi tamamlandıktan sonra kullanıcıya aşağıdaki bilgileri gösterir:

- Hedefe ulaşmak için izlenen puzzle durumları
- Yapılan hareketlerin yönleri
- Toplam hamle sayısı
- Genişletilen düğüm sayısı
- Çözüm derinliği
- Algoritmanın çalışma süresi

## Kullanılan Teknolojiler

- Python
- NumPy
- heapq
- Jupyter Notebook
- Artificial Intelligence
- Search Algorithms
- Heuristic Search

## Proje Dosyaları

- main.py — 8-Puzzle çözüm algoritmalarının bulunduğu ana Python dosyası
- EightPuzzle.ipynb — Projenin Jupyter Notebook sürümü
- yapay_zeka_rapor.pdf — Projeye ait ayrıntılı rapor
- README.md — Proje açıklamaları

## Kurulum

Projeyi çalıştırmak için Python ve NumPy gereklidir.

NumPy kütüphanesini yüklemek için:

pip install numpy

## Çalıştırma

Terminal üzerinden:

python main.py

komutunu çalıştırın.

Program başlangıç puzzle durumundaki 9 değeri kullanıcıdan ister.

Daha sonra kullanılacak algoritma seçilir:

1 - BFS  
2 - DFS  
3 - A*  
4 - Exit  

A* seçildiğinde ayrıca sezgisel fonksiyon seçilir:

1 - Manhattan Distance  
2 - Euclidean Distance  

Program seçilen algoritma ile puzzle'ı çözerek sonuçları terminal üzerinde gösterir.

## Projenin Amacı

Bu projenin amacı yapay zekâ alanındaki temel arama algoritmalarının aynı problem üzerinde uygulanmasını ve çalışma biçimlerinin incelenmesini sağlamaktır.

BFS, DFS ve A* algoritmaları uygulanarak uninformed ve informed search yöntemlerinin 8-Puzzle problemi üzerindeki kullanımı incelenmiştir.

## Proje Notu

Bu proje Yapay Zekâ dersi kapsamında geliştirilen akademik bir çalışmadır.
