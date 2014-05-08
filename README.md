Q-crawler
===========

[![Build Status](https://travis-ci.org/xiaohan2012/q-crawler.png?branch=master)](https://travis-ci.org/xiaohan2012/q-crawler)

#Installation

`>>git clone`

`>>pip install -r requirements.txt`

#Run the demo

#Usage

##training

`>> cd src`

`>> python classifier_util.py train`

And the produced classifier will be pickled and put in `data/classifier.pickle`.

##crawling
`>> cd src/spider`

`>> scrapy crawl apprentice %for the reinforcement learning based crawler`

`>> scrapy crawl baseline %for the reinforcement learning based crawler`

##Performance monitoring

`>> cd src/spider`

`>> make`

Open the `comparison.html` using modern web browser(Firefox 24.4.0 tested OK).

Some example performance plot is [here](http://www.cs.helsinki.fi/u/hxiao/rl-project/comparison.html).

##Training data preprocessing 

Merge the positive/negative training samples into two separate files, each for one class. Each line represents one traing sample and consists of the tokens in the sample and is ended with class label of the sample(`pos` or `neg`).

Put both files under the `data` directory. Name the postive sample files to `pos` and negative sample files to `neg`.

See [this(for negative samples)](https://raw.githubusercontent.com/xiaohan2012/q-crawler/master/data/neg) and [this(for positive samples)](https://raw.githubusercontent.com/xiaohan2012/q-crawler/master/data/pos) files for example.

##Configuration

1. Maximum number of crawled URLs: change  `CLOSESPIDER_ITEMCOUNT`'s value in [this](https://github.com/xiaohan2012/q-crawler/blob/master/src/spider/spider/settings.py) file
2. Starting URLs: change`START_URLS`'s value in [this](https://github.com/xiaohan2012/q-crawler/blob/master/src/spider/spider/settings.py) file

#Contact
xiaohan2012 at gmail.com

