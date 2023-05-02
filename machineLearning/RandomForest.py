import numpy as np
from sklearn.metrics import accuracy_score

import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix, classification_report
from sklearn.metrics import roc_curve, roc_auc_score, auc


# Create ROC curve and calculate best threshold value
def create_roc_curve(y_test, y_pred):
    # Create the ROC curve
    fpr, tpr, thresholds = roc_curve(y_test, y_pred)
    roc_auc = auc(fpr, tpr)

    print('roc_auc_score for RandomForestClassifier: ', roc_auc_score(y_test, y_pred)) # roc_auc_score samme som auc(fpr, tpr)

    # Calculate Youden's J statistic
    j_scores = tpr - fpr
    best_threshold = thresholds[np.argmax(j_scores)]
    print("Best threshold:", best_threshold)

    # Plot the ROC curve
    plt.plot(fpr, tpr, color='darkorange', label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    plt.scatter(fpr[np.argmax(j_scores)], tpr[np.argmax(j_scores)], s=70, marker='o', color='black', label='Best threshold')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.axvline(x=0.20, color='r')
    plt.axhline(y=0.76, color='b')
    plt.show()



def evaluate_rfc(rf, y_test, y_pred):
    # Evaluate the accuracy of the model
    accuracy = accuracy_score(y_test, y_pred)
    print('Accuracy:', round(accuracy*100, 2), "%")

    # Evaluate the performance of the model
    cm = confusion_matrix(y_test, y_pred, labels=rf.classes_)
    print(cm)
    print(classification_report(y_test, y_pred, digits=3))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=rf.classes_)

    disp.plot()
    plt.show()
