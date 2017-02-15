## WikiCrawler

WikiCrawler is a Python program that takes in a random Wikipedia url and follows its first link until it either reaches the Philosophy page, is part of a loop, or has no next link.

### Answers
1. The percentage of pages that lead to the Philosophy page is  ~97%
2. The distribution for 500 path lengths is pretty varied. The closest links are 1 step away and the farthest I found after running my program several times was 34 links away. The majority of links are between 9 - 13 steps away from Philosophy and the average is ~14 steps away.
3. There are several ways to reduce the number of HTTP requests necessary for 500 random starting pages. The Wikipedia API has a `rnlimit` attribute that can be set to an integer value and sent with the request params. It will return an array of that number of random Wikipedia pages with just that one request.

Additionally, to prevent re-asking for information on a page we have already seen, I opted to keep a dictionary of all pages that have been come across. Their urls are the keys and their link distance from Philosophy is the value.

While clicking on the first link of every page, I first check to see if it is a link I have come across before. If it is a valid link, I add its number of links to Philosophy to my current tally. I then make a call to empty my current path, since I know I have the information to calculate how far every link in the current path is from Philosophy (or if it will ever even get there).

Additionally, if we assume that we merely need to check 500 different links, rather than the 500 specific ones that we originally query for, we can get there a lot faster since we have been keeping track of the total links we have seen in the memo dictionary. Once there are 500 unique keys in `seen_urls` we already have the information we need to get our answers without actually having to go down 500 separate paths.

### Thoughts

#### Use of Dictionaries

Because I have to check against the current `path`, to make sure the link I am on is not a loop, and also against `seen_urls`, to guard against making extraneous requests for information I've already seen, I wanted to make look up as fast as possible. Though the syntax for seeing if something is in a dictionary is the same as checking if it's in a list, checking in a dictionary happens in 0(1) time. In a list lookup it is 0(n).

#### Tracking Clicks Away

I save the current count at the time I reach a url as its value in `path`. When I reache the end of the path, either by getting to Philosophy or it becoming invalid in some way, I transfer the urls in my current path to my memo dictionary and track their clicks from Philosophy by subtracting the value from the total amount of clicks away plus one.

### To Use

If you would like to use this script for yourself, please first download the requirements.txt file.
