from sklearn.model_selection import train_test_split
import glob

if __name__ == "__main__":

    X = glob.glob("../NTuples/**/*.root")

    X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)
    X_train, X_val = train_test_split(X_train, test_size=0.2, random_state=42)

    print(X_train)