import matplotlib.pyplot as plt
from IPython import display

# İnteraktif modu açıyoruz ki grafik her oyunda kendini güncellesin
plt.ion()

def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    
    # Grafiğin başlıkları ve eksenleri
    plt.title('Yapay Zeka Eğitim Süreci')
    plt.xlabel('Oyun Sayısı')
    plt.ylabel('Skor')
    
    # Skorları ve ortalamayı çizdir
    plt.plot(scores, label='Anlık Skor', color='blue')
    plt.plot(mean_scores, label='Ortalama Skor', color='orange')
    plt.ylim(ymin=0)
    
    # Grafiğin sonuna anlık değerleri yazdır
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))
    
    plt.legend(loc='upper left')
    plt.show(block=False)
    plt.pause(0.1)