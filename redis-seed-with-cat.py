#!/usr/bin/env python3

import wiki
import redis

def populate_from_category(redis_server, cat, level=0):
    """
    Populates a redis set 'foo' with wikipedia subcategories.
    """
    if not redis_server.sismember('foo', cat) and level < 5:
        redis_server.sadd('foo', cat)
        subcat = wiki.get_subcategories(cat)
        print(level, cat, subcat)
        for c in subcat:
            populate_from_category(redis_server, c, level+1)

def main():
    # Connection to redis server
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    # To start from scratch, delete the 'foo' set from redis.
    #r.delete('foo')

    # Add subcategories to the redis set 'foo'.
    # Choose one of these as starting points.
    populate_from_category(r, 'Anatomy')
    #populate_from_category(r, 'Animal anatomy')
    #populate_from_category(r, 'Organs (anatomy)')
    #populate_from_category(r, 'Thorax (human anatomy)')


if __name__ == "__main__":
    main()
