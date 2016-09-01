# Luxury Handbag on Rakuten - The API
A python module which parse Rakuten.co.jp and return a list of items.

## Installation
Go in the main directory and just do:
``pip install -r requirements.txt``

## How to use it
You can use it by importing the LHR_API module, creating a instance of the LHR class and starting it.  
Like this:  
```python
from LHR_API import LHR

lhr = LHR()
lhr.start()
```
  
Once it's done, lhr.results will be filled with a list of dictionnaries.  
You can access it like this :  
```python
lhr.results[index]
```

The dictionnary's keys are:
* "name"
* "url"
* "description"
* "price" (yens)
* "picture_url"
* "seller_name"
* "seller_url"

## TODO
* Add an error manager, for exemple when the network is down or the website unreachable. (At the moment, an exeception is thrown by urllib)
* Parse the items page and not just the search page
  * Pros:
    - Get more pictures instead of the thumbnail and having a better description of the item.
  * Cons:
    - Will multiply the request amount by 46 and so the execution time from ~40 minutes to over 1 day.
* Adding asynchronous request instead of synchronous request
  * Pros:
    - It will be way more faster.
  * Cons:
    - Will have to get all the pages, store them all and process them when all pages have been got, RAM will may not be okay with this.
* Gadget thing: Add a function to convert yens into euro/dollars by getting the change rate on an other website.
