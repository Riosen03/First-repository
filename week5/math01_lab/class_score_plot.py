import matplotlib.pyplot as plt

def read_data(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            if not line.startswith('#'): # If 'line' is not a header
                data.append([int(word) for word in line.split(',')])
    return data

if __name__ == '__main__':
    # Load score data
    class_kr = read_data('data/class_score_kr.csv')
    class_en = read_data('data/class_score_en.csv')

    # TODO) Prepare midterm, final, and total scores
    midterm_kr, final_kr = zip(*class_kr)
    total_kr = [40/125*midterm + 60/100*final for (midterm, final) in class_kr]
    midterm_en, final_en = zip(*class_en)
    total_en = [40/125*midterm + 60/100*final for (midterm, final) in class_en]

    # TODO) Plot midterm/final scores as pointsx
    plt.scatter(midterm_kr, final_kr, c='red', label='Korean')
    plt.scatter(midterm_en, final_en, c='blue', marker='+', label='English')
    plt.grid()
    plt.xlabel("Midterm scores")
    plt.ylabel("Final scores")
    plt.xlim(0,125)
    plt.ylim(0,100)
    plt.legend()

    # TODO) Plot total scores as a histogram
    bin_list = []
    for i in range(0,101,5):
        bin_list.append(i)
    plt.figure() 
    plt.hist(total_kr, color='red', alpha=0.5, label='Korean', bins=bin_list)
    plt.hist(total_en, color='blue', alpha=0.5, label='English', bins=bin_list)
    plt.xlabel("Total scores")
    plt.ylabel("The number of students")
    plt.xlim(0,100)
    plt.legend()

    plt.show()