import psutil
import matplotlib.pyplot as plt
import time

def collect_cpu_data(duration=10, interval=1):

    cpu_percentages = []
    timestamps = []
    for _ in range(duration):  # Collecter des données pendant 'duration' secondes
        cpupercent = psutil.cpu_percent(interval=interval)
        timestamp = time.strftime("%H:%M:%S")
        cpu_percentages.append(cpupercent)
        timestamps.append(timestamp)
    return timestamps, cpu_percentages

def simulate_load(duration=10):

    for _ in range(duration):  # Boucle pour simuler la charge
        # Calculer la somme de grands nombres pour simuler une charge CPU
        sum(i * i for i in range(1000000))
        time.sleep(1)  # Pause d'une seconde

def plot_cpu_usage(timestamps, cpu_percentages, title, label):

    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, cpu_percentages, label=label)
    plt.xlabel("Horodatage")
    plt.ylabel("Utilisation du CPU (%)")
    plt.title(title)
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    print("Collecte de données sur l'utilisation normale du CPU...")
    timestamps_normal, cpu_percentages_normal = collect_cpu_data()
    plot_cpu_usage(timestamps_normal, cpu_percentages_normal, "Évolution de l'utilisation normale du CPU", "Utilisation normale de la CPU")

    print("Simulation de charge sur le CPU...")
    simulate_load()

    print("Collecte de données sur l'utilisation du CPU sous charge...")
    timestamps_load, cpu_percentages_load = collect_cpu_data()
    plot_cpu_usage(timestamps_load, cpu_percentages_load, "Évolution de l'utilisation de la CPU sous charge", "Utilisation de la CPU sous charge")

if __name__ == "__main__":
    main()
