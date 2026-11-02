"""Recompute metrics from the legacy displayed matrix, not a fresh evaluation."""
import json

def metrics(tn=73, fp=290, fn=53, tp=1584):
    recall = tp/(tp+fn)
    specificity = tn/(tn+fp)
    return {'source': 'Legacy displayed synthetic confusion matrix; raw cases unavailable',
            'confusion_matrix': [[tn, fp], [fn, tp]],
            'accuracy': (tp+tn)/(tp+tn+fp+fn),
            'precision': tp/(tp+fp), 'recall': recall,
            'f1': 2*tp/(2*tp+fp+fn), 'specificity': specificity,
            'balanced_accuracy': (recall+specificity)/2,
            'always_positive_accuracy': (tp+fn)/(tp+tn+fp+fn),
            'drought_validated': False}

if __name__ == '__main__':
    print(json.dumps(metrics(), indent=2))
