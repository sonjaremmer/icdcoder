'''
Main script for using the baseline models

Author: Sonja Remmer

'''

from scripts.train import train_baseline
from scripts.train_test import train_test_baseline
from scripts.test import test_baseline_filepath, test_baseline_text

import argparse
import os


def main(train_and_test_data,
    train_data, 
    test_data,
    test_text, 
    trained_model,
    vectorizer,
    new_vectorizer,
    new_trained_model,
    test_size,
    n_kfold, 
    random_state,
    classifier,
    stopwords):
    
    # If argument train_and_test_data is given, the finetune_evaluate function is run
    if train_and_test_data:
        train_test_baseline(train_and_test_data=train_and_test_data, 
            stopwords=stopwords,
            new_vectorizer=new_vectorizer,
            new_trained_model=new_trained_model, 
            random_state=random_state, 
            classifier=classifier,
            test_size=test_size,
            n_kfold=n_kfold)

    # If argument train_data is given, the finetune function is run
    elif train_data:
        train_baseline(train_data=train_data, 
            stopwords=stopwords, 
            new_vectorizer=new_vectorizer,
            new_trained_model=new_trained_model, 
            random_state=random_state, 
            classifier=classifier)

    # If argument test_data is given, the evaluate function is run with the test filepath as input
    elif test_data:
        test_baseline_filepath(test_data=test_data,
            trained_model=trained_model, 
            vectorizer=vectorizer, 
            stopwords=stopwords)

    # If argument test_text is given, the evaluate function is run with the test text as input
    elif test_text:
        test_baseline_text(test_text=test_text,
            trained_model=trained_model, 
            vectorizer=vectorizer, 
            stopwords=stopwords)


if __name__ == '__main__':

    # Defining default values
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_stopwords = base_dir+'/stopwords.txt'
    default_trained_model = base_dir+'/models/trained_baseline_model/ICD_model.sav'
    default_vectorizer = base_dir+'/models/trained_baseline_model/vectorizer.sav'
    default_new_trained_vectorizer = base_dir+'/models/new_baseline_model/vectorizer.sav'
    default_new_trained_model = base_dir+'/models/new_baseline_model/ICD_model.sav'
    default_test_size = 0.1
    default_random_state = None
    default_classifier = 'SVM'
    default_kfold = 10
    
    
    parser = argparse.ArgumentParser()
    mutually_exclusive = parser.add_mutually_exclusive_group(required=True)

    # Arguments -train, -train_and_test and -test are mutually exclusive and at least one is required
    mutually_exclusive.add_argument('-train', dest='only_train_data', type=str, default=None,
                        help='Filepath to csv file used for training. The file needs to follow the structure specified in the README section How to get hold of/prepare datasets.')
    mutually_exclusive.add_argument('-train_and_test', dest='train_and_test_data', type=str, default=None,
                        help='Filepath to csv file used for training and testing. The file needs to follow the structure specified in the README section How to get hold of/prepare datasets.')
    mutually_exclusive.add_argument('-test_file', dest='test_data', type=str, default=None,
                        help='Filepath to csv file used for testing. The file needs to follow the structure specified in the README section How to get hold of/prepare datasets.')
    mutually_exclusive.add_argument('-test_text', dest='test_text', type=str, default=None,
                        help='Discharge summary to predict ICD codes for.')

    # The rest of the arguments are optional and while not all functions are compatible with all main arguments, passing a non-compatible argument will just be ignored 
    parser.add_argument('-stopwords', dest='stopwords', type=str, default=default_stopwords,
                        help='Filepath to txt file with stopwords. Default is ./stopwords.txt', required=False)
    parser.add_argument('-trained_model', dest='trained_model', type=str, default=default_trained_model,
                        help='Filepath to trained model. Note that if trained model is specified, the vectorizer needs to be specified as well. Default is ./models/trained_baseline_model/ICD_model.sav', required=False)
    parser.add_argument('-vectorizer', dest='vectorizer', type=str, default=default_vectorizer,
                        help='Filepath to trained vectorizer. Note that if vectorizer is specified, the trained model needs to be specified as well. Default is ./models/trained_baseline_model/vectorizer.sav', required=False)
    parser.add_argument('-new_trained_model', dest='new_trained_model', type=str, default=default_new_trained_model,
                        help='Filepath to new trained model. Default is /models/new_baseline_model//ICD_model.sav', required=False)
    parser.add_argument('-new_vectorizer', dest='new_vectorizer', type=str, default=default_new_trained_vectorizer,
                        help='Filepath to new trained vectorizer. Default is /models/new_baseline_model/vectorizer.sav', required=False)
    parser.add_argument('-test_size', dest='test_size', type=float, default=default_test_size,
                        help='Fraction of data to use for testing. Must be between 0 and 1. Default is 0.1.', required=False)
    parser.add_argument('-random_state', dest='random_state', type=int, default=default_random_state,
                        help='A seed (integer) to use as the random state when splitting the data. Default is None', required=False)
    parser.add_argument('-kfold', dest='n_kfold', type=int, required=False, default=default_kfold,
                        help='The number of folds (k) to use in k-fold cross-validation, must be > 1 for kfold to be used and default is 10.')
    parser.add_argument('-classifier', dest='classifier', type=str, required=False, default=default_classifier,
                        help='The desired classifier. Enter SVM, KNN or DT which represent Support Vector Machines, K-Nearest Neigbors, and Decision Trees. Default is SVM.')
    
    args = parser.parse_args()

    main(train_and_test_data=args.train_and_test_data,
        train_data=args.only_train_data,
        test_data=args.test_data,
        test_text=args.test_text,
        stopwords=args.stopwords,
        trained_model=args.trained_model,
        vectorizer=args.vectorizer,
        new_vectorizer=args.new_vectorizer,
        new_trained_model=args.new_trained_model,
        test_size=args.test_size,
        random_state=args.random_state,
        n_kfold=args.n_kfold,
        classifier=args.classifier)
