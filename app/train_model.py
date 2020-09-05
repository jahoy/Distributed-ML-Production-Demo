import timeit
import pickle
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier


def save_model(model):
    with open(f'model/clf_model.pkl', 'wb') as f:
        pickle.dump(model, f)
        print('model_saved')


def main():
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target

    # 모델 훈련
    clf = RandomForestClassifier()
    clf.fit(X, y)
    
    # 모델 저장
    save_model(clf)


if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    duration = timeit.default_timer() - start
    print('\n전체 소요시간: ', duration)