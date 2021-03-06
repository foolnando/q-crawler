import setting
import unittest, nltk, random
from nltk.corpus import movie_reviews

from src.classifier import NBClassifier
from src.util import read_traindata

class NBClassifierToyTest (unittest.TestCase):
    def setUp (self):
        """
        first train the model
        """
        self.classifier = NBClassifier ()
        traindata = read_traindata (setting.DIRNAME + '/data/train.txt', labels=['spam', 'ham'])
        self.classifier.train (traindata)

    def test_prediction1 (self):
        """
        test prediction for sample 1
        """
        sample = ['FREE', 'online', 'conference', '!!!']
        prediction = self.classifier.predict (sample)

        expected = {u'spam': 0.8371836806110771, u'ham': 0.16281631938892294}

        for cls in expected.keys ():
            self.assertAlmostEqual (prediction [cls], expected [cls])

    def test_prediction2 (self):
        """
        test prediction for sample 2
        """
        sample = ['conference', 'registration', 'results', 'conference', 'online']
        prediction = self.classifier.predict (sample)

        expected =  {u'ham': 0.9683852022829362, u'spam': 0.031614797717063825}

        for cls in expected.keys ():
            self.assertAlmostEqual (prediction [cls], expected [cls])

    def ttest_unknown_words (self):
        """
        test prediction with unknown words
        """
        sample = ['conference', 'registration', 'results', 'conference', 'online', '(&^*^*&^*']
        prediction = self.classifier.predict (sample)
        
        expected = {u'ham': 0.9698452719061822, u'spam': 0.030154728093817886}

        for cls in expected.keys ():
            self.assertAlmostEqual (prediction [cls], expected [cls])

class NBClassifierRealTest (unittest.TestCase):
    """This time is real!"""

    def setUp (self):
        """
        first train the model
        """
        nltk.download ('movie_reviews')
        
        documents = [(map(lambda word: word.lower (), list(movie_reviews.words(fileid))), category)
                     for category in movie_reviews.categories()
                     for fileid in movie_reviews.fileids(category)]

        random.seed (123456)
        random.shuffle (documents)

        train_set, self.test_set = documents[100:], documents[:100]
        
        self.classifier = NBClassifier ()
        self.classifier.train (train_set)
        
    def test_accuracy (self):
        """
        first train the model
        """
        def get_label (doc):
            table = self.classifier.predict (doc)
            return max (table.keys (), key=lambda label: table[label])

        predicted_labels = map(lambda (doc, label): get_label (doc) , self.test_set)
        true_labels = map (lambda (doc, label): label, self.test_set)
        correct_count = sum(map (lambda (tl, pl): tl == pl and 1 or 0, zip (true_labels, predicted_labels)))

        actual = correct_count / float(len (true_labels))
        expected = .81

        self.assertAlmostEqual (actual, expected)

class NBClassifierIncrementalTrainTest (unittest.TestCase):
    def setUp (self):
        """
        first train the model
        """
        self.classifier = NBClassifier ()
        traindata = read_traindata (setting.DIRNAME + '/data/train.txt', labels=['spam', 'ham'])
        self.classifier.train (traindata)

    def test_train (self):
        """
        test prediction for sample 1
        """
        samples = [(['FREE', 'online', 'food', '!!!'], 'spam' ),
                  (['interesting', 'stuff', 'online'], 'ham')]
        
        prediction = self.classifier.train (samples)

        expected = {'spam': sorted({u'!!!': 5, u'FREE': 5, u'online': 3, u'results': 1, u'registration': 1, u'food': 1}.items ()),
                    'ham': sorted({u'conference': 3, u'repository': 2, u'online': 3, u'results': 2, u'rsults': 1, u'registration': 1, u'interesting': 1, u'stuff': 1}.items ())}
        
        self.assertEqual (sorted(self.classifier.labels ()), sorted(['ham', 'spam'])) #test label set
        
        for label in self.classifier.labels ():
            self.assertEqual (expected [label], sorted(self.classifier.feature_freq () [label].items ())) #feature frequency
            self.assertEqual (4, self.classifier.label_freq () [label])#label frequency
            
        #test vocabulary
        self.assertEqual (self.classifier.vocabulary (), set([u'conference', u'rsults', u'!!!', u'repository', 'food', 'interesting', u'online', u'results', u'FREE', 'stuff', '__RARE__', u'registration']))
        

if __name__ == "__main__":
    unittest.main ()
