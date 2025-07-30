# Build Your Own Spell Checker Using A Bloom Filter
This challenge is to build your own micro spell checker. The goal is to create a spell checker that can determine if a word is probably spelt correctly without having to store the full list of words. Thus the spell checker can use less storage (disk or memory). A task that is much less relevant these days, but 20 years ago was incredibly useful on low storage devices.

Whilst we don’t have this problem with spell checking today, we do have similar problems checking if an item is in a data set that would be too big to store efficiently.

So how are these problems solved? With Bloom filters.

A bloom filter is a probabilistic data structure. It is built around a bit array and one or more hash functions. It provides a fast and efficient way of handling set membership queries when the set either does not fit within the memory constraints, or querying the full set would incur a performance penalty.

Bloom filters have been used in:

👉 Spell checkers - like you’re going to build in this Coding Challenge.

👉 Network routers - speeding up packet routing protocols amongst other uses.

👉 Databases - a quick way of determining if if a row is likely to be in the database without performing costly disk lookups. Used in Google’s Bigtable, Apache HBase, Apache Cassandra and Postgres

👉 Web crawlers - don’t re-crawl a URL that’s already been seen.

👉 Cyber security - blacklisting, whitelisting and password / username checkers

👉 Web caches - preventing ‘one hit wonders’ being stored in disk caches for CDNs.

👉 Cryptocurrency - Speeding up wallet synchronisation and finding logs in the blockchain.

👉 Recommendation systems - Medium has used Bloom filters to not recommend articles you’ve already seen.