from sklearn import metrics
import numpy as np
from pandas import DataFrame

class Reporter(object):

    def set_config(self, config):
        self.config = config

    def update_with_model(self, model):
        pass

    def update_with_predictions(self, dataset, x, actuals, predictions):
        pass


class ModelOutliers(Reporter):
    pass


class ConfusionMatrix(Reporter):

    def update_with_predictions(self, dataset, x, actuals, predictions):
        cm = metrics.confusion_matrix(actuals, predictions)
        if hasattr(self.config.target, 'factors'):
            names = [f[0] for f in self.config.target.factors]
            df = DataFrame(cm, columns=names, index=names)
            print df.to_string()
        else:
            print cm


class MislabelInspector(Reporter):

    def __init__(self, reported_features=None):
        self.reported_features = reported_features or []

    def update_with_model(self, model):
        pass

    def update_with_predictions(self, dataset, x, actuals, predictions):
        for ind in actuals.index:
            a, p = actuals[ind], predictions[ind]
            if a != p:
                print "-" * 20
                print "Actual: %s\tPredicted: %s" % (a, p)
                print x.ix[ind]
                print dataset._data.ix[ind]
                i = raw_input()
                if i.startswith('c'):
                    break