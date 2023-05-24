import numpy as np
from sklearn.model_selection import train_test_split, KFold


def split_data(req):
    match req['type']:
        case "hold_out":
            couple = []
            X_train, X_test = train_test_split(req['dataset'], test_size=req['properties']['test_size'],
                                               shuffle=req['properties']['shuffle'],
                                               random_state=req['properties']['random_state'])
            couple.append(X_train)
            couple.append(X_test)
            req['train_test'] = couple
            print(req)
            return req
        case "k-fold":
            kf = KFold(n_splits=req['properties']['n_splits'], shuffle=req['properties']['shuffle'],
                       random_state=req['properties']['random_state'])
            data = np.array(req['dataset'])
            result = []
            for train_index, test_index in kf.split(data):
                result.append([data[train_index].tolist(), data[test_index].tolist()])
                print(result)
            req['train_test'] = result
            print(req)
            return req

