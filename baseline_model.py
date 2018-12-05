import os
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
from configuration import Configuration
from sklearn.metrics import roc_auc_score, roc_curve, precision_recall_curve, auc
from sklearn.decomposition import pca
from sklearn.svm import OneClassSVM

class baseline_model():
    def __init__(self, ad_score_type = 'mean', dataset = 'prosivic'):

        self.dataset = dataset
        self.exp_name = "baseline"
        self.cfg = Configuration(self.dataset, self.exp_name)
        self.dataset_choices = ['dreyeve', 'prosivic']
        self.ad_score_type = ad_score_type # choices
        self.score_choices = ['mean','mean_squared']
        self.scores = []
        self.test_data = []
        self.labels = []

        self.load_test_data() # no training required for this method
        self.check_assertions()

    def check_assertions(self):
        assert(self.dataset in self.dataset_choices)
        assert(len(self.test_data) > 0)
        assert(len(self.scores) == len(self.labels))
        assert(self.ad_score_type in self.score_choices)

    def load_train_data(self):
         self.train_data = np.array([img_to_array(load_img(self.self.cfg.train_folder + filename)) for filename in os.listdir(self.cfg.train_folder)][:self.cfg.n_train])/255.0

    def load_test_data(self):
        n_test_out = self.cfg.n_test - self.cfg.n_test_in
        X_test_in = np.array([img_to_array(load_img(self.cfg.test_in_folder + filename)) for filename in os.listdir(self.cfg.test_in_folder)][:self.cfg.n_test_in])
        X_test_out = np.array([img_to_array(load_img(self.cfg.test_out_folder + filename)) for filename in os.listdir(self.cfg.test_out_folder)][:n_test_out])
        y_test_in  = np.zeros((len(X_test_in),),dtype=np.int32)
        y_test_out = np.ones((len(X_test_out),),dtype=np.int32)
        self.test_data = np.concatenate([X_test_in, X_test_out]) / 255.0
        print("Loaded test_data: %d inliers, %d outliers"%(len(X_test_in),len(X_test_out)))
        self.labels = np.concatenate([y_test_in, y_test_out])
        print("Loaded labels: %d values"%len(self.labels))

    def score_images(self):

        if self.ad_score_type == 'mean':
            self.scores = [img.mean() for img in self.test_data]

        elif self.ad_score_type == 'mean_squared':
            self.scores = [np.square(img).mean() for img in self.test_data]

        elif self.ad_score_type == 'ocsvm':
            self.scores = self.test_model.score_samples(self.test_data)*(-1)

    def train(self):
        assert(self.ad_score_type in ("ocsvm")
        if self.ad_score_type == "ocsvm":
            # Reshape inputs to (n_train,n_pixels)
            self.train_data.reshape(len(self.train_data),-1)
            self.test_data.reshape(len(self.test_data,-1)

            # Do dim reduction via PCA
            pca_model = pca(1000)
            self.train_data = pca_model.fit_transform(self.train_data)
            self.test_data = pca_model.fit_transform(self.test_data)

            # Train OCSVM
            self.test_model = OneClassSVM()
            self.test_model.fit(self.train_data)


    def test(self):
        print("Testing dataset %s with score function %s"%(self.dataset, self.ad_score_type))

        self.score_images()

        # Compute roc_auc
        fpr, tpr, _ = roc_curve(self.labels, self.scores)
        roc_auc = auc(fpr,tpr)
        print("AUROC:\t%.5f"%roc_auc)

        # Compute roc_auc
        pr, rc, _ = precision_recall_curve(self.labels, self.scores)
        roc_prc = auc(rc,pr)
        print("AUPRC:\t%.5f"%roc_prc)

if __name__ == '__main__': # executed when file is ran with python3 energy_density_baseline.py
    for score_type in ['mean', 'mean_squared','ocsvm']:
        model = baseline_model(ad_score_type = score_type, dataset = 'prosivic')
        if model.ad_score_type == "ocsvm":
            model.train()
        model.test()
    


