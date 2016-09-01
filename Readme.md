# Luxury Handbag on Rakuten - The API
A python module which parse Rakuten.co.jp and return a list of items.

## Installation
Go in the main directory and just do:
``pip install -r requirements.txt``

## How to use it
You can use it by importing the LHR_API module, creating a instance of the LHR class and starting it.
Like this:

```python
lhr = LHR()
lhr.start()
```

## TODO
* Parse the items page and not just the search page
  * Pros:
    * Get more pictures instead of the thumbnail and having a better description of the item.
  * Cons:
    * Will multiply the request amount by 46 and so the execution time from ~40 minutes to over 1 day.
* Adding asynchronous request instead of synchronous request
  * Pros:
    * It will be way more faster.
  * Cons:
    * Will have to get all the pages, store them all and process them when all pages have been got, RAM will may not be okay with this.
