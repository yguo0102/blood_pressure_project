import matplotlib.pyplot as plt

data = {'DATE': 4698911, 'STAFF': 1365069, 'PATORG': 829, 'ID': 1987419, 'HOSP': 1010139, 'PATIENT': 282263, 'AGE': 228366, 'LOC': 103507, 'PHONE': 1080317, 'OTHERPHI': 13, 'EMAIL': 3}

# Sorting the data by values in descending order
sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

# Extracting labels and values
labels = list(sorted_data.keys())
values = list(sorted_data.values())

# Creating the histogram
plt.bar(labels, values, color='skyblue')
plt.xlabel('Categories')
plt.ylabel('Counts')
plt.title('Data Distribution (Sorted)')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.tight_layout()

# Display the plot
plt.show()

